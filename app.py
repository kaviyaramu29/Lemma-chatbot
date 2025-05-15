from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os
from dotenv import load_dotenv
load_dotenv()


app = FastAPI()

# Enable CORS so frontend can talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Hugging Face access token (required for gated models)
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_HUB_TOKEN")  # Set this in your environment

# Load Gemma model from Hugging Face
MODEL_ID = "google/gemma-1.1-2b-it"

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, use_auth_token=HUGGINGFACE_TOKEN)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float16,
    device_map="auto",
    use_auth_token=HUGGINGFACE_TOKEN
)

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "")

    # Gemma is a base model, so use simple prompt style
    prompt = f"<start_of_turn>user\n{user_message}<end_of_turn>\n<start_of_turn>model\n"

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=100,
        temperature=0.7,
        do_sample=True,
        top_p=0.9,
        repetition_penalty=1.1
    )

    response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Extract model's reply only
    response_only = response_text[len(prompt):].strip()

    return {"response": response_only}
