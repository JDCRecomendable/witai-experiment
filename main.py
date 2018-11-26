"""
ChatBot Sample
Version 0.2
Copyright (c) 2018 Jared Daniel Carbonell Recomendable. All rights reserved.

CODE QUALITY AND PROGRAM LONGEVITY
To ensure that this program remains maintainable in the long run and easily
extensible, the files are organised like so:
    BASIC COMPONENTS:
    main.py -- the file that the user should only ever touch
            -- deals with the Flask micro web framework
    bot.py  -- the main logic of the program
    
    EXTENSION COMPONENTS:
    (extensions provide the behaviour for the chatbot, note that upon adding an
    extension, this has to be included in bot.py so that the chatbot can use it)
    _greetings.py -- behaviour for responding to "Hello"s and "Hi"s
    _thanks.py    -- behaviour for responding to gratitude
    _pizza.py     -- enable the chatbot to get the user's favourite flavour of
                     pizza
    _weather.py   -- enable the chatbot to return the weather status for a
                     location as queried by the user
"""
code_title = 'Chatbot'
code_version = '0.2'
code_manufacturer = 'Jared Daniel Carbonell Recomendable'

import bot

# Initiate the Command-Line Interface
def interact():
    """Start the commandline interface for this program."""
    while True:
        inp = input('Talk to me > ')
        if inp in ['exit', 'quit', 'bye', 'goodbye']:
            print('Goodbye!\n')
            break
        resp = bot.chat(inp)
        print(resp, end='\n\n')

# Initiate the Web Interface
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

msgs = [
    ['special', 'Weather Chatbot (Sample) by {}.'.format(code_manufacturer)],
    ['to-user', 'Type in your message in the box below. Press SEND or hit ENTER or RETURN when done.'],
    ['to-user', 'Alternatively, you may speak, using the microphone button.']
]

@app.route('/', methods=['GET', 'POST'])
def index():
    """Create the base for the web interface."""
    if request.method == 'GET':
        return show_page(msgs)
    text = request.form['user-text']
    msgs.append(['from-user', text])
    return get_response(text)

def show_page(msgs):
    """Render the page."""
    return render_template('index.html', msgs=msgs[::-1], code_title=code_title, code_version=code_version, code_manufacturer=code_manufacturer)

def web_interface():
    """Start the web interface."""
    app.run(debug=True, host='0.0.0.0', port=5000)

def get_response(inp):
    """Get the response from the chatbot."""
    resp = bot.chat(inp)
    msgs.append(['to-user', resp])
    return show_page(msgs)

if __name__ == '__main__':
    print('{}\nVersion {}\nCopyright (c) 2018 {}. All rights reserved.\n'.format(code_title, code_version, code_manufacturer))
    #interact() ## Launch Commandline Interface
    web_interface() ## Launch Web Interface
