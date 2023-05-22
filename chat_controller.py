import json

from .filter_triples import filter_triples
from .format_triples import format_triples_basic
from .knowledge_graph import KnowledgeGraph
from .story_generator import StoryGenerator, DummyStoryGenerator
from .triple_extractor import StanfordOpenIEWrapper
from .triple_selector import SemanticTripleSelector


class DummyStoryController:
    '''
    This class is just for debugging
    '''
    def __init__(self, baseline_mode=False, game_id='null_id'):
        self.story_paragraphs = []

    def get_story_length(self):
        return len(self.story_paragraphs)

    def set_initial_seed(self, seed_paragraph):
        self.recall_text(seed_paragraph)

    def respond(self, user_paragraph):
        self.recall_text(user_paragraph)
        new_message = '[GPT-2 Response Goes Here]'
        self.recall_text(new_message)
        return new_message

    def recall_text(self, paragraph):
        self.story_paragraphs.append(paragraph)



class StoryController:
    def __init__(self, baseline_mode=False, game_id='null_id'):
        self.story_paragraphs = []
        # self.story_generator = DummyStoryGenerator('gpt2-xl')
        self.story_generator = StoryGenerator('gpt2') # FIXME use gpt2-xl
        self.baseline_mode = baseline_mode
        self.kg = KnowledgeGraph()
        self.triple_extractor = StanfordOpenIEWrapper()
        self.triple_selector = SemanticTripleSelector()
        self.num_error_responses = 0
        self.game_id = game_id

    def get_story_length(self):
        return len(self.story_paragraphs) + self.num_error_responses

    def add_error_count(self):
        self.num_error_responses += 1

    def set_initial_seed(self, seed_paragraph):
        if len(self.story_paragraphs) > 0:
            print('Error, attempted to set an initial seed when there were already paragraphs stored')
            self.story_paragraphs = []
        if len(self.kg.triples) > 0:
            print('Error, attempted to set an initial seed when there were already knowledge graph facts stored')
            self.kg.triples = []
        self.recall_text(seed_paragraph)

    def respond(self, user_paragraph):
        self.recall_text(user_paragraph)
        relevant_triples = self.triple_selector.select(self.kg.triples, user_paragraph)
        with open(f'logs/knowledge-graph/{self.game_id}/retrieval.jsonl', 'a') as out_file:
            json.dump({'text': user_paragraph, 'selected': [list(trip) for trip, score in relevant_triples.items()], 'options': self.kg.triples}, out_file)
            print(file=out_file)
        formatted_triples = format_triples_basic(relevant_triples)
        useful_info = '\n'.join(formatted_triples)
        if self.baseline_mode:
            useful_info = ''
        have_valid_response = False
        num_attempts = 0
        while not have_valid_response:
            if num_attempts >= 3:
                print('Error, language model failed to compose valid response. Alerting user.')
                return -1
            next_paragraph = self.story_generator.generate_more_story(useful_info=useful_info, story_context='\n'.join(self.story_paragraphs[:-1]), last_paragraph=user_paragraph)
            num_attempts += 1
            if self.story_generator.format_text(user_paragraph) not in next_paragraph:
                print('Error, malformed LM response, attempting again...')
                continue
            next_paragraph = next_paragraph.split(self.story_generator.format_text(user_paragraph))[1].strip().split('\n')[0].strip()
            if len(next_paragraph) > 20:
                have_valid_response = True
            else:
                print('Error, empty LM response, attempting again...')
        self.recall_text(next_paragraph)
        return next_paragraph

    def recall_text(self, paragraph):
        extracted_triples = self.triple_extractor.extract_triples(paragraph)
        filtered_triples = filter_triples(extracted_triples)
        with open(f'logs/knowledge-graph/{self.game_id}/extractions.jsonl', 'a') as out_file:
            json.dump({'text': paragraph, 'all-triples': extracted_triples, 'good-triples': filtered_triples}, out_file)
            print(file=out_file)
        self.kg.add_edges(filtered_triples)
        self.story_paragraphs.append(paragraph)
        with open(f'logs/game-text/{self.game_id}/story.txt', 'w') as out_file:
            for paragraph in self.story_paragraphs:
                print(paragraph.strip(), file=out_file)
        with open(f'logs/game-text/{self.game_id}/story.json', 'w') as out_file:
            json.dump(self.story_paragraphs, out_file)
