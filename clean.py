import regex

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

with open("lyrics_quebonafide_25godzina.txt", 'r') as rfile:
    lyrics = rfile.read()

onefile_nobrackets([lyrics], "test.txt")
