"""
Main Code for Chatbot and Processor for Intent
Copyright (c) 2018 Jared Daniel Carbonell Recomendable. All rights reserved.
"""

# Pre-Requisites
from datetime import datetime
from wit import Wit # documentation at https://github.com/wit-ai/pywit
from random import randrange
import _weather
import _pizza
import _greetings
import _thanks
import __time
bot = Wit('R2T4LVWXEBS2IUJB73DKIZHYFVSK6CVL')
## Yes I know. I totally got rid of the API key.

# Wit API Centric Functions
def get_intent(resp):
    """Return the intent. If no intent is found, returns None.
    
    Parameters:
    resp -- response from Wit.ai
    """
    try:
        return resp['entities']['intent'][0]['value']
    except KeyError:
        return None

def get_entities(resp):
    """Return the list of entities from the response from Wit.ai.
    
    Parameters:
    resp -- response from Wit.ai
    """
    return list(resp['entities'].keys())

# Error Handler Functions to handle errors resulting from inputs with
# apostrophes and/or quotation marks
def replace_char(st, o, n):
    """Modify the string, replacing the instances of the character(s) in o with
    that of the character(s) in n.
    
    Parameters:
    st -- string to modify
    o  -- old characters in the string to remove
    n  -- new characters to replace the removed characters in the string
    """
    end = ''
    tem = st.split(o)
    for i in range(len(tem)):
        if i == len(tem) - 1:
            end += tem[i]
            break
        end += tem[i] + n
    return end

def remove_quotes(st):
    """Remove the apostrophes and/or quotation marks in the inputted string.
    
    Parameters:
    st -- string whose apostrophes will be removed
    """
    st = replace_char(st, '\'', '"')
    st = replace_char(st, '"', '')
    return st

# Logging Functions to help with debugging
def write_to_log(to_log):
    """Log the datetime in which the response was given and the response itself,
    separated by a newline. Then insert two newlines after the response.
    
    Parameter:
    to_log -- the string to append to the log
    """
    f = open(file='log.txt', mode='a+')
    now = __time.get_dt_now()
    f.write('{}\n{}\n\n'.format(now, to_log))
    f.close()

# Critical Function that facilitates communication between interface and the
# rest of the chatbot functions
def chat(inp):
    """Get user's input, then process user's input using Wit.ai to achieve the
    intended response from the chatbot.
    
    Parameters:
    inp -- user's input
    """
    inp = remove_quotes(inp)
    resp = bot.message(inp)
    write_to_log(resp)
    to_say = form_response(resp)
    return to_say

# Critical Function that formulates the English statements to be returned to the
# interface
def form_response(resp):
    """Form the response to output to the user based on response from Wit.ai.
    
    Parameter:
    resp -- response from Wit.ai
    """
    intent = get_intent(resp)
    if intent == 'pizza':
        _weather.clear_all_context()
        change_last_intent(intent)
        response = _pizza.form_response_pizza(resp)
        if response[0] == 1:
            context_misunderstood(intent)
        return response[1]
    if intent == 'weather':
        change_last_intent(intent)
        response = _weather.form_response_weather(resp)
        return response[1]
    if intent == None:
        if ('pizza_type' in get_entities(resp)) and (get_context_in_question() == 'pizza'):
            _weather.clear_all_context()
            change_last_intent(get_context_in_question())
            context_understood()
            response = _pizza.form_response_pizza(resp)
            if response[0] == 1:
                context_misunderstood(intent)
            return response[1]
        if (get_last_intent() == 'weather') and (('datetime' in get_entities(resp)) or ('location' in get_entities(resp))):
            change_last_intent('weather')
            context_understood()
            response = _weather.form_response_weather(resp)
            return response[1]
        if 'greetings' in get_entities(resp):
            return _greetings.form_response_greetings()[1]
        if 'thanks' in get_entities(resp):
            return _thanks.form_response_thanks()[1]
        context_understood()
        return message_intent_misunderstood()

# Misunderstanding Elements
context_in_question = []
last_intent = []

# Misunderstanding Handler
def message_intent_misunderstood():
    """Ask the user to repeat his/her input if chatbot misunderstands intent of
    the earlier input.
    """
    digit = randrange(3)
    if digit == 0:
        return 'Sorry, I did not get you. Can you please repeat?'
    elif digit == 1:
        return 'Sorry, I couldn\'t understand you? Can you please come again?'
    else:
        return 'I\'m sorry, I did not read you. Can you please come again?'

def context_misunderstood(context):
    """Store the context of current conversation to context_in_question.
    
    Parameter:
    context -- context of current conversation to put into context_in_question
    """
    context_in_question.append(context)

def get_context_in_question():
    """Get the latest context in question. If not available, return None."""
    if len(context_in_question) == 0:
        return None
    return context_in_question[len(context_in_question) - 1]

def context_understood():
    """Clear the context in question."""
    context_in_question.clear()

def get_last_intent():
    """Get the last intent used. If not available, return None."""
    if len(last_intent) == 0:
        return None
    return last_intent[len(last_intent) - 1]

def change_last_intent(intent):
    """Update the intent in last_intent based on new intent of ongoing
    conversation.
    
    Parameters:
    intent -- intent of current conversation, to replace the one in last_intent
    """
    last_intent.clear()
    last_intent.append(intent)

def clear_last_intent():
    """Clear the last intent."""
    last_intent.clear()
