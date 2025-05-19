# NL2SQL Web Application
Bu uygulama doğal dil sorgularını SQL sorgularına çeviren bir web uygulamasıdır. Kullanıcıların doğal dilde yazdığı sorguları SQL sorgularına dönüştürerek veritabanı sorgulamasını kolaylaştırır.

##Ornek Gorseller
![Ekran görüntüsü 2025-05-19 134600](https://github.com/user-attachments/assets/69c4832a-b26a-4c45-aeba-962dde52f162)
![Ekran görüntüsü 2025-05-19 134645](https://github.com/user-attachments/assets/720d5c6c-487a-48da-8ace-bcf040fef25c)
![Ekran görüntüsü 2025-05-19 135339](https://github.com/user-attachments/assets/a974bb96-fa47-46b3-8092-f7daaf146f34)


## Özellikler

- Doğal dil sorgularını SQL sorgularına çevirme
- Web tabanlı kullanıcı arayüzü
- Sequence-to-sequence mimarisi
- Türkçe metin işleme desteği

## Veri Seti
train.csv: doğal dil - SQL eşleşmeleri
turkish_query_answ_sql.csv: Türkçe doğal dil - SQL eşleşmeleri
train_finetune.xlsx

Veriler birleştirilip temizlenmiştir:

Doğal dil girişleri küçük harfe çevrilmiş ve gereksiz boşluklar kaldırılmıştır.

SQL sorguları normalize edilerek, sabit değerler <value> ile değiştirilmiş ve sembollerin etrafına boşluklar eklenmiştir.

## Model Mimarisi
Model, seq2seq mimarisi üzerine kurulmuştur:

Encoder: BiLSTM (256 boyutlu, çift yönlü)

Decoder: LSTM (512 boyutlu)

Embedding: Hem encoder hem decoder için ayrı

Output: Dense katman ile softmax

## Eğitim
Model sparse_categorical_crossentropy kaybı ile eğitilmiştir.
EarlyStopping ve ModelCheckpoint kullanılmıştır.

En iyi model best_model_nl2sql_seq2seq.keras olarak kaydedilir.
encoder ve decoder modeller kaydedilir 
tokenizasyonlar kaydedilir

 
## Değerlendirme
Modelin çıktısı aşağıdaki metriklerle değerlendirilmiştir:

BLEU Score

ROUGE-1

ROUGE-2

ROUGE-L

Değerlendirme sonrası skorlar grafik olarak görselleştirilmiştir.

## Teknik Detaylar

- **Framework**: Flask
- **Model**: Sequence-to-sequence (Seq2Seq) encoder BILSTM decoder LSTM
- **Tokenizer**: Keras Tokenizer
- **Dil**: Türkçe
- **Max Input/Output Uzunluğu**: 100 token
- 
 
## Kullanılan Kütüphaneler
TensorFlow / Keras

pandas

sklearn

nltk

rouge_score

matplotlib

re
