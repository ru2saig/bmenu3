#!/usr/bin/env python

import os
import glob
import sys
from PIL import Image
from multiprocessing import Pool

SIZE = (48, 48)
FILES = "[.jpg, .png]"

strip_dir = lambda f : f.replace(wallpaper_dir, "")


def gen_thumbnail(f):
    im = Image.open(f)
    im.thumbnail(SIZE)
    im.save(save_dir + strip_dir(f))


if __name__ == "__main__":
    try:
        wallpaper_dir = sys.argv[1]
        save_dir = sys.argv[2]
    except IndexError:
        print("Usage: genthumbs.py [directory] [save directory]\n"
              "\tdirectory is where target files are located.\n"
              "\tsave directory is where thumbnails will be placed")
        exit(1)

    # make sure the paths are uniform
    if wallpaper_dir[-1] != '/':
        wallpaper_dir += "/"

    if save_dir[-1] != '/':
        save_dir += "/"

    files = glob.glob(wallpaper_dir + "*" + FILES)

    try:
        os.makedirs(save_dir)
    except FileExistsError:
        print(f"{save_dir} directory already created", file=sys.stderr)

    pool = Pool(8)
    pool.map(gen_thumbnail, files)
