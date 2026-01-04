import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datasets import Dataset
from transformers import (
    BertTokenizerFast,
    BertForSequenceClassification,
    Trainer,
    TrainingArguments,
    TrainerCallback
)
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, confusion_matrix, roc_curve, auc
from sklearn.preprocessing import label_binarize
import torch
import warnings
import os

# Uyarıları kapat
warnings.filterwarnings('ignore')

# --- AYARLAR ---
MODEL_NAME = "dbmdz/bert-base-turkish-cased"
MODEL_PATH = "models/bert_intent"

# ✅ DÜZELTİLDİ: Artık 'data' klasörünün içindeki intents.csv'ye bakıyor.
DATA_PATH = "data/intents.csv"

print("=" * 70)
print("🚀 BERT Intent Modeli Eğitimi Başlıyor... (Görselleştirmeli)")
print(f"📂 Hedef Veri Yolu: {DATA_PATH}")
print("=" * 70)

# 1) Veri yükle
print("\n📂 Veri yükleniyor...")
try:
    df = pd.read_csv(DATA_PATH)
    # Label sütunu int değilse çevir
    df["label"] = df["label"].astype(int)
    print(f"✅ Toplam {len(df)} örnek yüklendi")
except FileNotFoundError:
    print(f"❌ HATA: '{DATA_PATH}' dosyası bulunamadı!")
    print("Lütfen projenin içinde 'data' klasörü olduğundan ve içinde 'intents.csv' olduğundan emin olun.")
    exit()

# 2) Train/Val böl
print("\n🔀 Veri bölünüyor...")
train_df, val_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df["label"])

train_dataset = Dataset.from_pandas(train_df)
val_dataset = Dataset.from_pandas(val_df)

# 3) Tokenizer
print("\n🔤 Tokenizer yükleniyor...")
tokenizer = BertTokenizerFast.from_pretrained(MODEL_NAME)


def tokenize(batch):
    return tokenizer(
        batch["text"],
        padding="max_length",
        truncation=True,
        max_length=64
    )


train_dataset = train_dataset.map(tokenize, batched=True)
val_dataset = val_dataset.map(tokenize, batched=True)

# Sütun isimlerini torch formatına hazırla
train_dataset = train_dataset.rename_column("label", "labels")
val_dataset = val_dataset.rename_column("label", "labels")
train_dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "labels"])
val_dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "labels"])

# 4) Model ve Sabitler
print("\n🤖 Model yükleniyor...")
# constants dosyasından ID2LABEL çekiliyor
try:
    from constants import ID2LABEL
except ImportError:
    print("❌ HATA: 'constants.py' dosyası bulunamadı. Lütfen aynı dizinde olduğundan emin olun.")
    exit()

LABEL2ID = {v: k for k, v in ID2LABEL.items()}
num_labels = len(ID2LABEL)

model = BertForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=num_labels,
    id2label=ID2LABEL,
    label2id=LABEL2ID
)


# 5) Metrik Hesaplama Fonksiyonu (F1 ve AUC Eklendi)
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = logits.argmax(axis=-1)

    # Softmax ile olasılıkları al (AUC için gerekli)
    def softmax(x):
        e_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        return e_x / e_x.sum(axis=1, keepdims=True)

    probs = softmax(logits)

    # Temel Metrikler
    acc = accuracy_score(labels, preds)
    f1 = f1_score(labels, preds, average="weighted")

    # AUC Hesaplama (Hata verirse 0 dön)
    try:
        roc_auc = roc_auc_score(labels, probs, multi_class='ovr', average='weighted')
    except:
        roc_auc = 0.0

    return {"accuracy": acc, "f1": f1, "auc": roc_auc}


# 6) Eğitim Argümanları
training_args = TrainingArguments(
    output_dir=MODEL_PATH,
    per_device_train_batch_size=8,
    num_train_epochs=15,
    save_strategy="no",
    eval_strategy="epoch",
    logging_steps=5,
    report_to="none",
    use_cpu=True
)

# 7) Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    compute_metrics=compute_metrics
)

# 8) Eğitim Başlat
print("\n🎯 Eğitim başlıyor...")
trainer.train()

# Modeli kaydet
model.save_pretrained(MODEL_PATH)
tokenizer.save_pretrained(MODEL_PATH)

# --- GÖRSELLEŞTİRME KISMI ---
print("\n📊 Grafikler hazırlanıyor...")

# Tahminleri al
predictions = trainer.predict(val_dataset)
preds = np.argmax(predictions.predictions, axis=-1)
labels = predictions.label_ids
probs = torch.nn.functional.softmax(torch.tensor(predictions.predictions), dim=-1).numpy()

# A) Confusion Matrix
try:
    plt.figure(figsize=(10, 8))
    cm = confusion_matrix(labels, preds)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=ID2LABEL.values(),
                yticklabels=ID2LABEL.values())
    plt.title('Confusion Matrix (Hata Matrisi)')
    plt.ylabel('Gerçek Etiket')
    plt.xlabel('Tahmin Edilen')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('confusion_matrix.png')
    print("✅ 'confusion_matrix.png' kaydedildi.")
except Exception as e:
    print(f"⚠️ Grafik hatası: {e}")

# B) ROC Eğrisi
try:
    plt.figure(figsize=(10, 8))
    y_test_bin = label_binarize(labels, classes=list(ID2LABEL.keys()))
    n_classes = y_test_bin.shape[1]

    for i in range(n_classes):
        fpr, tpr, _ = roc_curve(y_test_bin[:, i], probs[:, i])
        roc_auc = auc(fpr, tpr)
        plt.plot(fpr, tpr, label=f'{ID2LABEL[i]} (AUC = {roc_auc:.2f})')

    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Eğrisi')
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig('roc_curve.png')
    print("✅ 'roc_curve.png' kaydedildi.")
except Exception as e:
    print(f"⚠️ Grafik hatası: {e}")

# C) Loss Grafiği
try:
    history = trainer.state.log_history
    loss_values = [x['loss'] for x in history if 'loss' in x]
    epochs_list = range(1, len(loss_values) + 1)

    if loss_values:
        plt.figure(figsize=(8, 5))
        plt.plot(epochs_list, loss_values, 'b-o', label='Training Loss')
        plt.title('Eğitim Kayıp Grafiği')
        plt.xlabel('Adım')
        plt.ylabel('Loss')
        plt.legend()
        plt.savefig('training_loss.png')
        print("✅ 'training_loss.png' kaydedildi.")
except Exception as e:
    print(f"⚠️ Grafik hatası: {e}")

print("\n" + "=" * 70)
print(f"🎉 İşlem Tamam! F1 Score: {predictions.metrics['test_f1']:.4f}")
print("Grafikler oluşturuldu.")
print("=" * 70)
