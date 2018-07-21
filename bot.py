'''
Main Code for Chatbot and Processor for Intent
Copyright (c) 2018 Jared Daniel Carbonell Recomendable. All rights reserved.
'''

# Pre-Requisites
from datetime import datetime
from wit import Wit # documentation at https://github.com/wit-ai/pywit
from random import randrange
import _weather
import _pizza
import _greetings
import _thanks
import __time
bot = Wit('R2T4LVWXEBS2IUJB73DKIZHYFVSK6CVL')  ## I totally accidentally left my API key here.

# Wit API Centric Functions
def get_intent(resp):
    '''Takes in resp for user's input. Processes resp to return the intent. If no intent is found, returns None.'''
    try:
        return resp['entities']['intent'][0]['value']
    except KeyError:
        return None

def get_entities(resp):
    '''Takes in resp for the response from Wit.ai. Processes resp to return the list of entities from the response from Wit.ai.'''
    return list(resp['entities'].keys())

# Error Handler Functions to handle errors resulting from inputs with apostrophes and/or quotation marks
def replace_char(st, o, n):
    '''Takes in st for string, o for character(s) to be replaced, and n for character(s) to replace o. Processes the string such that o is replaced by n in the string.'''
    end = ''
    tem = st.split(o)
    for i in range(len(tem)):
        if i == len(tem) - 1:
            end += tem[i]
            break
        end += tem[i] + n
    return end

def remove_quotes(st):
    '''Takes in st for string. Removes the apostrophes and/or quotation marks in an inputted string.'''
    st = replace_char(st, '\'', '"')
    st = replace_char(st, '"', '')
    return st

# Logging Functions to help with debugging
def write_to_log(to_log):
    '''Takes in to_log for response of the chatbot. Logs the datetime in which the response was given and the response itself, separated by a newline. Then inserts two newlines after the response.'''
    f = open(file='log.txt', mode='a+')
    now = __time.get_dt_now()
    f.write('{}\n{}\n\n'.format(now, to_log))
    f.close()

# Critical Function that facilitates communication between interface and the rest of the chatbot functions
def chat(inp):
    '''Takes in inp for user's input from the interface. The input is then passed through the various chatbot functions to remove apostrophes and quotation marks from the input to prevent error then to get the response from Wit.ai, which is logged. Then the response from Wit.ai is further processed by other functions to return a polished response to the user in English.'''
    inp = remove_quotes(inp)
    resp = bot.message(inp)
    write_to_log(resp)
    to_say = form_response(resp)
    return to_say

# Critical Function that formulates the English statements to be returned to the interface
def form_response(resp):
    '''Takes in resp for response from Wit.ai. The input is then passed through the various chatbot functions to return an English statement based on the response by Wit.ai.
    \nNote that the responses returned by form_response_(intent) is a tuple with two elements.
    \nThe first element returned is a status number, used for context. 0 means that the context is correctly understood. 1 means that the context is misunderstood, and necessary misunderstanding handler functions must be invoked to understand the context fully.
    \nThe second element returned is the text to be put up in the chatbot as a response by the chatbot.'''
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
    '''Asks the user to repeat his/her input if chatbot misunderstands intent of the earlier input.'''
    digit = randrange(3)
    if digit == 0:
        return 'Sorry, I did not get you. Can you please repeat?'
    elif digit == 1:
        return 'Sorry, I couldn\'t understand you? Can you please come again?'
    else:
        return 'I\'m sorry, I did not read you. Can you please come again?'

def context_misunderstood(context):
    '''Takes in the context for context in question. Appends the context to the context in question.'''
    context_in_question.append(context)

def get_context_in_question():
    '''Gets the latest context in question.'''
    if len(context_in_question) == 0:
        return None
    return context_in_question[len(context_in_question) - 1]

def context_understood():
    '''Clears the context in question.'''
    context_in_question.clear()

def get_last_intent():
    '''Gets the last intent used.'''
    if len(last_intent) == 0:
        return None
    return last_intent[len(last_intent) - 1]

def change_last_intent(intent):
    '''Takes in intent for the latest intent used. Clears the last_intent then appends intent to last_intent.'''
    last_intent.clear()
    last_intent.append(intent)

def clear_last_intent():
    '''Clears the last intent.'''
    last_intent.clear()
