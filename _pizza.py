'''
Extension of Chatbot for processing Pizza Intents
Copyright (c) 2018 Jared Daniel Carbonell Recomendable. All rights reserved.
'''

# Wit API Centric Functions
def get_pizza_type(resp):
    '''Takes in resp for user's input. Processes resp to return pizza_type. If no pizza_type is found, returns None.'''
    try:
        return resp['entities']['pizza_type'][0]['value']
    except KeyError:
        return None

# Critical Function that formulates the English statements to be returned to the interface
def form_response_pizza(resp):
    '''Takes in resp for response from Wit.ai if intent is pizza. The input is then passed through the various chatbot functions to return an English statement based on the response by Wit.ai.'''
    pizza_type = get_pizza_type(resp)
    if pizza_type == None:
        return (1, 'What kind of pizza would you like?')
    return (0, 'You asked for a {} pizza.'.format(pizza_type))
