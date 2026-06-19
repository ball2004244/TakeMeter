"""
app.py — TakeMeter deployed interface

Loads the fine-tuned DistilBERT classifier and serves a Gradio UI that
accepts a r/QuantumComputing post and returns the predicted label + confidence.

Setup:
    1. Download takemeter-model/checkpoint-104 from Colab and place it at ./model/
    2. pip install gradio transformers torch
    3. python app.py
"""

import os
import torch
import gradio as gr
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_PATH = "./model"
MAX_LENGTH = 384

LABEL_MAP = {"news": 0, "discussion": 1, "question": 2}
ID_TO_LABEL = {v: k for k, v in LABEL_MAP.items()}

LABEL_DESCRIPTIONS = {
    "news":       "Shares an external announcement, paper, or industry development.",
    "discussion": "Poster has a take or claim they want the community to debate.",
    "question":   "Poster lacks understanding and wants an explanation.",
}

if not os.path.isdir(MODEL_PATH):
    raise FileNotFoundError(
        f"Model not found at '{MODEL_PATH}'. "
        "Download checkpoint-104 from Colab and place it at ./model/"
    )

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
model = model.to("cpu")
model.eval()


def classify(post_text: str):
    if not post_text or not post_text.strip():
        return "—", {label: 0.0 for label in LABEL_MAP}

    inputs = tokenizer(
        post_text,
        return_tensors="pt",
        truncation=True,
        max_length=MAX_LENGTH,
        padding=True,
    )
    with torch.no_grad():
        logits = model(**inputs).logits

    probs = torch.softmax(logits, dim=-1)[0]
    pred_id = int(probs.argmax())
    pred_label = ID_TO_LABEL[pred_id]
    confidence = float(probs[pred_id])

    scores = {ID_TO_LABEL[i]: float(probs[i]) for i in range(len(LABEL_MAP))}

    summary = f"{pred_label}  —  {confidence:.1%} confidence\n{LABEL_DESCRIPTIONS[pred_label]}"
    return summary, scores


demo = gr.Interface(
    fn=classify,
    inputs=gr.Textbox(
        label="r/QuantumComputing post",
        placeholder="Paste a post title or title + body here…",
        lines=5,
    ),
    outputs=[
        gr.Textbox(label="Prediction", lines=2),
        gr.Label(label="Confidence scores", num_top_classes=3),
    ],
    title="TakeMeter",
    description=(
        "Fine-tuned DistilBERT classifier for r/QuantumComputing posts.\n"
        "Labels: **news** · **discussion** · **question**"
    ),
    examples=[
        ["QpiAI Achieves High-Speed Quantum Error Correction on Superconducting Systems"],
        ["When will SC qubits start to die off?"],
        ["Why don't we just perform another transform in the Fourier basis after QFT?"],
        ["Critique of Microsoft\n\nhttps://arxiv.org/abs/2502.19560\n\nThoughts?"],
        ["When will we have Quantum Computing for general purpose compute?\n\nWhat I mean is that we have some quantum computing already and available through the cloud in some cases. But those quantum computers are very specific purpose machines."],
    ],
)

if __name__ == "__main__":
    demo.launch()
