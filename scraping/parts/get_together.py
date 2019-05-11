from os import listdir
from os.path import isfile, join
import regex


def import_lyrics(txt_path):
    #get lyrics from txts created before with make_txt.py
    #if txt_path doesn't end with \\ -> add it
    if txt_path[-2:] != '\\':
        txt_path += '\\'

    #get list of all txt files in your txt path
    songs = [f for f in listdir(txt_path) if
        isfile(join(txt_path, f)) and f[-3:] == "txt"]

    #make paths from list of songs
    songs_paths = [txt_path + i for i in songs]

    lyrics = []
    for i in songs_paths:
        with open(i, 'r', encoding="utf-8") as readfile:
            s = readfile.read()
            lyrics.append(s)
        #make list of lyrics
    return lyrics

def onefile_orginal(lyrics, file):
    #put every txt into one file, must pass list lyrics
    #keep orginal formatting
    with open(file, 'a', encoding="utf-8") as writefile:
        for i in lyrics:
            writefile.write(i + '\n')

def onefile_nobrackets(lyrics, file):
    #put every txt into one file, must pass list lyrics
    #remove everything in brackets or parentheses,
    #like (x2) or [Verse: xxx]
    new_lyrics = []

    for i in lyrics:
        s = regex.subf(r'\[.*.\]', "", i)
        s = regex.subf(r'\(x.*.\)', "", s)
        new_lyrics.append(s)

    if file != 0:
        with open(file, 'a', encoding = "utf-8") as writefile:
            for i in new_lyrics:
                writefile.write(i + '\n')
        #as default you'd pass file path to this function,
        #the 0 option is for the other function
    else:
        return new_lyrics

def onefile_clean(lyrics, file):
    #put everything into one file, must pass list lyrics
    #remove special signs, don't keep newlines

    new_lyrics = onefile_nobrackets(lyrics, 0)

    new_clean = []
    for i in new_lyrics:
        s = i.replace("\n", " ").lower()
        s = regex.sub(' +', ' ', s)
        s = regex.sub(r"[-()\"#/@;:<>{}`+=~|.!?,]", "", s)
        s = regex.sub("x2", "", s)
        s = regex.sub("x3", "", s)
        s = regex.sub("x4", "", s)
        s = regex.sub("x5", "", s)
        s = regex.sub("x6", "", s)
        s = regex.sub("x7", "", s)
        s = regex.sub("x8", "", s)
        s = regex.sub("x9", "", s)
        new_clean.append(s)

    with open(file, 'a', encoding = "utf-8") as writefile:
        for i in new_clean:
            writefile.write(i)
