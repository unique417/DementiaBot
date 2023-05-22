from appJar import gui
import os
from time import sleep
from concurrent.futures import ThreadPoolExecutor
import sys
from conversation_engine import conversation_engine
#from emotion_detector import Emotion
from personality_questions import MBTIClassifier
#from stanford_triple_extraction import StanfordOpenIEWrapper
from similarities import Similarity
from yes_no import Yes_no
from knowledgegraph import KnowledgeGraph
#import chat

#emotion= Emotion()

conversation_lst = []
ce = conversation_engine()
mbti= MBTIClassifier()
#stanford_triple_extractor = StanfordOpenIEWrapper()
sim= Similarity()
kg=KnowledgeGraph()
ynclassifier = Yes_no()
start = ce.start()
start_sent=start
flag=0
personality=[" - "," - "," - "," - "]
done=False
n=2
r=2
count=0

story_controller = None
selected_setting = ''
selected_genre = ''

def chat_function(baseline_mode, version_number, game_id):
    global story_controller
    global selected_setting
    global selected_genre
    os.mkdir(f'logs/{game_id}')
    #os.mkdir(f'logs/knowledge-graph/{game_id}')
    selected_setting = ''
    selected_genre = ''

    app = gui()

    app.setTitle(f'DementiaBot')
    app.setIcon('icon.png')

    app.addLabel('title', 'Welcome to this chatbot!')
    app.setLabelPadding('title', x=5, y=20)
    app.getLabelWidget('title').config(font='Verdana 16 bold')
    app.setBg('#f1f5eb', override=True, tint='#99f7a9')
    app.setGuiPadding(54, 54)

    parallel_executor = ThreadPoolExecutor(max_workers=1)

    def introduction_screen():
        def proceed(_):
            app.removeLabel('intro_label_1')
            app.removeLabel('intro_label_2')
            app.removeLabel('intro_label_3')
            app.removeLabel('intro_label_4')
            app.removeButton('proceed')
            chat_screen()


        app.addLabel('intro_label_1', text = 'This chatbot tries to know you better and find your personality type! ')
        app.addLabel('intro_label_2', text='It will ask you questions about, and uses your respond to modify its future responses based on what it learned about you.')
        app.addLabel('intro_label_3', text=' your conversation can be short or as long as you enjoy it.')
        app.addLabel('intro_label_4', text=' This chatbot has been developed to help caregivers of people with dementia, but you do not need to be a caregiver :)')
        for i in range(1, 5):
            app.setLabelPadding(f'intro_label_{i}', 10, 20)
            app.getLabelWidget(f'intro_label_{i}').config(font='Verdana 14')

        app.addButton('proceed', proceed)
        app.setButton('proceed', 'Continue')
        app.setButtonRelief('proceed', 'groove')
        app.setButtonBg('proceed', '#8099ff')
        app.setButtonActiveBg('proceed', '#a6b8ff')
        app.setButtonWidth('proceed', 12)


    def chat_screen():

        def finish_chat(button_id):
            app.stop()

        def respond(new_message):
            global flag
            global personality
            global done

            text = new_message
            #print("FLAG = *******************************" ,flag)
            if flag != 0:
                #check if the response is yes or no.
                yn=ynclassifier.classifier(text)
                #print("yn = *******************************" ,yn)

                #send the yes or no response and flag to mbti.personality_classifier
                personality,done =ce.personality_classifier(yn,flag)
                flag=0

            q,flag=ce.flag(text)
            #print("question= ",q)
            print("User's personality so far :", personality)
            if done== True:
                kg.add_personality(personality)
        #    mo= emotion.get_emotion(text)
            #print('here')
            response = ce.chat(text,q, verbose=True)
            #print('now here')
            response = ce.sentences(response,personality)
            #print("response after sentence",response)
            return response

        def baseline_respond(new_message):

            text = new_message
            q = None
            response = ce.chat(text,q, verbose=True)
            print(response)
            return response

        def compose_response(new_message):
            global r
            if baseline_mode:
                response_paragraph = respond(new_message)
            else:
                response_paragraph = baseline_respond(new_message)

            save_as_txt(new_message,response_paragraph)
            if response_paragraph == -1:
                response_paragraph = '[Error: The AI failed to compose a valid response.]\n[You may write another paragraph or exit the chat.]'
            app.openScrollPane('DementiaBot')
            app.addMessage(f'r{n}', response_paragraph)
            app.setMessageWidth( f'r{n}',600)
            app.setMessageAnchor(f'r{n}', 'left')
            app.stopScrollPane()
            app.enableButton('submit_text')
            app.setButton('submit_text', 'Submit')
            app.setButtonBg('submit_text', '#8099ff')

        def submit_user_text(button_id):
            global n

            new_message = app.getTextArea('text_entry')
            if len(new_message) > 0:
                app.openScrollPane('DementiaBot')
                #app.addMessage(f'p{story_controller.get_story_length()}', new_message)
                app.addMessage(f'p{n}', new_message)
                app.setMessageWidth(f'p{n}', 600)
                app.setMessageAnchor(f'p{n}', 'right')
                n +=1
                app.stopScrollPane()
                app.clearTextArea('text_entry')
                app.disableButton('submit_text')
                app.setButtonBg('submit_text', '#8cddff')
                app.setButton('submit_text', 'Loading response...')
                parallel_executor.submit(compose_response, new_message)

        def save_as_txt(new_message,response):
            global conversation_lst
            conversation_lst.append(new_message)
            conversation_lst.append(response)
            with open(f'logs/{game_id}/story.txt', 'w') as out_file:
                out_file.write(str(conversation_lst))
                #out_file.write(new_message)
                #out_file.write('\n')
                #out_file.write(response)


        app.removeLabel('title')
        #print('Selected genre:', selected_genre)
        #if os.path.exists(f'prompts/{selected_setting}_{selected_genre}.txt'):
        #    with open(f'prompts/{selected_setting}_{selected_genre}.txt') as in_file:
        #        initial_message = in_file.read()
        #else:
        #    print(f'prompts/{selected_setting}_{selected_genre}.txt')
        initial_message = start_sent

        app.startScrollPane('DementiaBot')
        app.addMessage('p0', initial_message)
        app.setMessageWidth('p0', 800)
        app.setMessageAnchor('p0', 'left')
        app.setFont(size=16, family="Times", underline=False)
        app.stopScrollPane()

        app.addTextArea('text_entry')

        app.setTextAreaWidth('text_entry', 40)

        app.addMessage('spacer', ' ')

        app.addButtons(['submit_text', 'finish_chat'], [submit_user_text, finish_chat])
        for btn_id, btn_label, btn_colors in zip(['submit_text', 'finish_chat'], ['Submit', 'Finish'], [('#8099ff', '#a6b8ff'), ('#ffa7a1', '#f7d0cd')]):
            app.setButton(btn_id, btn_label)
            app.setButtonPadding(btn_id, 16, 5)
            app.setButtonRelief(btn_id, 'groove')
            app.setButtonBg(btn_id, btn_colors[0])
            app.setButtonActiveBg(btn_id, btn_colors[1])

    introduction_screen()

    app.go()
    #del story_controller
