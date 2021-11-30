import itunespy
import urllib.request
from hashlib import md5
import os
from db import *

ARTWORK_FILEPATH_TEMPLATE = "/home/pi/ams/artwork/{}.jpg"
MISSING_ARTWORK_PLACEHOLDER = "/home/pi/ams/missing.jpg"

def new_media(*args):
    display_artwork(*args)


def display_artwork(*args):

    concat = args[1]+args[0]
    hashstr = md5(concat.encode('utf-8')).hexdigest()
    print(hashstr)

    filepath = ARTWORK_FILEPATH_TEMPLATE.format(hashstr)
    if not os.path.exists(filepath):
        print("Inserting!")
        insert_track(args[1], args[0], args[2], hashstr)
        print("Inserted")
        display_on_screen(MISSING_ARTWORK_PLACEHOLDER)
    else:
        display_on_screen(filepath)
    return filepath


def display_on_screen(path):

    if os.path.exists(path):
        os.system("sudo killall fbi")
        os.system("sudo fbi -T 1 --fitwidth --noverbose {}".format(path))
        return True
    else:
        return False
        print("Not a path")

