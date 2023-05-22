from datetime import datetime # Just for debugging

group = input('Which group are you in? (A or B) ')
while group not in ['A', 'B']:
    group = input('Invalid group, please enter A or B: ')

from app2 import chat_function

session_key = datetime.now().strftime('%m_%d_%H_%M')

if group == 'A':
    chat_function(True, 1, session_key + '_A1')
    chat_function(False, 2, session_key + '_A2')
else:
    chat_function(False, 1, session_key + '_B1')
    chat_function(True, 2, session_key + '_B2')
