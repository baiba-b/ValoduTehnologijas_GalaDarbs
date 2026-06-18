import pandas as pd
import numpy as np
from datasets import Dataset
from sklearn.metrics import accuracy_score, f1_score
from transformers import (
    BertConfig,
    BertTokenizerFast,
    BertForSequenceClassification,
    Trainer,
    TrainingArguments
)

DATA_PATH = "data/manual_emotion_labels.csv"

LABELS = ["anger", "disgust", "fear", "joy", "neutral", "sadness", "surprise"]
label2id = {label: i for i, label in enumerate(LABELS)}
id2label = {i: label for label, i in label2id.items()}

df = pd.read_csv(DATA_PATH)
df = df[["sentence", "manual_label"]].dropna()
df["label"] = df["manual_label"].map(label2id)

dataset = Dataset.from_pandas(df[["sentence", "label"]])
dataset = dataset.train_test_split(test_size=0.2, seed=42)

# Izmanto BERT tokenizatora vārdnīcu, bet modeļa svari ir nejauši (netrenēts no nulles)
tokenizer = BertTokenizerFast.from_pretrained("bert-base-multilingual-cased")

def tokenize(batch):
    return tokenizer(
        batch["sentence"],
        truncation=True,
        padding="max_length",
        max_length=128
    )

dataset = dataset.map(tokenize, batched=True)
dataset = dataset.remove_columns(["sentence"])
dataset.set_format("torch")

config = BertConfig(
    vocab_size=tokenizer.vocab_size,
    hidden_size=128,
    num_hidden_layers=2,
    num_attention_heads=2,
    intermediate_size=256,
    num_labels=len(LABELS),
    id2label=id2label,
    label2id=label2id
)

model = BertForSequenceClassification(config)

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=1)

    return {
        "accuracy": accuracy_score(labels, predictions),
        "macro_f1": f1_score(labels, predictions, average="macro")
    }

training_args = TrainingArguments(
    output_dir="models/bert_from_scratch",
    eval_strategy="epoch",
    save_strategy="epoch",
    learning_rate=5e-4,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=20,
    weight_decay=0.01,
    logging_dir="logs"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    compute_metrics=compute_metrics
)

trainer.train()
print(trainer.evaluate())

trainer.save_model("models/bert_from_scratch_final")
tokenizer.save_pretrained("models/bert_from_scratch_final")