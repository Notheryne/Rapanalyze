import pyphen

dic = pyphen.Pyphen(lang='pl')

with open('test.txt', 'r', encoding = 'utf-8') as rfile:
    lyrics = rfile.read()

lyrics = lyrics.replace('\n', ' ').strip(' ')

lyrics = lyrics.split(' ')



lyrics = [dic.inserted(lyric) for lyric in lyrics]
#print(lyrics)

polish_signs = ['ć', 'ł', 'ń', 'ś', 'ż', 'ź']

"""
for i in lyrics:
    print(i)
    if i[-1] in polish_signs:
        if i[-2] == '-':
            i = i[:-2] + i[-1]
"""
print(lyrics)
lyrics = ' '.join(lyrics)
print(lyrics)
with open("sylab-test.txt", 'w', encoding='utf-8') as wfile:
    wfile.write(lyrics)
