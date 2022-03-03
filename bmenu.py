#!/usr/bin/env python3
import os
import re
import sys
from random import choice
from os.path import isdir
import tracemalloc

# ---------------------------------- About ----------------------------------- #
# This file inserts a wallpaper pipe menu into Openbox which uses feh          #
# in order to set the wallpaper from a chosen directory.                       #
#                                                                              #
# Authors: dav1d(main author) and Pwnz3r(hacker and redistributor)             #
#                                                                              #
# Dav1d's site: http://southwing.homeip.net/~david/                            #
# Pwnz3r's site: http://pstudios.ath.cx/                                       #
#                                                                              #
# ------------------------------ Setting it up ------------------------------- #
# feh automatically inserts the full command string used to set the wallpaper  #
# into ~/.fehbg. In order to set the wallpaper back at the next start of       #
# Openbox, just add the following to ~/.xinitrc.                               #
#                                                                              #
# eval `cat ~/.fehbg`                                                          #
# ---------------------------------------------------------------------------- #

# types of files accepted (list, seperated by a |)
filetypes = "jpg|png|gif"
# directory where wallpapers are stored (must be long: no ~ symbol allowed)
directory = sys.argv[1]
# directory where thumbnails can be found. The files name must match up with the files in "directory"
thumbnails = sys.argv[2]

# program to set wallpaper defined in the command string
program = "feh --bg-scale"

# image paths, for random selection
img_paths = []


def genmenu(start, directory):
    # get a directory list
    dirlist = os.listdir(directory)
    for d in dirlist:
        # set di to overall directory
        di = directory + "/" + d
        # if we get a dir, generate a menu
        if isdir(di) and ".thumbnails" not in di:
            print("")
            print(f"  <menu id=\"{di}\" label=\"{d}\" >")
            genmenu(start, di)
            print("  </menu>")
        # if we get a file, check if it is a valid type
        else:
            if re.search(filetypes, di.lower()):
                print("  <item")

                # open the file
                fi = str.replace(str.replace(di, directory, ""), "/", "")
                print(f"\ticon= \"{thumbnails}{fi}\"")

                # make fi variable just filename, without extension
                fi = fi[:str.rfind(fi, ".")]
                # if so, add it to the pipe menu
                print(f"\tlabel=\"{fi}\"")
                print("  >")

                img_paths.append(di)

                # execute line to set wallpaper
                print(f"    <action name=\"Execute\"><execute>{program} \"{di}\" </execute></action>")
                # if we want to update config file, do so
                print("  </item>")


def main():
    # start menu
    print("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
    print("<openbox_pipe_menu>")

    # open base wallpaper directory
    print(f"""<item label=\"Open Wallpaper Directory\">
    <action name=\"Execute\"><execute>xdg-open {directory}</execute></action>
    </item>""")

    # TODO: some how put the random wallpaper thing here? How will I do that? Save up the buffer?
    # Is that good? Anyother way?

    print("<separator />")
    # set the original start directory
    start = directory
    # generate menu
    genmenu(start, directory)

    # set a random wallpaper, from the list of wallpapers
    rand_wallpaper = choice(img_paths)
    print(f"""<item label=\"Set a Random Wallpaper\">
    <action name=\"Execute\"><execute>{program} \"{rand_wallpaper}\"</execute></action>
    </item>""")

    # end menu
    print("</openbox_pipe_menu>")


# run the main() function
if __name__ == "__main__":
    tracemalloc.start()
    main()
    print("Current: %d, Peak %d" % tracemalloc.get_traced_memory())
