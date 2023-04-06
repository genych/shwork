#!python

from flask import Flask, request
from subprocess import call

f = Flask(__name__)

@f.route('/', methods=['POST'])
def index():
    items = request.get_json()
    run_script(items)

    return 'ok'

def run_script(items):
    head = '+login anonymous'
    quit = '+quit'
    commands = [f'+workshop_download_item 552100 {item["id"]}' for item in items]

    call(['steamcmd', head, *commands, quit])
    print('done')

if __name__ == '__main__':
    f.run(debug=True)
