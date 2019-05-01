from keras.preprocessing.text import Tokenizer
from numpy import array
from keras.utils import to_categorical, plot_model
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense


def define_model(vocab_size):
    model = Sequential()
    model.add(Embedding(vocab_size, 10, input_length=2))
    model.add(LSTM(50))
    model.add(Dense(vocab_size, activation='softmax'))
    # compile network
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    # summarize defined model
    model.summary()

    return model


def generate_seq(model, tokenizer, seed_text, n_words):
    in_text, result = seed_text, seed_text
    # generate a fixed number of words
    for _ in range(n_words):
        # encode the text as integer
        encoded = tokenizer.texts_to_sequences([in_text])[0]
        encoded = array(encoded)
        # predict a word in the vocabulary
        yhat = model.predict_classes(encoded, verbose=0)
        # map predicted word index to word
        out_word = ''
        for word, index in tokenizer.word_index.items():
            if index == yhat:
                out_word = word
                break
    # append to input
        in_text, result = out_word, result + ' ' + out_word
    return result

with open('test.txt', 'r', encoding='utf-8') as rfile:
    data = rfile.read()

tokenizer = Tokenizer()
tokenizer.fit_on_texts([data])
encoded = tokenizer.texts_to_sequences([data])[0]

vocab_size = len(tokenizer.word_index) + 1
print('Vocabulary Size: %d' % vocab_size)

sequences = []
for i in range(2, len(encoded)):
    sequence = encoded[i-2:i+1]
    sequences.append(sequence)

print('Total Sequences: %d' % len(sequences))

sequences = array(sequences)
print(sequences)

X, y = sequences[:,:-1],sequences[:,-1]


y = to_categorical(y, num_classes=vocab_size)

model = define_model(vocab_size)
# fit network
model.fit(X, y, epochs=500, verbose=2)
# evaluate
print(generate_seq(model, tokenizer, 'Co bym', 193))
