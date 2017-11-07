import sys
import os
import hashlib
import requests

media_extension = ['mp4', 'mkv', 'avi', 'mpg', 'mov', 'm4v']

def get_hash(name):
    readsize = 64 * 1024
    with open(name, 'r+b') as f:
        size = os.path.getsize(name)
        data = f.read(readsize)
        f.seek(-readsize, os.SEEK_END)
        data += f.read(readsize)
    return hashlib.md5(data).hexdigest()


def make_request(hash):
    url = 'http://api.thesubdb.com/?action=download&hash={}&language=en'.format(hash)
    headers = {'User-agent': 'SubDB/1.0 (SubTank/0.1; http://github.com/CHURLZ/subtank)'}
    response = requests.get(url, headers=headers)
    return response if response.status_code == 200 else None


def download_sub(file_name):
    response = make_request(get_hash(file_name))
    if not response:
        print('### ERROR downloading subs for\n\t{}'.format(file_name))
        return False
    write_sub_to_file(file_name, response.content)
    return True


def write_sub_to_file(file_name, byte_data):
    sub_file_name = '{}.srt'.format('.'.join(file_name.split('.')[:-1]))
    print('printing sub to file: {}'.format(sub_file_name))
    with open(sub_file_name, 'wb') as f:
        f.write(byte_data)


def rq(f):
    print('### ERROR file not found!\n\t{}'.format(f))
    sys.exit()

downloads = 0
if len(sys.argv) < 2:
    for f in os.listdir():
        if f.split('.')[-1] in media_extension:
            downloads += 1 if download_sub(f) else 0
else:
    f = sys.argv[1]
    rq(f) if f not in os.listdir() else download_sub(f)

print('{} subs downloaded in folder {}.'.format(downloads, os.getcwd()))
