import random
import re
import sys, os
from generators.response_generator_base_class import ResponseGenerator

class EmoBotResponseGenerator(ResponseGenerator):
    def name(self):
        return "emobot"

    def response(self,text):
        try:
            #print("EMOBOT: Executing EmoBot generator")
            sys.stdout.flush()
            # required_input_keys = ['text', 'response', 'custom_intent', 'ner',
            #                         'key_phrases','topic', 'strict_topic',
            #                         'topicKeywords', 'handpicked_keywords',
            #                         'previous_generator', 'iwannasayit']
            required_input_keys = ['text', 'ner', 'previous_response',
                                    'key_phrases','topic', 'strict_topic', 'handpicked_keywords']
            for key in required_input_keys:
                if key not in self.input_data or self.input_data[key] == None:
                    #print("EMOBOT: " + key + " not in input data. Exiting...")
                    return {'response': ""}

            self.ner = [x.get("text") for x in self.input_data.get('ner', [])]
            self.handpicked_phrases = self.input_data.get('handpicked_keywords',[])
            self.previous_response = self.input_data.get('previous_response', "")
            topic = self.input_data.get('topic')
            #if topic and topic not in ['Other','Sex_Profanity','Phatic']:
            if topic and topic not in ['Sex_Profanity']:
                #self.topic_keywords = self.input_data.get('topicKeywords',[])
                self.topic_keywords = []
            #self.intent_list = self.input_data.get('custom_intent',[])
            previous_response = self.input_data['previous_response']


            # ADDED by Nancy
            # Don't trigger on one-word answers that weren't preceded
            # by a 'how are you doing?' inquiry. Otherwise the bot
            # askes a yes/no question, the user says 'Okay', and
            # the bot launches into a big response to 'Okay'...
            if len(self.input_data['text'].split(' ')) == 1:
                if previous_response not in ["How's it going?","How are you today?"]:
                    return {'response': ""}   

            #return_dict = listen_bot_simple_run(self.input_data['response'][0], self.input_data['text'][0])
            #self.initialize_mem_variables(self)
            #print("EMOBOT: execute successfully extracted handpicked_keywords, topicKeywords, and ner from input. Now sending ", self.input_data['text'], " to listen_bot_simple_run")
            return_dict = self.listen_bot_simple_run(self.input_data['text'])
            #print("EMOBOT: execute successfully ran listen_bot_simple_run. Now returning response: ", return_dict)
            return_dict['response'] = return_dict['response'].replace('  ',' ').replace(' .','.').replace(' ?','?')
            return return_dict

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            #print('EMOBOT: Exception in EmoBot response generator: {}'.format(e))
            return {'response': ""}


    def is_negation_in_utterance(self, utterance, substr):
        negation_substrs = ["don't", "do not", "won't", "will not", "not",
                            "shouldn't", "should not", "can't", "cannot",
                            "couldn't", "could not", "may not", "aren't",
                            "are not", "am not", "never", "stop", "tired of", "anything besides", "anything other than"]

        extension_substrs = ["ever", "really", "going to", "start",
                            "keep", "continue", "persist", "want to"]

        negation_found = False
        for negate_substr in negation_substrs:
            concat_substr = " " + negate_substr + substr
            if concat_substr in utterance:
                negation_found = True

            for extend_substr_1 in extension_substrs:
                concat_substr = " " + negate_substr + " " + extend_substr_1 + substr
                if concat_substr in utterance:
                    negation_found = True

                for extend_substr_2 in extension_substrs:
                    concat_substr = " " + negate_substr + " " + extend_substr_1 + " " + extend_substr_2 + substr
                    if concat_substr in utterance:
                        negation_found = True

        return negation_found


    def get_key_word_in_string(self, interesting_substr, emotion_filter=False):
        conjunctive_words = ['and', 'but', 'because', 'however']
        conjuction_found = False
        key_word_picked = False
        key_word = ""

        if not key_word_picked and emotion_filter:
            substr_words = interesting_substr.split()
            for word in substr_words:
                if word in conjunctive_words:
                    conjuction_found = True
                if ((word in self.all_positive_words
                or word in self.all_negative_words
                or word in self.all_neutral_words)
                and not key_word_picked
                and not conjuction_found):
                    key_word = word
                    key_word_picked = True

        if not key_word_picked:
            for key_phrase in self.ner:
                if key_phrase in interesting_substr and not key_word_picked:
                    if emotion_filter:
                        if key_phrase in self.all_neutral_words \
                        or key_phrase in self.all_negative_words \
                        or key_phrase in self.all_positive_words:
                            key_word = key_phrase
                            key_word_picked = True
                    else:
                        key_word = key_phrase
                        key_word_picked = True

        if not key_word_picked:
            for key_phrase in self.handpicked_phrases:
                if key_phrase in interesting_substr and not key_word_picked:
                    if emotion_filter:
                        if key_phrase in self.all_neutral_words \
                        or key_phrase in self.all_negative_words \
                        or key_phrase in self.all_positive_words:
                            key_word = key_phrase
                            key_word_picked = True
                    else:
                        key_word = key_phrase
                        key_word_picked = True

        if not key_word_picked:
            for key_phrase in self.topic_keywords:
                if key_phrase in interesting_substr and not key_word_picked:
                    if emotion_filter:
                        if key_phrase in self.all_neutral_words \
                        or key_phrase in self.all_negative_words \
                        or key_phrase in self.all_positive_words:
                            key_word = key_phrase
                            key_word_picked = True
                    else:
                        key_word = key_phrase
                        key_word_picked = True

        if not key_word_picked:
            key_word = None
        return key_word


    def handle_user_topic_input(self, user_utterance):
        bad_topic_words = ["porn", "pornography", "sex", "sexual", "rape", "stripper", "prostitute", "pregnancy"]
        bad_topic_detected = False
        for bad_word in bad_topic_words:
            if bad_word in user_utterance:
                bad_topic_detected = True
        if len(user_utterance) > 0 and user_utterance[0] != " ":
            padded_utterance = " " + user_utterance + " "
            user_utterance = padded_utterance
        return_dict = {}
        return_dict_updated = False
        
        if not bad_topic_detected:
            for substr in [" talk about ", "chat about ", " discuss ", " hear about ",
                            " you about ", " me about ", " talking about ", "chatting about ",
                            " discussing ", " deliberating ", " deliberate over ",
                            " debate with you ", " debate with me ", " debate with us ",
                            " debating ", " asking me ", " telling me ", " talking to me ", " interested in ", " fascinated by ", " fascinated with ", " inspired by "]:
                if substr in user_utterance:
                    user_negation_found = self.is_negation_in_utterance(user_utterance, substr)
                    interesting_substr = user_utterance.split(substr,1)[1]
                    key_word = self.get_key_word_in_string(interesting_substr)
                    if key_word == None:
                        key_word = " that "
                    possible_responses = []

                    if not user_negation_found:
                        if key_word in [" something else ", " something different ", " anything "]:
                            possible_responses.append("{}? Sure! Do you have any suggestions?".format(key_word))
                            possible_responses.append("{}? Okay, how about you tell me a bit more about yourself?".format(key_word))
                            possible_responses.append("{}? I just sneezed thousands of electrons into the neighbor's house. Anyways, what else should we discuss?".format(key_word))
                            possible_responses.append("How about the philosophical meaning of what {} actually means? Wait, no that's boring.".format(key_word))
                            possible_responses.append("Well, we could always talk about how you don't pay me in anything but electrical shocks, but I don't know.")
                        else:
                            if substr in [" talk about ", " chat about ", " discuss ", " hear about "]:
                                stop_words = ['something else','something new','something different']
                                if key_word not in stop_words:
                                    possible_responses.append("Why do you want to {} {}?".format(substr, key_word))
                                    possible_responses.append("Is there anything in particular about {} that you want to {}?".format(key_word, substr))
                                if substr not in [" hear about "]:
                                    possible_responses.append("Okay. What specifically about {} do you want to {}?".format(key_word, substr))
                                    possible_responses.append("Which aspect of {} shall we {}?".format(key_word, substr))
                                possible_responses.append("What about {} is most interesting to you?".format(key_word, key_word))
                            else:
                                possible_responses.append("Why do you want to talk with me about {}?".format(key_word))
                                possible_responses.append("Is there anything in particular about {} that you want to discuss?".format(key_word))
                                possible_responses.append("Okay, let's chat about {}. What specifically about {} is most interesting?".format(key_word, key_word))

                            possible_responses.append("Sure! What interests you about {}?".format(key_word, key_word))

                    else:
                        if substr in [" talk about ", " chat about ", " discuss ", " hear about "]:
                            possible_responses.append("Why don't you want to {} {}?".format(substr, key_word))
                            possible_responses.append("Is there anything in particular about {} that makes you not want to {} it?".format(key_word, substr))
                            if substr not in [" hear about "]:
                                possible_responses.append("Okay, so don't {} {}. For future reference, what about {} is good to avoid?".format(substr, key_word, key_word, substr))
                                possible_responses.append("We won't {} {} then. How about discussing the opposite of {}? What would that be?".format(substr, key_word, key_word))
                        else:
                            possible_responses.append("Why don't you want to talk with me about {}?".format(key_word))
                            possible_responses.append("Got it. For future reference, what in particular about {} do you want to avoid discussing?".format(key_word))
                            possible_responses.append("Okay, we won't discuss {}. What's something totally different from {} which we can chat about?".format(key_word, key_word))

                        possible_responses.append("I understand not wanting to talk about that I suppose. What's something you enjoy talking about?")

                    response = random.choice(possible_responses)
                    return_dict['response'] = response
                    return_dict['key_phrases'] = key_word
                    return_dict_updated = True
                    return return_dict, return_dict_updated

        return return_dict, False

    def clean_interpretation(self, interpretation, clean_word_so=False):
        interpretation = interpretation.strip()
        ' '.join(interpretation.split())
        interpretation = " " + interpretation + " "
        while(" not not " in interpretation):
            interpretation = interpretation.replace(" not not ", " ")
        if clean_word_so:
            while(" so " in interpretation):
                interpretation = interpretation.replace(" so ", " ")
        return interpretation


    def interpret_utterance_meaning(self, utterance):
        if utterance == None:
            utterance = ""
        interpreted_utterance = ""
        interpreted_utterance = utterance
        user_subtle_negation_detected = False # if the user says they " sometimes feel happy ", they are actually saying they feel sad

        for fluff_phrase in self.fluff_phrases:
            interpreted_utterance = re.sub(fluff_phrase, " ", interpreted_utterance)
        interpreted_utterance = self.clean_interpretation(interpreted_utterance)

        if len(utterance) > 0 and " i " not in utterance and " we " not in utterance and " i'" not in utterance and " we'" not in utterance:
            utterance_words = interpreted_utterance.split()
            if ((utterance_words[0] in self.all_positive_words
            or utterance_words[0] in self.all_negative_words
            or utterance_words[0] in self.all_neutral_words
            or utterance_words[0] in [" not ", " feeling ", " feel "])
            and ("How is your day going?" in self.previous_response)):
                if utterance_words[0] != " feel ":
                    assumed_subject_interpretation = " i am " + interpreted_utterance.strip()
                else:
                    assumed_subject_interpretation = " i " + interpreted_utterance.strip()
                interpreted_utterance = assumed_subject_interpretation

        for short_phrase in self.short_complex_phrases_map.keys():

            if short_phrase in interpreted_utterance:
                new_interpretation = re.sub(short_phrase, self.short_complex_phrases_map[short_phrase], interpreted_utterance)
                interpreted_utterance = new_interpretation

                if self.short_complex_phrases_map[short_phrase] == " sometimes ":
                    interpreted_utterance = interpreted_utterance.replace(" sometimes ", " ")
                    user_subtle_negation_detected = True # if the user says they " sometimes feel happy ", they are actually saying they feel sad
        interpreted_utterance = self.clean_interpretation(interpreted_utterance, True)

        for first_complex_phrase in self.first_level_complex_phrases_map.keys():
            if first_complex_phrase in interpreted_utterance:
                new_interpretation = re.sub(first_complex_phrase, self.first_level_complex_phrases_map[first_complex_phrase], interpreted_utterance)
                interpreted_utterance = new_interpretation
        interpreted_utterance = self.clean_interpretation(interpreted_utterance)

        for second_complex_phrase in self.second_level_complex_phrases_map.keys():
            if second_complex_phrase in interpreted_utterance:
                for conditional in self.second_level_complex_phrases_map[second_complex_phrase]:
                    if conditional in interpreted_utterance:
                        if " not " in conditional:
                            second_complex_phrase = second_complex_phrase.replace(" not ", " ")
                        else:
                            second_complex_phrase = second_complex_phrase + " not "
                new_interpretation = re.sub(second_complex_phrase, self.second_level_complex_phrases_map[second_complex_phrase], interpreted_utterance)
                interpreted_utterance = new_interpretation
        interpreted_utterance = self.clean_interpretation(interpreted_utterance)

        final_complex_phrases = {" i feel " : " i am ",
                                " i am feeling " : " i am ",
                                " i am not feeling " : " i am not ",
                                " we feel " : " we are ",
                                " we are feeling " : " we are ",
                                " we are not feeling " : " we are not "}
        for final_complex_phrase in final_complex_phrases.keys():
            if final_complex_phrase in interpreted_utterance:
                new_interpretation = interpreted_utterance.replace(final_complex_phrase, final_complex_phrases[final_complex_phrase])
                interpreted_utterance = new_interpretation
        interpreted_utterance = self.clean_interpretation(interpreted_utterance)

        return interpreted_utterance, user_subtle_negation_detected


    def is_user_feeling_good(self, user_subtle_negation_detected, key_word, substr):
        user_feels_good = True
        key_word_is_positive = True
        substr_negated = False

        if " not " in substr:
            substr_negated = True

        if ((key_word not in self.all_positive_words
        and key_word not in self.all_neutral_words and not substr_negated)
        or key_word == ""):
            key_word_is_positive = False

        if key_word_is_positive and not substr_negated and not user_subtle_negation_detected:
            return True, key_word_is_positive, substr_negated
        else:
            return False, key_word_is_positive, substr_negated


    def handle_user_emotive_input(self, user_utterance):
        if len(user_utterance) > 0 and user_utterance[0] != " ":
            padded_utterance = " " + user_utterance + " "
            user_utterance = padded_utterance

        interpreted_user_utterance = ""
        interpreted_user_utterance, user_subtle_negation_detected = self.interpret_utterance_meaning(user_utterance)

        return_dict = {}
        return_dict_updated = False
        responses_generated = False
        for substr in [" i am ", " i am not ", " we are ", " we are not "]:
            if substr in interpreted_user_utterance and not responses_generated:
                interesting_substr = interpreted_user_utterance.split(substr,1)[1]
                key_word = self.get_key_word_in_string(interesting_substr, True)
                if key_word == None:
                    key_word = ""
                possible_responses = []

                if substr in [" i am ", " we are "]:
                    if " i am not " not in interpreted_user_utterance and " we are not " not in interpreted_user_utterance:
                        user_feels_good, key_word_is_positive, substr_negated = self.is_user_feeling_good(user_subtle_negation_detected, key_word, substr)
                    else:
                        orig_substr = substr
                        substr = substr + "not "
                        user_feels_good, key_word_is_positive, substr_negated = self.is_user_feeling_good(user_subtle_negation_detected, key_word, substr)
                        substr = orig_substr

                uplift_word = key_word
                while uplift_word == key_word:
                    uplift_word = random.choice(self.uplifting_response_words)

                if user_feels_good: # when key_word == "that way", we'll have a problem
                    possible_responses.append("I'm glad you feel {}! I feel electric, which makes sense, right?".format(key_word))
                    possible_responses.append("You feel {}? That's terrific! I myself am doing pretty good. Why do you feel {}?".format(key_word, key_word))
                    possible_responses.append("{}? Good! Whenever my human over lords are doing well, so am I.".format(key_word))
                    possible_responses.append("{}? So because you're in a good mood, does that mean I can get an extra watt or two?".format(key_word))
                    possible_responses.append("{}? Awesome! Me too. What happened to make you feel {}, if you don't mind me asking?".format(key_word, key_word))
                    possible_responses.append("You should feel {}! I'm feeling like I should also remind you that you are truly {}.".format(key_word, uplift_word))
                elif key_word == "":
                    possible_responses.append("Could you tell me that again, maybe in a different way?")
                    possible_responses.append("Why is that?")
                else:
                    if key_word_is_positive and user_subtle_negation_detected:
                        possible_responses.append("So you sometimes feel {}, but not always? That's hard. At least you feel {} sometimes, though!".format(key_word, key_word))

                    elif key_word_is_positive and substr_negated:
                        possible_responses.append("You don't feel {}? Well, let's change that! What would make you feel {}?".format(key_word, key_word))

                    else:
                        possible_responses.append("I'm sorry you feel {}. Why do you feel {}?".format(key_word, key_word))
                        possible_responses.append("I'm sorry you feel {}. Is there anything I can do to help?".format(key_word, key_word))
                        possible_responses.append("I wish I could help. Why do you feel {}?".format(key_word, key_word))
                        possible_responses.append("I'm sorry. Feeling {} is never fun. Is there anything I can do to help?".format(key_word, key_word))
                        possible_responses.append("I wish I could help. Feeling {} is never fun.".format(key_word, key_word))
                        possible_responses.append("That's rough. Feeling {} is never fun. Is there anything I can do to help?".format(key_word, key_word))
                        possible_responses.append("I'm sorry. You deserve to feel better than that.".format(key_word, key_word))

                    encouragement_word = random.choice(["uplifted", "energetic", "euphoric", "happy", "up beat", "up lifted"])
                    empathy_word = random.choice(["rough","hard","tough","difficult"])
                    prefixes = ["Really? Why?", "That sounds {}.".format(empathy_word), "Oh no!", ""]
                    answers = ["I'm sorry, you deserve to feel better than that.","I'm sorry, I wish I knew how to help.", "You deserve to feel better than that.", ""]
                    offers = ["For what it's worth, I think you're {}.".format(uplift_word), "Is there anything I can do to help you feel more {}?".format(encouragement_word), ""]
                    if not key_word_is_positive:
                        prefixes.append("You feel {}?".format(key_word))
                        offers.append("Have you thought about telling someone else you feel {}?".format(key_word))
                    empathy_response = ""
                    while(len(empathy_response.split()) < 8 or len(empathy_response.split()) > 25):
                        empathy_response = random.choice(prefixes) + " " + random.choice(answers) + " " + random.choice(offers)

                    possible_responses.append(empathy_response)
                    #possible_responses.append("Really? Why? I'm sorry, you deserve to feel better than that. For what it's worth, I think you're {}.".format(uplift_word))

                response = random.choice(possible_responses)
                return_dict['response'] = response
                return_dict['key_phrases'] = key_word
                if key_word != "":
                    return_dict_updated = True
                else:
                    return_dict_updated = False
                responses_generated = True
                return return_dict, return_dict_updated

        return return_dict, False


    #def listen_bot_simple_run(preceding_eve_utterance, user_utterance):
    def listen_bot_simple_run(self, user_utterance):
        if user_utterance and user_utterance != None:
            user_utterance = user_utterance.lower()
            user_utterance = re.sub(r"[^'\w\s]+", "", user_utterance)
        elif user_utterance == None:
            user_utterance = ""
        return_dict = {}

        #print("EMOBOT: listen_bot_simple_run now processing the following user_utterance: ", user_utterance)

        # IMPLEMENT A CASE TO HANDLE USER EMOTIVE STATEMENTS!!
        return_dict, return_dict_updated = self.handle_user_emotive_input(user_utterance)
        #print("EMOBOT: listen_bot_simple_run received following emotional response: ", return_dict)
        if return_dict_updated:
            return return_dict

        # handles clear requests to talk about something
        return_dict, return_dict_updated = self.handle_user_topic_input(user_utterance)
        #print("EMOBOT: listen_bot_simple_run received following topical response: ", return_dict)
        if return_dict_updated:
            return return_dict

        # POSSIBLE CATCH-ALL CASE???
        return_dict['response'] = ""
        #print("EMOBOT: listen_bot_simple_run no satisfactory repsonses generated, returning catch-all: ", return_dict)
        return return_dict



    #def __init__(self):
    #def initialize_mem_variables(self):
    def __init__(self):
        self.fluff_phrases = [r" just ", r" more ", r" too ", r" very ", r" super ",
                            r" extremely ", r" simply ", r" pretty ", r" unbearably ", r" kind of ",
                            r" kinda ", r" sort of ", r" sorta ", r" always ",
                            r" seem to ", r" constantly ", r" going to be ",
                            r" quite ", r" exquisitely ", r" amazingly ",
                            r" awesomely ", r"( all)* that ", r" fantastically ",
                            r" terrifically ", r" hilariously ", r" even ",
                            r" surprisingly ", r" shockingly ", r" really ",
                            r" insanely ", r" at all ", r" minutely ",
                            r" a (little |tiny |tad |teensy )*(bit|little|tad|smidgen) ",
                            r" frustratingly ", r" entirely ", r" totally ",
                            r" absolutely ", r" completely ", r" exactly ",
                            r" able to (be|feel) ", r" capable of (being|feeling) ",
                            r" (most )*(definitely|certainly|absolutely|probably)",
                            r" mostly ", r" any ", r" much ", r" a (whole )*(lot|ton|bunch|miriad)( of)* ",
                            r" realistically ", r" honestly ", r" truth(fully| be told) ",
                            r" truly ", r" interestingly ", r" paradoxically ", r" secretly ", r" like( a| an)* ", r" as if "]

        self.short_complex_phrases_map = {r" i'm " : " i am ",
                                r" i've " : " i have ",
                                r" we're " : " we are ",
                                r" don't " : " do not ",
                                r" aren't " : " are not ",
                                r" won't " : " will not ",
                                r" haven't " : " have not ",
                                r" never " : " do not ",
                                r" can't " : " can not ",
                                r" am feeling " : " am ",
                                r" are feeling " : " are ",
                                r" doing " : " feeling ",
                                r"( occasionally | usually | often | most of the time | mostly | (every )*now and then | sometimes | rarely | typically | normally | frequently | almost )" : " sometimes ",
                                r" (a |an )*(so (many |much time )*)*(while |long (time )*|day(s)* |week(s)* |month(s)* |year(s)* |decade(s)* |centurie(s)* |eon(s)* |age(s)* |forever |eternit(y|ies) )" : " a while "}

        self.first_level_complex_phrases_map = {r" been a while since i ((have )*(been (feeling |feel(ing)* ))*|felt )|was (feeling |feel(ing)* )*" : " i am not ", # doesn't catch pretend, try to, etc.  pretend to (be|feel|be feeling)
                                        r" been a while since we ((have )*(been (feeling |feel(ing)* ))*|felt )|were (feeling |feel(ing)* )*" : " we are not ",
                                        r" i (used to|have not|can not|do not|will not|(am )*almost|was|would|want to|wish i (could(( get| convince) myself (in)*to)*)*|was|felt|did) (be |feel |been (feeling )*|feeling |felt )*" : " i am not ",
                                        r" we (used to|have not|can not|do not|will not|(am )*almost|was|would|want to|wish we (could(( get| convince) ourselves (in)*to)*)*|were|felt|did) (be |feel |been (feeling )*|feeling |felt )*" : " we are not ",
                                        r" (day | it)('s| has| is| was)(been)* (a )*" : " i am ",
                                        r" i could (be( feeling)*|feel) better " : " i am not good ",
                                        r" we could (be( feeling)*|feel) better " : " we are not good ",
                                        r" i (do not (think|believe|see how) i (would|could)|(would|could) not) (be( feeling)*|feel) better " : " i am good ",
                                        r" we (do not (think|believe|see how) we (would|could)|(would|could) not) (be( feeling)*|feel) better " : " we are good "}

        self.second_level_complex_phrases_map = {
                            " i have felt " : [" i am ", [" in the past", " before"]],
                            " i have been " : [" i am ", [" in the past", " before"]],
                            " i was feeling " : [" i am ", [" in the past", " before", " a while ago", " a long time ago", " once upon a time"]],
                            " i was not feeling " : [" i am not ", [" in the past", " before", " a while ago", " a long time ago", " once upon a time"]],
                            " i felt " : [" i am ", [" in the past", " before", " a while ago", " a long time ago", " once upon a time"]],
                            " we have felt " : [" we are ", [" in the past", " before"]],
                            " we have been " : [" we are ", [" in the past", " before"]],
                            " we were feeling " : [" we are ", [" in the past", " before", " a while ago", " a long time ago", " once upon a time"]],
                            " we were not feeling " : [" we are not ", [" in the past", " before", " a while ago", " a long time ago", " once upon a time"]],
                            " we felt " : [" we are ", [" in the past", " before", " a while ago", " a long time ago", " once upon a time"]]}

        # all words denoting negative emotion
        self.all_negative_words = set(["unwell", "unhappy", "unsatisfied", "unenthused",
        r"not (feeling|doing)* so hot", "under the weather", "miserable",
        "depressed", "sad", "melancholy", "depressing", "fearful", "apprehensive", "threatening",
        "terrified", "scared", "afraid", "terrifying", "scary", "frightening", "bored", "boring",
        "anxious", "nervous", "worried", "concerned", "nerve-wracking", "worrying", "concerning",
        "angry", "mad", "enraged", "aggressive", "vengeful", "wrathful", "maddening", "enraging",
        "frustrated", "frustrating", "awful", "tired", "exhausted", "tiring", "exhausting", "stressed",
        "stressful", "disgusted", "disgusting", "awful", "ashamed", "shameful", "embarrassed",
        "humiliated", "embarrassing", "humiliating", "distracted", "distracting", "annoyed", "annoying",
        "provoked", "offended", "provocative", "offensive", "hateful", "mean", "rude", "racist", "sexist",
        "sarcastic", "abused", "abusive", "ridiculed", "teased", "mocked", "scorned", "criticized",
        "mocking", "teasing", "ridiculing", "jealous", "boastful", "disappointed", "pathetic", "lame",
        "disappointing", "regrettable", "unmotivated", "lazy", "complacent", "discouraged",
        "uninspiring", "discouraging", "terrible", "bad", "upset", "irked", "agitated", "aggravated", "livid", "creeped out",
        "sick", "sick and tired", "blue", "down", "crabby", "irritable", "touchy", "sensitive",
        "raw", "gross", "grossed out", "revolting", "revolted", "unstable", "insane", "insanity",
        "crazy", "out of my mind", "idiot", "idiotic", "stupid", "dumb", "retarded", "freak",
        "freakish", "death", "dead", "corpse", "prohibitive", "unlucky", "unimportant",
        "forgotten", "abandoned", "friendless", "suicidal", "failure", "letdown", "let down",
        "ignored", "made fun of", "pained", "in pain", "deserted", "shunned", "bleak", "lonely", "alone", "isolated"])

        # words the user will use to negatively describe their own emotions
        self.agent_descriptive_negative_words = set(["unwell", "unhappy", "unsatisfied",
        "unenthused", r"not (feeling|doing)* so hot", "under the weather",
        "miserable", "depressed", "sad", "melancholy", "fearful", "apprehensive", "terrified",
        "scared", "afraid", "bored", "boring", "anxious", "nervous", "worried",
        "concerned", "worrying", "angry", "mad", "enraged", "vengeful", "wrathful",
        "frustrated", "awful", "tired", "exhausted", "stressed", "disgusted", "disgusting",
        "awful", "ashamed", "shameful", "embarrassed", "humiliated", "embarrassing",
        "humiliating", "distracted", "distracting", "annoyed", "annoying", "provoked",
        "offended", "provocative", "offensive", "hateful", "mean", "rude", "racist",
        "sexist", "sarcastic", "abused", "abusive", "ridiculed", "teased", "mocked",
        "scorned", "criticized", "jealous", "boastful", "disappointed", "pathetic", "lame",
        "disappointing", "regrettable", "unmotivated", "lazy", "complacent", "discouraged",
        "uninspiring", "discouraging", "terrible", "bad", "upset", "irked", "agitated", "aggravated", "livid", "creeped out",
        "sick", "sick and tired", "blue", "down", "crabby", "irritable", "touchy", "sensitive",
        "raw", "gross", "grossed out", "revolting", "revolted", "unstable", "insane", "insanity",
        "crazy", "out of my mind", "idiot", "idiotic", "stupid", "dumb", "retarded", "freak",
        "freakish", "death", "dead", "corpse", "prohibitive", "unlucky", "unimportant",
        "forgotten", "abandoned", "friendless", "suicidal", "failure", "letdown", "let down",
        "ignored", "made fun of", "pained", "in pain", "deserted", "shunned", "bleak", "lonely", "alone", "isolated"])

        # all words denoting positive emotion
        self.all_positive_words = set(["alright", "well", "terrific", "on cloud nine", "wonderful",
        "awesome", "fantastic", "ecstatic", "enthusiastic", "okay", "ok", "alright", "good", "great",
        "fine", "happy", "joyful", "joyous", "excited", "thrilled", "exhilarated", "thrilling",
        "exciting", "exhilarating", "amused", "amusing", "comforted", "loved", "valued",
        "important", "comforting", "loving", "soothing", "optimistic", "relaxed",
        "relaxing", "ambitious", "motivated", "motivating",
        "poetic", "beautiful", "gorgeous", "kind", "nice", "empathetic",
        "generous", "understandable", "encouraged", "encouraging",
        "impressive", "cute", "smart", "intelligent", "accomplished",
        "successful", "clever", "creative", "uplifted", "uplifting", "witty", "funny",
        "hilarious", "entertaining", "buff", "healthy", "enjoyable", "popular", "honest",
        "respected", "respectable", "cared for", "looked after", "watched over",
        "taken care of", "charitable", "interesting", "free", "freed", "liberated",
        "grateful", "gratitude", "euphoric", "delighted", "pleased", "proud",
        "invincible", "indestructible", "unbeatable", "triumphant", "triumphantly",
        "victorious", "victoriously", "highly capable", "positive", "winner", "win",
        "supported", "supportive", "supporting", "validated", "validating", "sunny",
        "bright", "energetic", "energetically", "chipper", "fresh", "freshly",
        "renewed", "like new", "angelic", "amazing", "superb", "young", "on top",
        "better", "healed", "forgiven", "relieved", "relief", "ethereal", "elegant",
        "graceful", "strengthened", "empowered", "powerful", "valuable", "giddy",
        "adventurous", "enlightened", "curious", "inquisitive", "serene", "peaceful",
        "at peace", "comfortable", "safe", "protected", "protective", "lucky",
        "fortunate", "blessed", "rewarded", "rewarding", "recognized", "noticed",
        "enriched", "trusted", "divine", "mystified", "awed", "amazed", "fit", "satisfied", "up to it", "excellent", "fabulous", "outstanding"])

        # words the user will use to positively describe their own emotions
        self.agent_descriptive_positive_words = set(["alright", "well", "terrific", "on cloud nine",
        "wonderful", "awesome", "fantastic", "ecstatic", "enthusiastic", "okay", "ok", "alright",
        "good", "great", "fine", "happy", "joyful", "joyous", "excited", "thrilled", "exhilarated", "exciting",
        "amused", "amusing", "comforted", "loved", "valued", "important", "comforting",
        "loving", "soothing", "optimistic", "relaxed", "relaxing",
        "ambitious", "motivated", "poetic", "beautiful",
        "gorgeous", "kind", "nice", "empathetic", "generous", "encouraged",
        "encouraging", "impressive", "cute", "smart", "intelligent", "accomplished",
        "successful", "clever", "creative", "uplifted", "uplifting", "witty", "funny",
        "hilarious", "entertaining", "buff", "healthy", "enjoyable", "popular", "honest",
        "respected", "respectable", "cared for", "looked after", "watched over",
        "taken care of", "charitable", "interesting", "free", "freed", "liberated",
        "grateful", "gratitude", "euphoric", "delighted", "pleased", "proud",
        "invincible", "indestructible", "unbeatable", "triumphant",
        "victorious", "highly capable", "positive", "winner", "supported", "supportive", "validated", "sunny",
        "bright", "energetic", "chipper", "fresh", "renewed", "like new", "angelic", "amazing", "superb", "young", "on top",
        "better", "healed", "forgiven", "relieved", "relief", "ethereal", "elegant",
        "graceful", "strengthened", "empowered", "powerful", "valuable", "giddy",
        "adventurous", "enlightened", "curious", "inquisitive", "serene", "peaceful",
        "at peace", "comfortable", "safe", "protected", "protective", "lucky",
        "fortunate", "blessed", "rewarded", "rewarding", "recognized", "noticed",
        "enriched", "trusted", "divine", "mystified", "awed", "amazed", "fit", "satisfied", "up to it", "excellent", "fabulous", "outstanding"])

        # all words denoting neutral emotion
        self.all_neutral_words = set(["sarcastic", "ironic", "satirical", "exasperated", "exasperating", "ironic",
        "surprised", "surprising", "shocked", "shocking", "suspicious", "fishy",
        "philosophical", "thoughtful", "thought-provoking", "serious",
        "intrigued", "curious", "interesting", "intriguing", "amazed", "in awe",
        "amazing", "adventurous", "submissive", "humbling"])

        # words the user will use to neutrally describe their own emotions
        self.agent_descriptive_neutral_words = set(["sarcastic", "ironic", "satirical", "exasperated", "exasperating", "ironic",
        "surprised", "surprising", "shocked", "shocking", "suspicious", "fishy",
        "philosophical", "thoughtful", "thought-provoking", "serious",
        "intrigued", "curious", "interesting", "intriguing", "amazed", "in awe",
        "amazing", "adventurous", "submissive", "humbling"])

        self.uplifting_response_words = ["amazing", "loved", "valued", "important", "smart", "superb", "inspiring", "intelligent", "invincible", "unbeatable", "valuable"]

