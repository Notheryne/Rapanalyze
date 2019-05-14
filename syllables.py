import math

vowels = {'a', 'ą', 'e', 'ę', 'i', 'y', 'o','ó', 'u',
    'A','E', 'I', 'Y', 'O','Ó', 'U'}

sounds = {'sz','cz','rz','ch','dż','dz'}

vowels_pairs =()
class Syllables():
    @staticmethod
    def find_vowels(text):
        indexes= []
        i=0
        while(i<len(text)):

            if(text[i] in vowels):
                if(i<len(text)-1):

                    if(text[i] =='i'):

                        if(text[i-1] not in vowels) and (text[i+1] in vowels):
                            indexes.append((i-1,i+1))
                            i+=2
                            continue

                        # handling wi,ci etc.
                        elif (text[i-1] not in vowels):
                            indexes.append((i-1,i))
                            i+=1
                            continue
                        # handling ie,ia etc.
                        elif(text[i+1] in vowels):
                            indexes.append((i,i+1))
                            i+=2
                            continue

                        else:
                            indexes.append((i,i))
                            i+=1
                            continue




                    # handling au, eu

                    if((text[i] == 'e' or text[i] =='a') and text[i+1]=='u'):
                        indexes.append((i,i+1))
                        i+=2
                        continue





                indexes.append((i,i))

            i+=1
        return indexes

    def split(text):

        #syl = []

        indexes = Syllables.find_vowels(text)
        i = 0
        #print(indexes)
        while(i < len(indexes)-1):
            begin = indexes[i][1]
            end = indexes[i+1][0]
            #print(begin,end)

            r = list(range(begin,end))
            #print('r',r)
            l = len(r)
            #print(text[end+i])
            try:
                if(text[end+1+i] == 'i'):
                    l+=1
            except:
                pass
                #print(l)
            if(l>2):
                s = math.floor((len(r))/2)
                r = r[0:s+1][::-1] + r[s+1::][::-1]
            #print(r)

            for j in r:
                #print("j",j)
                if ("".join([text[j+i],text[j+1+i]]) in sounds):
                    #print("wykryto dźwięk")
                    continue
                else:
                    #print("else")
                    #print("text :j+1",text[:j+1])
                    #syl+= text[j+1]
                    text = text[:j+1+i] + "-" +text[j+1+i:]
                    break

            i+=1

        return text



#print(Syllables.split("feudalny"))



with open('scraping/clean.txt', 'r', encoding = 'utf-8') as rfile:
    lyrics = rfile.read()

lyrics = lyrics.replace('\n', ' ').strip(' ')

lyrics = lyrics.split(' ')
#print(' '.join(lyrics))


lyrics = [Syllables.split(l) for l in lyrics]
lyrics = "- -".join(lyrics)

with open("all_syl.txt", 'w', encoding='utf-8') as wfile:
    wfile.write(lyrics)
