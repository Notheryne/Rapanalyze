import pygame as pg
from keras.preprocessing.text import Tokenizer
from numpy import array
from keras.utils import to_categorical, plot_model
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense,Dropout
from keras.preprocessing.sequence import pad_sequences
from keras.callbacks import ModelCheckpoint
from keras.models import load_model

import pygame as pg

def define_model(vocab_size, max_length):
    model = Sequential()
    model.add(Embedding(vocab_size, 10, input_length=max_length-1))
    model.add(LSTM(500))

    model.add(Dropout(0.5))
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
    for _ in range(n_words):
        # encode the text as integer
        encoded = tokenizer.texts_to_sequences([in_text])[0]
        # pre-pad sequences to a fixed length
        encoded = pad_sequences([encoded], maxlen=max_length, padding= 'pre' )
        # predict probabilities for each word
        yhat = model.predict_classes(encoded, verbose=0)
        # map predicted word index to word
        out_word = ''
        for word, index in tokenizer.word_index.items():
            if index == yhat:
                out_word = word
                break
# append to input
        in_text += ' ' + out_word
    return in_text


with open('scraping/x00', 'r', encoding='utf-8') as rfile:
    data = rfile.read()
data = data.replace('\n',', nowalinia ')
tokenizer = Tokenizer()
tokenizer.fit_on_texts([data])
encoded = tokenizer.texts_to_sequences([data])[0]
# retrieve vocabulary size
vocab_size = len(tokenizer.word_index) + 1
print( ' Vocabulary Size: %d ' % vocab_size)
# encode 2 words -> 1 word
sequences = list()
for i in range(2, len(encoded)):
    sequence = encoded[i-5:i+1]
    sequences.append(sequence)
print( ' Total Sequences: %d ' % len(sequences))
# pad sequences
max_length = max([len(seq) for seq in sequences])
sequences = pad_sequences(sequences, maxlen=max_length, padding= 'pre' )
print( ' Max Sequence Length: %d ' % max_length)
# split into input and output elements
sequences = array(sequences)
X, y = sequences[:,:-1],sequences[:,-1]
y = to_categorical(y, num_classes=vocab_size)
# define model
model = define_model(vocab_size, max_length)
# fit network
#model.fit(X, y, epochs=100, verbose=2)
# evaluate model


filepath="weights-improvement-{epoch:02d}-{val_acc:.2f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
callbacks_list = [checkpoint]
# Fit the model
#model.fit(X, y, validation_split=0.10, epochs=50, batch_size=5, callbacks=callbacks_list, verbose=0)
model = load_model('Saved_models/words_model-150-0.07.hdf5')

print(generate_seq(model, tokenizer, max_length-1, 'Nie płacz bo lubie cie' , 50))

def generate_seq(model, tokenizer, max_length, seed_text, n_words):
    in_text = seed_text
    # generate a fixed number of words
    for _ in range(n_words):
        # encode the text as integer
        encoded = tokenizer.texts_to_sequences([in_text])[0]
        # pre-pad sequences to a fixed length
        encoded = pad_sequences([encoded], maxlen=max_length, padding= 'pre' )
        # predict probabilities for each word
        yhat = model.predict_classes(encoded, verbose=0)
        # map predicted word index to word
        out_word = ''
        for word, index in tokenizer.word_index.items():
            if index == yhat:
                out_word = word
                break
# append to input
        in_text += ' ' + out_word
    return in_text







def main():
    sequence = ''

    screen = pg.display.set_mode((700, 500))
    font = pg.font.Font(None, 32)
    title_font = pg.font.SysFont("Impact", 72)
    sequence_font =  pg.font.SysFont("Impact", 10)
    clock = pg.time.Clock()
    input_box = pg.Rect(0, 0, 140, 32)
    input_box.center=(640/2-200,100)
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
                        sequence = generate_seq(model, tokenizer, max_length-1, text , 50).replace("nowalinia ",'\n')
                        sequence = sequence.split('\n')
                        label = []
                        for line in sequence:
                                label.append(font.render(line, True, (255,255,255)))
                        text = ''
                    elif event.key == pg.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
            elif event.type==pg.VIDEORESIZE:
                screen=pg.display.set_mode(event.dict['size'],pg.HWSURFACE|pg.DOUBLEBUF|pg.RESIZABLE)
                screen.fill((30, 30, 30))
                title_text_rect = txt_title.get_rect(center=(event.dict['size'][0], 50))
                input_box.center=(event.dict['size'][0],100)
                print(event.dict['size'][0])
                pg.display.flip()
        screen.fill((30, 30, 30))
        # Render the current text.
        txt_surface = font.render(text, True, (255,255,255))
        txt_title = title_font.render("Neural rap", True, (255,255,255))
        #txt_sequence = sequence_font.render(sequence, True, (255,255,255))
        title_text_rect = txt_title.get_rect(center=(700/2, 50))

        # Resize the box if the text is too long.
        width = max(500, txt_surface.get_width()+10)
        input_box.w = width
        # Blit the text.
        input_box.center=(700/2,100)
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
