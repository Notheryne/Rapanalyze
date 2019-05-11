from prettytable import PrettyTable

def count(file):
    #count how many times each word appeared

    with open(file, 'r', encoding = "utf-8") as readfile:
        words = readfile.read()
    #get words from file

    words = words.split(" ") #make list from string
    words = [word for word in words if word != ""] #remove empty strings

    all_words = len(words) #get number of all words

    with open("stopwords.txt", 'r', encoding = "utf-8") as stopfile:
        stopwords = stopfile.read()
    stopwords = stopwords.split("\n") #get stopwords, because there's no point counting these

    words = [word for word in words if word not in stopwords] #delete all stopwords from words

    without_stopwords = len(words) #get number of words without stopwords

    occurences = {}

    for i in words:
        if i in occurences.keys():
            occurences[i] += 1
        else:
            occurences[i] = 1
    #actual counting

    sorted_list = sorted(occurences.items(), key=lambda x: x[1], reverse=True)
    #sort by number of occurences (mostly used up top)

    unique_words = len(sorted_list)

    return sorted_list, all_words, without_stopwords, unique_words

def save_counters(file, outfile):
    noname = count(file)
    sorted_list = noname[0]
    all_words = noname[1]
    without_stopwords = noname[2]
    unique_words = noname[3]
    #get values from count
    all_frequencies = [round(i[1] / all_words, 8) for i in sorted_list]
    ws_frequencies = [round(i[1] / without_stopwords, 8) for i in sorted_list]
    unique_frequencies = [round(i[1] / unique_words, 8) for i in sorted_list]
    #get frequencies for each word
    all_occurences = [i[1] for i in sorted_list]
    occurences = sum(all_occurences)
    #get sum of all occurences, should be same as without_stopwords

    table = PrettyTable()
    table.field_names = ['Words', 'Occurences', 'F (all words)', 'F (no stopwords)', 'F (unique)']
    #initialize PrettyTable() with field names

    for i in range(len(sorted_list)):
        table.add_row([sorted_list[i][0], sorted_list[i][1], all_frequencies[i],
                    ws_frequencies[i], unique_frequencies[i]])
    #add_row for each word to PrettyTable()

    with open(outfile, 'w', encoding = "utf-8") as writefile:
        writefile.write("Based on {} words, {} after removing stopwords ({} unique words).\n**F means frequency.**\n\n".format(
        all_words, without_stopwords, unique_words
        ))
        writefile.write(table.get_string())
    #save to outfile
