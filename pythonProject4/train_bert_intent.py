import pandas as pd
import torch
from datasets import Dataset
from transformers import (
    BertTokenizerFast,
    BertForSequenceClassification,
    Trainer,
    TrainingArguments
)

MODEL_NAME = "dbmdz/bert-base-turkish-cased"
MODEL_PATH = "models/bert_intent"
DATA_PATH = "data/intents.csv"

# Data yükle
df = pd.read_csv(DATA_PATH)
dataset = Dataset.from_pandas(df)

tokenizer = BertTokenizerFast.from_pretrained(MODEL_NAME)

def tokenize(batch):
    return tokenizer(
        batch["text"],
        padding="max_length",
        truncation=True,
        max_length=32
    )

dataset = dataset.map(tokenize, batched=True)
dataset = dataset.rename_column("label", "labels")
dataset.set_format("torch", columns=["input_ids", "attention_mask", "labels"])

model = BertForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=len(df["label"].unique())
)

training_args = TrainingArguments(
    output_dir=MODEL_PATH,
    per_device_train_batch_size=8,
    num_train_epochs=6,
    logging_steps=10,
    save_strategy="epoch",
    report_to="none"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset
)

trainer.train()

# 🔥 MODEL VE TOKENIZER KAYDET
trainer.save_model(MODEL_PATH)
tokenizer.save_pretrained(MODEL_PATH)

print("✅ BERT intent modeli başarıyla eğitildi ve kaydedildi")
