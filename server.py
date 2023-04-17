#!python -u

import sys, os, time
from flask import Flask, request
from subprocess import Popen, PIPE
from slugify import slugify
from threading import Thread

f = Flask(__name__)

# global, mutable
queued = set()

@f.route('/', methods=['POST'])
def index():
    items = request.get_json()
    download(items)

    return 'ok'

def get_steam_workshop_process():
    return Popen(['steamcmd', '+login anonymous'], stdin=PIPE, stderr=PIPE)

def download(items):
    for item in items:
        game_id = item["app_id"]
        mod_id = item["id"]
        mod_name = item['name']

        cmd = f'workshop_download_item {game_id} {mod_id}\n'.encode('utf-8')
        steam.stdin.write(cmd)
        # force write
        steam.stdin.flush()

        # keep for renaming later
        queued.add((game_id, mod_id, mod_name))

def watch_dir(abs_path, queued):
    while 1:
        # todo: still too cpu heavy. need some watchdog
        time.sleep(1)
        renamed = set()
        for q in queued:
            game_id, id, name = q
            slug = slugify(name)
            game_dir = os.path.join(abs_path, game_id, '')
            raw_mod_dir = os.path.join(game_dir, id, '')
            pretty_mod_dir = os.path.join(game_dir, slug, '')
            print(f'gonna rename {id} to {slug}')
            try:
                os.rename(raw_mod_dir, pretty_mod_dir)
                renamed.add(q)
            except OSError as e:
                # todo: handle stuck mods, n retries?
                repr(e)
        queued.difference_update(renamed)

if __name__ == '__main__':
    steam_path = sys.argv[1]
    if not steam_path:
        raise Exception('no path')
    # will despawn on exit hopefully
    Thread(target=watch_dir, args=[steam_path, queued]).start()
    steam = get_steam_workshop_process()
    f.run(debug=True)
    # no zombies
    steam.communicate(b'quit\n')
