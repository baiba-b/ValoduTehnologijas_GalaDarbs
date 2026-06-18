import pandas as pd
import numpy as np

from datasets import Dataset
from sklearn.metrics import accuracy_score, f1_score

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments
)

MODEL_NAME = "AiLab-IMCS-UL/lvbert"

DATA_PATH = "data/manual_emotion_labels.csv"

LABELS = [
    "anger",
    "disgust",
    "fear",
    "joy",
    "neutral",
    "sadness",
    "surprise"
]

label2id = {label: i for i, label in enumerate(LABELS)}
id2label = {i: label for label, i in label2id.items()}


# Ielādē datus
df = pd.read_csv(DATA_PATH)

df = df[["sentence", "manual_label"]].dropna()

df["label"] = df["manual_label"].map(label2id)

dataset = Dataset.from_pandas(
    df[["sentence", "label"]]
)

dataset = dataset.train_test_split(
    test_size=0.2,
    seed=42
)


# LV-BERT
tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=len(LABELS),
    id2label=id2label,
    label2id=label2id
)


# Tokenizācija
def tokenize(batch):
    return tokenizer(
        batch["sentence"],
        truncation=True,
        padding="max_length",
        max_length=128
    )

dataset = dataset.map(
    tokenize,
    batched=True
)

dataset = dataset.remove_columns(
    ["sentence"]
)

dataset.set_format("torch")


# Metrika
def compute_metrics(eval_pred):

    logits, labels = eval_pred

    predictions = np.argmax(
        logits,
        axis=1
    )

    return {
        "accuracy": accuracy_score(
            labels,
            predictions
        ),
        "macro_f1": f1_score(
            labels,
            predictions,
            average="macro"
        )
    }


# Treniņš
training_args = TrainingArguments(
    output_dir="models/lvbert",
    eval_strategy="epoch",
    save_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=5,
    weight_decay=0.01
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    compute_metrics=compute_metrics
)


# Apmācība
trainer.train()


# Novērtēšana
results = trainer.evaluate()

print("\nLV-BERT rezultāti:")
print(results)


# Saglabā modeli
trainer.save_model(
    "models/lvbert_final"
)

tokenizer.save_pretrained(
    "models/lvbert_final"
)