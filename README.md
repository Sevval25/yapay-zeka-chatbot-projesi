## Uygulama Arayüzü

Bu uygulama kullanıcıların hızlı ve güvenli şekilde hizmet bulmasını sağlar.

![sevval yapayzeka](https://github.com/user-attachments/assets/b3dc2deb-ae83-490d-be3b-6b11b131f637)

# 🤖 Transformer Tabanlı AI Destekli Chatbot Uygulaması

Bu proje, CSV formatında oluşturulmuş veri seti kullanılarak eğitilen
Transformer tabanlı (**BERT**) bir intent sınıflandırma modeli ve
**GPT destekli yanıt üretimi** içeren AI tabanlı bir chatbot uygulamasıdır.

Chatbot, kullanıcıdan gelen mesajları analiz ederek **niyet (intent) tespiti**
yapmakta ve bağlama uygun yanıtları otomatik olarak üretmektedir.

Uygulama; **NLU (Doğal Dil Anlama)**, **Diyalog Yönetimi** ve
**NLG (Doğal Dil Üretimi)** adımlarını içeren **uçtan uca bir chatbot mimarisi**
ile geliştirilmiştir.

Frontend tarafı **HTML tabanlıdır** ve backend ile **REST API** üzerinden
haberleşmektedir.

---

## 🎯 Projenin Amacı

Bu projenin temel amaçları şunlardır:

- CSV dosyası üzerinden chatbot için veri seti oluşturulması  
- Transformer tabanlı **BERT modeli** ile intent sınıflandırmasının öğretilmesi  
- Kullanıcı mesajlarının doğal dil işleme yöntemleriyle analiz edilmesi  
- Kural tabanlı bilgi cevaplarının **GPT ile daha doğal hale getirilmesi**  
- Belirsiz sorular için **GPT destekli fallback mekanizmasının** kurulması  
- Akademik bir proje kapsamında modern NLP tabanlı bir chatbot geliştirilmesi  

---

## 🧠 Kullanılan Teknolojiler

**Python**: Tüm sistemin ana programlama dili.

**Transformers** (Hugging Face): dbmdz/bert-base-turkish-cased modeli kullanılarak niyet sınıflandırma (intent classification) yapılmıştır.

**PyTorch**: BERT modelinin eğitimi, tensör işlemleri ve çıkarım (inference) süreçlerini yönetmek için kullanılmıştır.

**OpenAI API**: Kullanıcı sorgularına doğal ve akıcı yanıtlar üretmek için GPT mimarisinden faydalanılmıştır.

**Flask & Flask-CORS**: Modelin web üzerinden erişilebilir olmasını sağlayan Backend API yapısı.

**HTML & CSS**: Kullanıcı dostu arayüz tasarımı (Frontend).

**CSV**: Modelin eğitimi için kullanılan 1492 satırlık etiketlenmiş niyet veri seti.

**Matplotlib & Seaborn**: Modelin %98.27 başarı oranını belgeleyen Confusion Matrix ve Loss grafiklerinin görselleştirilmesi.

---

## 📁 Proje Dosya Yapısı

```text
pythonProject4/
│
├── data/
│   └── intents.csv
│      Intent eğitimi için kullanılan CSV veri seti
│
├── models/
│   └── bert_intent/
│      Eğitilmiş BERT modeli ve tokenizer dosyaları
│
├── step1_preprocessing.py
│   Metin temizleme ve ön işleme işlemleri
│
├── step2_nlu.py
│   BERT ile intent tahmini ve confidence hesaplama
│
├── dialog_manager.py
│   Intent ve confidence değerine göre karar mekanizması
│
├── step4_nlg.py
│   GPT tabanlı yanıt üretimi
│
├── step5_logging.py
│   Sohbetlerin dosya tabanlı loglanması
│
├── train_bert_intent.py
│   CSV verisi kullanılarak BERT intent modelinin eğitimi
│
├── app.py
│   Flask API ve chatbot ana akışı
│
├── frontend/
│   └── index.html
│      Chatbot kullanıcı arayüzü
│
├── requirements.txt
│   Projede kullanılan Python kütüphaneleri
│
└── README.md
│   Proje dokümantasyonu
```
---
## 🛠 Kurulum ve Çalıştırma (Yerel)
**1. Gerekli kütüphaneleri yükleyin**
pip install -r requirements.txt

**2. BERT Intent Modelini Eğitin**
python train_bert_intent.py

**3. Flask Sunucusunu Başlatın**
python app.py

---



## 📊MODEL EĞİTİMİ VE VERİ HAZIRLAMA SÜRECİ

-Model eğitimi ve veri hazırlama süreci Python scriptleri kullanılarak
gerçekleştirilmiştir.

-**train_bert_intent.py** dosyasında aşağıdaki adımlar yer almaktadır:

-**CSV formatındaki** veri setinin okunması

-Metinlerin **BERT tokenizer ile tokenize edilmesi**

-Transformer tabanlı BERT intent modelinin eğitilmesi

-Eğitilen model ve tokenizer’ın diske kaydedilmesi
**📈 Elde Edilen Başarı (Validation Results)**
Model, test verileri üzerinde yapılan değerlendirmede şu sonuçları vermiştir:

**Accuracy (Doğruluk): %98.27**

**F1-Score: %98.28**

**AUC Score: 1.00 (Kusursuz sınıflandırma başarısı)**

---

## 🤖 GPT Destekli Yanıt Üretimi

Chatbot, OpenAI API anahtarı tanımlandığında GPT destekli yanıt üretimi
yapmaktadır.

**Kural tabanlı** bilgi cevapları GPT ile daha doğal hale getirilir

Intent güven değeri düşükse veya intent belirlenemezse
**GPT fallback mekanizması** devreye girer

---


## 👩‍💻 Geliştirici
Bu proje, akademik bir çalışma ve kişisel uygulama geliştirme
kapsamında hazırlanmıştır.

---






