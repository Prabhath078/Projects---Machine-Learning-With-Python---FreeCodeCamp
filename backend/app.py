import os
import urllib.request
import pickle
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- ML Setup ---
TRAIN_URL = "https://cdn.freecodecamp.org/project-data/sms/train-data.tsv"
TEST_URL = "https://cdn.freecodecamp.org/project-data/sms/valid-data.tsv"

def download_data():
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)')]
    urllib.request.install_opener(opener)

    if not os.path.exists("train-data.tsv"):
        print("Downloading train data...")
        urllib.request.urlretrieve(TRAIN_URL, "train-data.tsv")
    if not os.path.exists("valid-data.tsv"):
        print("Downloading valid data...")
        urllib.request.urlretrieve(TEST_URL, "valid-data.tsv")

model = None
tokenizer = None

def init_model():
    global model, tokenizer
    if os.path.exists('spam_model.keras') and os.path.exists('tokenizer.pkl'):
        print("Loading saved model and tokenizer...")
        model = keras.models.load_model('spam_model.keras')
        with open('tokenizer.pkl', 'rb') as handle:
            tokenizer = pickle.load(handle)
        return

    download_data()
    print("Training model from scratch...")
    
    df_train = pd.read_csv("train-data.tsv", sep='\t', names=['label', 'message'])
    df_test = pd.read_csv("valid-data.tsv", sep='\t', names=['label', 'message'])

    df_train['label'] = df_train['label'].map({'ham': 0, 'spam': 1})
    df_test['label'] = df_test['label'].map({'ham': 0, 'spam': 1})

    tokenizer_local = Tokenizer()
    tokenizer_local.fit_on_texts(df_train['message'])
    vocab_size = len(tokenizer_local.word_index) + 1

    train_seq = tokenizer_local.texts_to_sequences(df_train['message'])
    test_seq = tokenizer_local.texts_to_sequences(df_test['message'])

    train_padded = pad_sequences(train_seq, maxlen=50)
    test_padded = pad_sequences(test_seq, maxlen=50)

    model_local = keras.Sequential([
        keras.layers.Embedding(vocab_size, 32, input_length=50),
        keras.layers.GlobalAveragePooling1D(),
        keras.layers.Dense(32, activation='relu'),
        keras.layers.Dense(1, activation='sigmoid')
    ])

    model_local.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    print("Model Training starting...")
    model_local.fit(
        train_padded,
        df_train['label'],
        epochs=20,
        validation_data=(test_padded, df_test['label']),
        verbose=1
    )
    
    print("Saving model and tokenizer for future use...")
    model_local.save('spam_model.keras')
    with open('tokenizer.pkl', 'wb') as handle:
        pickle.dump(tokenizer_local, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
    model = model_local
    tokenizer = tokenizer_local

@app.route('/predict/spam', methods=['POST'])
def predict_spam():
    data = request.json
    text = data.get('message', '')
    if not text:
        return jsonify({'error': 'No message provided'}), 400
        
    seq = tokenizer.texts_to_sequences([text])
    padded = pad_sequences(seq, maxlen=50)
    pred_value = float(model.predict(padded)[0][0])
    
    label = "ham" if pred_value < 0.5 else "spam"
    
    return jsonify({
        'prediction': label,
        'probability': pred_value
    })

if __name__ == '__main__':
    print("Initializing Model...")
    init_model()
    print("Starting Flask Server...")
    app.run(port=5000, debug=False)
