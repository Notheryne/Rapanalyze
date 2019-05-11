import shutil
import os
from os.path import isfile, join
import regex

def make_folders(txt_path, new_path, nofile = None):
    if txt_path[-2:] != "\\":
        txt_path += "\\"
    if new_path[-2:] != "\\":
        new_path += "\\"

    songs = [f for f in os.listdir(txt_path) if
            isfile(join(txt_path, f)) and f[-3:] == "txt"]

    no_lyrics = [song.strip("lyrics_") for song in songs] #removed lyrics_ from all songs

    rappers = [song[:song.find("_")] for song in no_lyrics] #get all rappers

    rappers = list( dict.fromkeys(rappers) ) #remove duplicates

    rappers = [rapper[0].upper() + rapper[1:] for rapper in rappers] #make the first letter big

    rappers_dirs = [new_path + rapper for rapper in rappers]

    for rapper in rappers_dirs:
        if not os.path.exists(rapper):
            os.makedirs(rapper)

    if nofile != None:
        return rappers, songs, rappers_dirs

def copy_to_folders(txt_path, new_path):

    rappers = make_folders(txt_path, new_path, 1)[0]
    songs = make_folders(txt_path, new_path, 1)[1]
    rappers_dirs = make_folders(txt_path, new_path, 1)[2]
    #print(rappers_dirs)

    rappers = [rapper.lower() for rapper in rappers]

    rapper_start = rappers_dirs[0].find("\\") + 1
    rappers_songs = {}

    for rapper in rappers_dirs:
        his_songs = []
        for song in songs:
            #print(rapper[rapper_start:])
            if song.find(rapper[rapper_start:].lower()) != -1:
                his_songs.append(song)
        rappers_songs[rapper] = his_songs

    new_songs_dirs = [key + "\\" + i for key,value in rappers_songs.items()
            for i in value]

    if txt_path[-2:] != "\\":
        txt_path += "\\"
    if new_path[-2:] != "\\":
        new_path += "\\"

    songs_dirs = [txt_path + song for song in songs]

    for i in range(len(songs_dirs)):
        shutil.copy2(songs_dirs[i], new_songs_dirs[i])

def sort_by_folders(txt_path, new_path):
    make_folders(txt_path, new_path)
    copy_to_folders(txt_path, new_path)

txt_path = "texts"
new_path = "texts_folders"
