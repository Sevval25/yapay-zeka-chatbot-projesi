import torch
import torch.nn.functional as F
from transformers import BertTokenizerFast, BertForSequenceClassification

MODEL_PATH = "models/bert_intent"

tokenizer = BertTokenizerFast.from_pretrained(MODEL_PATH)
model = BertForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()

# Label id → intent adı
ID2LABEL = {
    0: "get_shipping_info",
    1: "get_discount_info",
    2: "get_campaign_info",
    3: "get_price_info",
    4: "get_availability_info",
    5: "support",
    6: "fallback"
}

def predict_intent_bert(text: str):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=64
    )

    with torch.no_grad():
        outputs = model(**inputs)

    logits = outputs.logits
    probs = F.softmax(logits, dim=1)

    confidence, predicted_id = torch.max(probs, dim=1)

    intent = ID2LABEL[predicted_id.item()]
    confidence = confidence.item()

    return intent, confidence
