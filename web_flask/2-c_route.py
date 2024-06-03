#!/usr/bin/python3
"""Starts a flask web application
/ displays sth and  /hbnb displays also"""

from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """ Displays Hello HBNB!"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def display_hbnb():
    """ Displays 'HBNB'"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """Displays 'c' followed by the value of <text>"""
    text = text.replace('_', ' ')
    return "c {}".format(text)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
