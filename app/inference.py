# app/inference.py

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import nltk
nltk.download('punkt')

# Setup device
device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained("gpt2")
tokenizer.add_special_tokens({
    "pad_token": "<pad>",
    "bos_token": "<startofstring>",
    "eos_token": "<endofstring>"
})
tokenizer.add_tokens(["<bot>:"])

# Load model architecture
model = AutoModelForCausalLM.from_pretrained("gpt2")
model.resize_token_embeddings(len(tokenizer))

# Load trained weights
model.load_state_dict(torch.load("app/model_state.pt", map_location=device))
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
    start_idx = decoded.find("<bot>:")
    if start_idx != -1:
        response = decoded[start_idx + len("<bot>"):]
        end_idx = response.find("<endofstring>")
        if end_idx != -1:
            response = response[:end_idx]
        response = response.replace("<startofstring>", "").replace("<pad>", "").strip()
    else:
        response = "Maaf, saya tidak dapat memahami pertanyaan Anda."

    return response
