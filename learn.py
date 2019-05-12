from keras.preprocessing.text import Tokenizer
from numpy import array
from keras.utils import to_categorical, plot_model
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense, Dropout
from keras.preprocessing.sequence import pad_sequences
from keras.callbacks import ModelCheckpoint
from keras.models import load_model

def define_model(vocab_size, max_length):
    model = Sequential()
    model.add(Embedding(vocab_size, 200, input_length=max_length-1))
    model.add(LSTM(200, return_sequences=True))
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


filepath="Saved_models/words_model-{epoch:02d}-{val_acc:.2f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=False, mode='max')
callbacks_list = [checkpoint]
# Fit the model
model.fit(X, y, validation_split=0.10, epochs=150, batch_size=50, callbacks=callbacks_list, verbose=1)
#model = load_model('weights-improvement-49-0.20.hdf5')

print(generate_seq(model, tokenizer, max_length-1, 'Nie płacz bo lubie cie' , 50))
