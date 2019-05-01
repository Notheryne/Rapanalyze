import math

def count_vowels(word):
    vowels = ['a', 'ą', 'e', 'ę', 'i', 'y', 'o', 'u',
            'A', 'Ą', 'E', 'Ę', 'I', 'Y', 'O', 'U']

    counter = 0
    indexes = []

    for i in range(len(word)):
        if word[i] in vowels:
            counter += 1
            indexes.append(i)

    return counter, indexes

def gowno(word):
    c, indexes = count_vowels(word)
    mean = [0]
    for i in range(1, len(indexes)):
        mean.append(math.ceil((indexes[i-1] + indexes[i]) /2))
    mean.append(len(word))

    syllabes = []
    for i in range(len(mean)):
        syllabes.append(word[mean[i-1]:mean[i]])

    return '-'.join(syllabes[1:])

with open('test.txt', 'r', encoding = 'utf-8') as rfile:
    lyrics = rfile.read()

lyrics = lyrics.replace('\n', ' ').strip(' ')

lyrics = lyrics.split(' ')
print(' '.join(lyrics))
syl = []
for l in lyrics:
    syl.append(gowno(l))

syl = ' '.join(syl)

with open("nasze_sylab-test.txt", 'w', encoding='utf-8') as wfile:
    wfile.write(syl)
