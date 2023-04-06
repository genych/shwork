#!python

from flask import Flask, request
from subprocess import Popen

f = Flask(__name__)

@f.route('/', methods=['POST'])
def index():
    items = request.get_json()
    import pdb; pdb.set_trace()  # breakpoint 9f0d7010 //
    run_script(items)

    return 'ok'

def run_script(items):
    head = '+login anonymous'
    quit = '+quit'
    commands = [f'+workshop_download_item 552100 {item["id"]}' for item in items]

    Popen(['steamcmd', head, *commands, quit])

if __name__ == '__main__':
    f.run(debug=True)
