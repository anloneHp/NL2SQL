from flask import Flask, render_template, request, jsonify
import os
import pickle
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import re

# Flask uygulamasını başlat
app = Flask(__name__)

# Template ve static klasörlerini belirtiyoruz
app.template_folder = 'templates'
app.static_folder = 'static'

# Modelleri yükle
try:
    model = load_model("nl2sql_seq2seq_model.keras")
    encoder_model = load_model("encoder_model.keras")
    decoder_model = load_model("decoder_model.keras")
    
    # Tokenizer'ları yükle
    with open('tokenizer_input.pkl', 'rb') as f:
        input_tokenizer = pickle.load(f)
    
    with open('tokenizer_target.pkl', 'rb') as f:
        target_tokenizer = pickle.load(f)
    
    # Tokenizer sözlüklerini oluştur
    reverse_target_word_index = {i: word for word, i in target_tokenizer.word_index.items()}
    max_encoder_len = 100  # encoder_model.input_shape[1] kullanabilirsiniz
    max_decoder_len = 100
    
    print("Modeller ve tokenizer'lar başarıyla yüklendi!")
except Exception as e:
    print(f"Model yüklenirken hata oluştu: {str(e)}")
    raise e

def temizle_input(text):
    text = str(text)
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    text = text.lower()
    return text

def predict_query(input_sentence):
    input_sentence = temizle_input(input_sentence)
    input_seq = input_tokenizer.texts_to_sequences([input_sentence])
    input_seq = pad_sequences(input_seq, maxlen=max_encoder_len, padding='post')
    
    states_value = encoder_model.predict(input_seq, verbose=0)

    target_seq = np.zeros((1, 1))
    target_seq[0, 0] = target_tokenizer.word_index['<start>']

    stop_condition = False
    decoded_sentence = ''

    while not stop_condition:
        output_tokens, h, c = decoder_model.predict([target_seq] + states_value, verbose=0)

        sampled_token_index = np.argmax(output_tokens[0, -1, :])
        sampled_word = reverse_target_word_index.get(sampled_token_index, '')

        if sampled_word == '<end>' or len(decoded_sentence.split()) > max_decoder_len:
            stop_condition = True
        else:
            decoded_sentence += ' ' + sampled_word

        target_seq = np.zeros((1, 1))
        target_seq[0, 0] = sampled_token_index
        states_value = [h, c]

    return decoded_sentence.strip()

# Anasayfa için route
@app.route('/')
def home():
    return render_template('index.html')

# Modeli çalıştıracak route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Kullanıcıdan gelen girdi metnini al
        input_text = request.form.get('input_text', '')
        
        if not input_text:
            return jsonify({"error": "Lütfen bir metin girin"}), 400
        
        # Modeli kullanarak tahmin yap
        prediction = predict_query(input_text)
        
        # Tahmin sonucunu JSON olarak döndür
        return jsonify({
            "input_text": input_text,
            "sql_query": prediction
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Uygulamayı çalıştır
if __name__ == '__main__':
    app.run(debug=True)
