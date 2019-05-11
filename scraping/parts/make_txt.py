import json
from os import listdir
from os.path import isfile, join


def find_jsons(jsons_path, control):
    #if file is of type json, create a list of strings with it's name
    songs = [f for f in listdir(jsons_path) if
        isfile(join(jsons_path, f)) and f[-4:] == "json"]
    if jsons_path[-2:] != '\\':
        jsons_path += '\\'
    #then it's path, so you can access it
    songs_jsons = [jsons_path + i for i in songs]
    if control == "dir":
        return songs_jsons
    if control == "names":
        return songs

def make_new_paths(txt_path, jsons):
    #make new txt files based on jsons
    if txt_path[-2:] != '\\':
        txt_path += '\\'

    songs_txts = [txt_path + i[:-5] + ".txt" for i in jsons]

    for i in songs_txts:
        with open(i, 'w') as writefile:
            writefile.write("")

    return songs_txts

def jsons_to_txts(jsons_path, txt_path):
    jsons = find_jsons(jsons_path, "dir")
    txts = make_new_paths(txt_path, find_jsons(jsons_path, "names"))

    lyrics = []
    for i in jsons:
        with open(i, 'r') as readfile:
            data = json.load(readfile)
            lyrics.append(data['songs'][0]['lyrics'])

    for i in range(len(txts)):
        with open(txts[i], 'w', encoding = "utf-8") as writefile:
            writefile.write(lyrics[i])

    print("Success! Got {} songs.".format(str(len(txts))))
