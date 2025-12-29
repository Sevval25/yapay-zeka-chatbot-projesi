Transformer Tabanlı AI Destekli Chatbot Uygulaması

Bu proje, CSV formatında oluşturulmuş veri seti kullanılarak eğitilen Transformer tabanlı (BERT) bir intent sınıflandırma modeli ve GPT destekli yanıt üretimi içeren AI tabanlı bir chatbot uygulamasıdır.
Chatbot, kullanıcıdan gelen mesajları analiz ederek niyet (intent) tespiti yapmakta ve bağlama uygun yanıtları otomatik olarak üretmektedir.

Uygulama; NLU (Doğal Dil Anlama), Diyalog Yönetimi ve NLG (Doğal Dil Üretimi) adımlarını içeren uçtan uca bir chatbot mimarisi ile geliştirilmiştir.
Frontend tarafı HTML tabanlıdır ve backend ile REST API üzerinden haberleşmektedir.

🎯 Projenin Amacı

Bu projenin temel amaçları şunlardır:

CSV dosyası üzerinden chatbot için veri seti oluşturulması

Transformer tabanlı BERT modeli ile intent sınıflandırmasının öğretilmesi

Kullanıcı mesajlarının doğal dil işleme yöntemleriyle analiz edilmesi

Kural tabanlı bilgi cevaplarının GPT ile daha doğal hale getirilmesi

Belirsiz sorular için GPT destekli fallback mekanizmasının kurulması

Akademik bir proje kapsamında modern NLP tabanlı bir chatbot uygulaması geliştirilmesi

🧠 Kullanılan Teknolojiler

Python

Transformers (Hugging Face) – BERT intent modeli

PyTorch – Model eğitimi ve çıkarım

Flask – Backend API

OpenAI API – GPT tabanlı yanıt üretimi

HTML / CSS / JavaScript – Frontend

CSV – Intent eğitim verisi

📁 Proje Dosya Yapısı
pythonProject4/
│
├── data/
│   └── intents.csv
│     Intent eğitimi için kullanılan CSV veri seti
│
├── models/
│   └── bert_intent/
│     Eğitilmiş BERT modeli ve tokenizer dosyaları
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
│     Chatbot kullanıcı arayüzü
│
├── requirements.txt
│   Projede kullanılan Python kütüphaneleri
│
└── README.md
│   Proje dokümantasyonu

▶️ Uygulamanın Çalıştırılması (Yerel)

Gerekli kütüphaneleri yükleyin:

pip install -r requirements.txt


BERT intent modelini eğitin:

python train_bert_intent.py 
📊 Model Eğitimi ve Veri Hazırlama Süreci Python scriptleri kullanılarak gerçekleştirilmiştir.
train_bert_intent.py dosyasında; CSV formatındaki veri setinin okunması, metinlerin tokenize edilmesi, Transformer tabanlı BERT modelinin eğitilmesi ve eğitilen modelin kaydedilmesi adımları yer almaktadır.
Bu yaklaşım, modelin doğrudan uygulama ortamında yeniden eğitilebilmesini sağlamakta ve projenin üretim (production) mantığına daha uygun bir yapı sunmaktadır.
🤖 GPT Destekli Yanıt Üretimi

Chatbot, OpenAI API anahtarı tanımlandığında GPT destekli yanıt üretimi yapmaktadır.

Kural tabanlı bilgi cevapları GPT ile daha doğal hale getirilir

Intent belirlenemezse GPT fallback mekanizması devreye girer.
👩‍💻 Geliştirici

Bu proje, akademik bir çalışma ve kişisel uygulama geliştirme kapsamında hazırlanmıştır.
Amaç, CSV tabanlı veri kullanımı, Transformer modelleri ve GPT entegrasyonunun bir chatbot uygulamasında birlikte nasıl kullanılabileceğini göstermektir.



Flask sunucusunu başlatın:

python app.py
