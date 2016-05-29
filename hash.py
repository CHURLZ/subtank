import sys,os,hashlib
import urllib2

def get_hash(name):
    readsize = 64 * 1024
    with open(name, 'r+b') as f:
        size = os.path.getsize(name)
        data = f.read(readsize)
        f.seek(-readsize, os.SEEK_END)
        data += f.read(readsize)
    return hashlib.md5(data).hexdigest()

def get_request(hash):
    url = 'http://api.thesubdb.com/?action=download&hash='+hash+'&language=en'
    request = urllib2.Request(url)
    request.add_header('User-agent', 'SubDB/1.0 (SubTank/0.1; http://github.com/CHURLZ/subtank)')
    return request

def get_subname(file):
    fileName = file
    filelength = len(file)
    if(file[filelength-4]) == '.':
        fileName = file[:-4]
    elif(file[filelength-5]) == '.':
        fileName = file[:-5]
    return fileName + '.srt'

file = sys.argv[1]
hash = get_hash(file)

contents = urllib2.urlopen(get_request(hash))
if contents.getcode() == 200:
    print("printing sub to file:" + get_subname(file))
    output = open(get_subname(file), 'w')
    output.write(contents.read())
    output.close()
else:
    print("### ERROR ###")
    print(contents.read())
