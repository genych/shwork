#!python

import sys, os, subprocess
from flask import Flask, request
from slugify import slugify

f = Flask(__name__)

@f.route('/', methods=['POST'])
def index():
    items = request.get_json()
    download(items)

    return 'ok'

def download(items):
    for item in items:
        game_id = item["app_id"]
        mod_id = item["id"]
        mod_name = item['name']

        subprocess.run([
            'steamcmd',
            '+login anonymous',
            f'+workshop_download_item {game_id} {mod_id}',
            '+quit'
        ])

        rename(game_id, mod_id, mod_name)

def rename(game_id, mod_id, mod_name):
    slug = slugify(mod_name)

    game_dir = os.path.join(steam_path, game_id, '')
    raw_mod_dir = os.path.join(game_dir, mod_id, '')
    pretty_mod_dir = os.path.join(game_dir, slug, '')
    print(f'gonna rename {mod_id} to {slug}')
    os.rename(raw_mod_dir, pretty_mod_dir)

if __name__ == '__main__':
    steam_path = sys.argv[1]
    if not steam_path:
        raise Exception('no path')
    f.run(debug=True)
