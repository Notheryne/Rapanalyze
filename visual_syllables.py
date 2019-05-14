import pygame as pg
from keras.preprocessing.text import Tokenizer
from numpy import array
from keras.utils import to_categorical, plot_model
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense,Dropout
from keras.preprocessing.sequence import pad_sequences
from keras.callbacks import ModelCheckpoint
from keras.models import load_model
from syllables import Syllables
import pygame as pg
import time

def define_model(vocab_size, max_length):
    model = Sequential()
    model.add(Embedding(vocab_size, 200, input_length=max_length-1))

    model.add(LSTM(200, dropout=0.5))

    model.add(Dense(vocab_size, activation= 'softmax' ))
    # compile network
    model.compile(loss= 'categorical_crossentropy' , optimizer= 'adam' , metrics=['accuracy'])
    # summarize defined model
    model.summary()
    #plot_model(model, to_file= 'model.png' , show_shapes=True)
    return model


def generate_seq(model, tokenizer, max_length, seed_text, n_words):
    in_text = seed_text
    # generate a fixed number of words
    i = 0
    start = time.time()
    while i<n_words:
        if time.time() - start > 1:
            raise Exception('gowno')
        # encode the text as integer
        #print(in_text)
        encoded = tokenizer.texts_to_sequences([in_text])[0]
        #print(encoded)
        # pre-pad sequences to a fixed length
        encoded = pad_sequences([encoded], maxlen=max_length, padding= 'pre' )
        # predict probabilities for each word
        encoded = array(encoded)
        #print(encoded)
        yhat = model.predict_classes(encoded, verbose=0)
        # map predicted word index to word
        out_word = ''
        for word, index in tokenizer.word_index.items():
            if index == yhat:
                out_word = word
                break
# append to input
        if(out_word==" "):
            pass
            #print("SPACJA")
        else:
            i+=1
        in_text +="-"+out_word
        in_text.replace("-","")
    return in_text


with open('x00_syl.txt', 'r', encoding='utf-8') as rfile:
    data = rfile.read()
data = data.replace('\n',', nowalinia ')
tokenizer = Tokenizer(split='-',filters="")
tokenizer.fit_on_texts([data])
encoded = tokenizer.texts_to_sequences([data])[0]
# retrieve vocabulary size
vocab_size = len(tokenizer.word_index) + 1
print( ' Vocabulary Size: %d ' % vocab_size)
# encode 2 words -> 1 word
sequences = list()
for i in range(5, len(encoded)):
    sequence = encoded[i-5:i+1]
    sequences.append(sequence)
    #print(sequence)
print( ' Total Sequences: %d ' % len(sequences))
# pad sequences
max_length = max([len(seq) for seq in sequences])
#sequences = pad_sequences(sequences, maxlen=max_length, padding= 'pre' )
print( ' Max Sequence Length: %d ' % max_length)
# split into input and output elements
# fit network
#model.fit(X, y, epochs=100, verbose=2)
# evaluate model


filepath="Saved_models/syllables_model-{epoch:02d}-{val_acc:.2f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=False, mode='max')
callbacks_list = [checkpoint]
# Fit the model
#model.fit(X, y, validation_split=0.10, epochs=150, batch_size=50, callbacks=callbacks_list, verbose=0)
model = load_model('Saved_models/syllables_model-100-0.43.hdf5')




def main():
    sequence = ''
    s_width = 1100
    screen = pg.display.set_mode((s_width, 600))
    font = pg.font.Font(None, 32)
    title_font = pg.font.SysFont("Impact", 72)
    sequence_font =  pg.font.SysFont("Impact", 10)
    clock = pg.time.Clock()
    input_box = pg.Rect((500)/2, 0, 140, 32)

    color_inactive = (60,60,60)
    color_active = (80,80,80)
    color = color_inactive
    active = False
    text = ''
    done = False
    label = []
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pg.KEYDOWN:
                if active:
                    if event.key == pg.K_RETURN:
                        sequence = [generate_seq(model, tokenizer, max_length-1, Syllables.split(text), 16)]
                        print(sequence)
                        for i in range(1, 15):
                            try:
                                tmp = sequence[i-1]
                                tmp = tmp.replace('-', '').replace("  ", " ")
                                tmp = tmp.split(" ")
                                tmp = tmp[-i]
                                sequence.append(generate_seq(model,tokenizer,max_length-1, Syllables.split(tmp), 16))
                            except:
                                tmp = sequence[i-1]
                                tmp = tmp.replace('-', '').replace("  ", " ")
                                tmp = tmp.split(" ")
                                tmp = tmp[-2]
                                sequence.append(generate_seq(model,tokenizer,max_length-1, Syllables.split(tmp), 16))
                        for i in sequence:
                            print(i)

                        """text = text.split(' ')
                        sequence = "\n".join([generate_seq(model, tokenizer, max_length-1, Syllables.split(t) , 15) for t in text]).replace("no-wali-nia ",'')
                        sequence.replace("-","|")
                        sequence = sequence.split('\n')
                        print(sequence)"""
                        label = []
                        for line in sequence:
                            line = line.replace("- ", " ")
                            line = line.replace(" -", " ")
                            label.append(font.render(line, True, (255,255,255)))
                        text = ''
                    elif event.key == pg.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((30, 30, 30))
        # Render the current text.
        txt_surface = font.render(text, True, (255,255,255))
        txt_title = title_font.render("Hot 16 generator", True, (255,255,255))
        #txt_sequence = sequence_font.render(sequence, True, (255,255,255))
        title_text_rect = txt_title.get_rect(center=(s_width/2, 50))

        # Resize the box if the text is too long.
        width = max(500, txt_surface.get_width()+10)
        input_box.w = width
        # Blit the text.
        input_box.center=(s_width/2,100)
        # Blit the input_box rect.
        pg.draw.rect(screen, color, input_box, 0)
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        screen.blit(txt_title,title_text_rect)
        #screen.blit(txt_sequence,(30,150))

        for line in range(len(label)):
            screen.blit(label[line],(30,150+(line*15)+(15*line)))


        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
