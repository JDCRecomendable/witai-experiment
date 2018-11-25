"""
Extension of Chatbot for processing Greetings
Copyright (c) 2018 Jared Daniel Carbonell Recomendable. All rights reserved.
"""

from random import randrange

def form_response_greetings():
    """Say hello to the user."""
    digit = randrange(3)
    if digit == 0:
        return 0, 'Hi!'
    elif digit == 1:
        return 0, 'Hello!'
    else:
        return 0, 'Greetings!'
