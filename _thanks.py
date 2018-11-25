"""
Extension of Chatbot for processing Thanks
Copyright (c) 2018 Jared Daniel Carbonell Recomendable. All rights reserved.
"""

from random import randrange

def form_response_thanks():
    """Respond to user's gratitude."""
    digit = randrange(3)
    if digit == 0:
        return 0, 'My pleasure to serve you.'
    elif digit == 1:
        return 0, 'It is my duty.'
    else:
        return 0, 'I should thank you for helping me build my (artificial) intelligence.'
