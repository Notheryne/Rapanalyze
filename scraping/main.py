import os

from parts import getting_data as gd
from parts import make_txt as mt
from parts import get_together as gt
from parts import sort_into_folders as sif
from parts import counters

def do_everything(rappers, id, jsons_dir, txts_dir, m_songs, org_file, nb_file, cl_file, sorted_txts_dir, sorting, outfile):
    """
    rappers - list or tuple of names you want to search on genius (only artists), it will take songs from top result
    id - your Genius API id
    jsons_dir - a directory in which you want to store .json files
    txts_dir - a directory in which you want to store .txt files
    m_songs - amount of songs for each rapper you want to download, if more than he has made,
    m_songs - it will just take all of them, so if you want all, just set to 10000 or something
    org_file - where you want to store all texts together in orginal formatting
    nb_file - where you want to store all texts together without brackets
    cl_file - where you want to store all words without anything else (only spaces)
    sorted_txts_dir - directory you want to make folders for each rapper and put his songs in there
    sorting - either True or False, if you want to sort as above or not
    outfile - where you want to store words with their occurences numbers and frequencies
    """
    if sorting == True:
        if not os.path.exists(sorted_txts_dir):
            os.makedirs(sorted_txts_dir)
    elif sorting == False:
        pass
    else:
        print("Wrong 'sorting' value! It must be True or False!")
        return
    #sorting is True if you want to make a directory for each rapper (names may be a little broken)
    #if it's not bool, you'll get error message

    if not os.path.exists(jsons_dir):
        os.makedirs(jsons_dir)
    if not os.path.exists(txts_dir):
        os.makedirs(txts_dir)
    #create directories for jsons and txts if not created yet

    os.chdir(jsons_dir)
    #go into jsons directory
    gd.get_jsons(rappers, id, m_songs)
    #get songs in jsons
    os.chdir('..')
    #go back into main directory
    mt.jsons_to_txts(jsons_dir, txts_dir)
    #make txt files from jsons
    if sorting == True:
        sif.sort_by_folders(txts_dir, sorted_txts_dir)
    #if sorting is True sort songs into rapper's folder

    lyrics = gt.import_lyrics(txts_dir)
    #get lyrics from all txts
    gt.onefile_orginal(lyrics, org_file)
    #get one file with all texts, keeping original formatting
    gt.onefile_nobrackets(lyrics, nb_file)
    #get one file with all texts, remove everything in brackets ([Verse: xxx] etc.)
    gt.onefile_clean(lyrics, cl_file)
    #get one file with all texts, removing all special signs, newlines etc

    counters.save_counters(cl_file, outfile)
    #count words and save result as a PrettyTable(), based on cl_file

id = "axt5F6Ftpw5kY7CZWEKvQqsqnp9YwiyrEfw-3tPeNjEw2HggilHfhjGFOwrY--7z" #YOUR GENIUS API ID GOES HERE!
jsons_dir = "jsons"
txts_dir = "texts"
sorted_txts_dir = "texts_folders"
m_songs = 1000
rappers = ['Adi Nowak', 'O.S.T.R.', 'Kartky', 'RAU (PL)', 'Paktofonika', 'Peja', 'Chada',
'Cira', 'Deys', 'Diox', 'Donguralesko', 'Eldo', 'Ero JWP', 'Filipek', 'Fisz', 'Gedz',
'Gruby Mielzky', 'Guzior', 'Taco Hemingway', 'HuczuHucz', 'Kaczor', 'Kaen'
, 'Kaz Bałagane', 'KęKę', 'FIlipek'] #first round
rappers2 = ['Kuban', 'Leh', 'Łona', 'Małolat', 'Vixen',
'Otsochodzi', 'Paluch', 'Peerzet', 'Pelson', 'Pezet', 'Pih', 'PlanBe',
'Planet ANM', 'Pono', 'Pyskaty', 'Quebonafide', 'Rafi', 'ReTo', 'Sarius',
'Shellerini', 'Sitek', 'Siwers', 'Słoń', 'Smolasty', 'Sobota', 'Sokół', 'Solar',
'Spinache', 'Szad', 'Szesnasty', 'Szpaku', 'PRO8L3M', 'Grammatik', 'Ten Typ Mes',
'Jan-rapowanie', 'VBS', 'B.R.O (PL)', 'Płomień 81', 'Hemp Gru', 'TACONAFIDE',
'VNM', '2sty', 'Abradab', 'Bedoes', 'Bezczel', 'Białas', 'Bilon', 'Bisz', 'Bonson',
 'Bonus RPK', 'Borixon', 'Buka']
rappers3 = ['Kuba Knap', 'Liroy', 'Małpa', 'Meek, Oh Why?', 'Miuosh', 'Nullo', 'Onar']
org_file = "orginal.txt"
nb_file = "nobrackets.txt"
cl_file = "clean.txt"
outfile = "sorted amounts.txt"
sorting = True

do_everything(rappers3, id, jsons_dir, txts_dir, m_songs, org_file, nb_file, cl_file, sorted_txts_dir, sorting, outfile)
