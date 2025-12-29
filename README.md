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

- **Python**
- **Transformers (Hugging Face)** – BERT intent modeli
- **PyTorch** – Model eğitimi ve çıkarım
- **Flask** – Backend API
- **OpenAI API** – GPT tabanlı yanıt üretimi
- **HTML** – Frontend
- **CSV** – Intent eğitim verisi

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

▶️ Uygulamanın Çalıştırılması (Yerel)
1. Gerekli kütüphaneleri yükleyin
pip install -r requirements.txt

2. BERT Intent Modelini Eğitin
python train_bert_intent.py

3. Flask Sunucusunu Başlatın
python app.py





---
