import lyricsgenius
import json

def get_jsons(rappers, my_id, m_songs):
    #get jsons with data about m_songs songs of rappers[i] rapper
    #pass your id, list/tuple of rappers and max songs for every one
    genius = lyricsgenius.Genius(my_id)

    for i in range(len(rappers)):
        try:
            artist = genius.search_artist(rappers[i],max_songs = m_songs,  sort="title")
            artist.save_lyrics()
        except Exception as error:
            #if you get an exception just write it into a file
            #and continue with another rapper, because it takes
            #some time, and if it fails on say third rapper,
            #you may be screwed
            with open("errors.txt", 'a') as f:
                err_mess = "\n#########################################"
                err_mess2 = "\nProblem z: " + rappers[i] + "\n" + str(error)
                f.write(err_mess + err_mess2)
            continue
