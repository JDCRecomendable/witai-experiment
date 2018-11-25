"""
Extension of Chatbot for processing Pizza Intents
Copyright (c) 2018 Jared Daniel Carbonell Recomendable. All rights reserved.
"""

# Wit API Centric Functions
def get_pizza_type(resp):
    """Get pizza type requested by user, processed by Wit.ai. Return None if
    not indicated by Wit.ai.
    
    Parameters:
    resp -- response from Wit.ai
    """
    try:
        return resp['entities']['pizza_type'][0]['value']
    except KeyError:
        return None

# Critical Function that formulates the English statements to be returned to the
# interface
def form_response_pizza(resp):
    """Form response to output to user based on the pizza type chosen by user
    during conversation with Wit.ai. If pizza type is not clear as found by
    Wit.ai, return None.
    
    Parameters:
    resp - response from Wit.ai
    """
    pizza_type = get_pizza_type(resp)
    if pizza_type == None:
        return (1, 'What kind of pizza would you like?')
    return (0, 'You asked for a {} pizza.'.format(pizza_type))
