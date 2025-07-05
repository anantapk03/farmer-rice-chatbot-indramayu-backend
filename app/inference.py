# app/inference.py

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import nltk
nltk.download('punkt')

# Setup device
device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"

# Ganti dengan nama repo kamu di Hugging Face
base_model = "anantapk03/gpt2-chatbot-indramayu-farmer-rice-10kdata"

# Load model dan tokenizer langsung dari Hugging Face
tokenizer = AutoTokenizer.from_pretrained(base_model)
model = AutoModelForCausalLM.from_pretrained(base_model)
model.resize_token_embeddings(len(tokenizer))
model.to(device)
model.eval()

def generate_response(prompt: str, max_new_tokens: int = 150) -> str:
    input_text = f"<startofstring> {prompt} <bot>:"
    inputs = tokenizer(input_text, return_tensors='pt', padding=True).to(device)

    with torch.no_grad():
        output = model.generate(
            input_ids=inputs['input_ids'],
            attention_mask=inputs['attention_mask'],
            max_new_tokens=max_new_tokens,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id
        )

    decoded = tokenizer.decode(output[0], skip_special_tokens=False)

    # Ekstrak respons dari token khusus
    start_idx = decoded.find("<bot>:")
    if start_idx != -1:
        response = decoded[start_idx + len("<bot>"):].split("<endofstring>")[0]
        response = response.replace("<startofstring>", "").replace("<pad>", "").strip()
    else:
        response = "Maaf, saya tidak dapat memahami pertanyaan Anda."

    return response
