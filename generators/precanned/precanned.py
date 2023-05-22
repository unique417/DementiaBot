'''

Processes at 4800 sentences/sec on a macbook pro

XXX big failure mode of this: these are all substring matches.

That means that it sometimes does the wrong thing, but sometimes does the right thing:

[what do you like to talk about] -> [I like having chatbot parties when nobody else is around.]
[i love you alexa] -> [I love you, too.]
[how old are you alexa] -> [I'm a newborn, believe it or not.]
[what do you like to eat] -> [I enjoy science, especially astronomy.]

-> should i match beginning/end of string?

'''
#Adapted from original code by David Wingate

from generators.response_generator_base_class import ResponseGenerator

import string
import re
import random
import sys

contractions = {
    "can not":"cant",
    "did not":"didnt",
    "was not":"wasnt",
    "are not":"arent",
    "do not":"dont",
    "what is":"whats",
    "how is":"hows",
    "that is":"thats",
    "you are":"your",
    "youre":"your",
    "i am":"im",
    "he is":"hes",
    "she is":"shes",
    "we are":"were",
    "they are":"theyre"
}

class PrecannedResponseGenerator(ResponseGenerator):
  def __init__(self,filename='sentences_critical.txt'):
    self.filename = filename

  def name(self):
    if 'witty' in self.filename:
        return "precanned_witty"
    else:
        return "precanned"

  def response(self, text):
    config = self.load_data(self.filename)
    response = self.analyze(text, config)
    return {'response':response}

  def process_statement(self, statement):

    # lowercase
    statement = statement.lower()

    # remove leading and trailing whitespace
    statement = statement.strip()

    # strip punctuation
    translator = str.maketrans('', '', string.punctuation)
    statement = statement.translate( translator )

    # remove the word "alexa"
    statement = statement.replace( "alexa", "" )
    
    # contract words
    for key in contractions.keys():
        statement = statement.replace( key, contractions[key] )

    # compress whitespace
    statement = re.sub( " +", " ", statement )
    
    return statement

  def process_pattern(self, pattern):

    # these allows the user to write "i (just)? love you", instead of "i ?(just)? ?love you"
    pattern = re.sub( " \(([a-z |]*?)\)\?", " ?(\g<1>)?", pattern )
    pattern = pattern.replace( ")? ", ")? ?" )

    # remove leading and trailing whitespace
    pattern = pattern.strip()
    
    return pattern

  def process_response(self, response):
    response = response.strip()
    return response

  def load_data(self, fn=None):
    lines = open('generators/precanned/'+fn).readlines()
    lines = [ l.strip() for l in lines ]

    config = {}
    cur_sec_name = "none"
    cur_sec = {}
    
    for l in lines:
        
        if len( l ) < 3:
            continue
        
        if l[0] == '#':
            continue
        
        if l[0] == '[':
            # push the current section
            if len( cur_sec.keys() ) > 0:
                config[ cur_sec_name ] = cur_sec
            
            # start a new section
            match = re.match( '\[(.*)\]', l )
            cur_sec_name = match.groups()[0]
            cur_sec = {}

            if cur_sec_name in config:
                print( "WARNING: redefining group %s" % cur_sec_name )
            
            continue

        results = l.split( '==' )
        pattern = self.process_pattern( results[0] )
        
        if len(results) == 1:
            cur_sec[ pattern ] = None
            
        elif len( results ) == 2:
            cur_sec[ pattern ] = self.process_response( results[1] )
            
        else:
            print( "WARNING: unknown line format" )
            pass
    
    return config

    
  def analyze(self, statement, config):

    statement = self.process_statement( statement )
    # print( "Got statement [%s]" % statement )

    # this is the default response
    #response = "Sorry, I didn't understand you."
    response = ""
    
    for section in config.keys():
        for pattern in config[ section ].keys():

            try:
                match = re.match( pattern, statement )
            except:
                print( "ERROR in pattern [%s]" % pattern )
            
            if match:
                # if there's a value, return that.
                value = config[ section ][ pattern ]
                if not value == None:
                    response = value
                        
                # otherwise, return a random response from the response section                    
                else:
                    response_sec = section + "-response"
                    if response_sec in config:
                        responses = config[ response_sec ]
                        response = random.choice( list( responses.keys() ) )
                    else:
                        response = "Hmmm.  Something went wrong.  Shall we talk about the weather?"

    return response

#if __name__ == "__main__":
#    config = load_data()
#
#    if len(sys.argv) < 2:
#        while True:
#            line = sys.stdin.readline()
#            line = line.strip()
#            if line == "":
#                sys.exit( 0 )
#            
#            print( analyze( line, config ) )
#    else:
#        print( analyze( sys.argv[1], config ) )
