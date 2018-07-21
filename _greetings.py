'''
Extension of Chatbot for processing Greetings
Copyright (c) 2018 Jared Daniel Carbonell Recomendable. All rights reserved.
'''

from random import randrange

def form_response_greetings():
    '''Says hello to the user.'''
    digit = randrange(3)
    if digit == 0:
        string = 'Hi!'
    elif digit == 1:
        string = 'Hello!'
    else:
        string = 'Greetings!'
    return 0, string
