'''
Extension of Chatbot for processing Thanks
Copyright (c) 2018 Jared Daniel Carbonell Recomendable. All rights reserved.
'''

from random import randrange

def form_response_thanks():
    '''Responds to user's gratitude.'''
    digit = randrange(3)
    if digit == 0:
        string = 'My pleasure to serve you.'
    elif digit == 1:
        string = 'It is my duty.'
    else:
        string = 'I should thank you for helping me build my (artificial) intelligence.'
    return 0, string
