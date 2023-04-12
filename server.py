#!python

from flask import Flask, request
from subprocess import Popen, PIPE

f = Flask(__name__)

@f.route('/', methods=['POST'])
def index():
    items = request.get_json()
    run_script(items)

    return 'ok'

def get_steam_workshop_process():
    return Popen(['steamcmd', '+login anonymous'], stdin=PIPE)

def run_script(items):
    for item in items:
        cmd = f'workshop_download_item 552100 {item["id"]}\n'.encode('utf-8')
        print(item)
        steam.stdin.write(cmd)
        steam.stdin.flush()

if __name__ == '__main__':
    steam = get_steam_workshop_process()
    f.run(debug=True)
    steam.communicate(b'quit\n')
