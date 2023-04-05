#!python

from flask import Flask, request
from subprocess import Popen

f = Flask(__name__)

@f.route('/', methods=['POST'])
def index():
    ids = request.get_json()
    run_script(ids)

    return 'ok'

def run_script(ids):
    head = '+login anonymous'
    quit = '+quit'
    commands = [f'+workshop_download_item 552100 {id}' for id in ids]

    Popen(['steamcmd', head, *commands, quit])

if __name__ == '__main__':
    f.run(debug=True)
