from transformers import VitsModel, AutoTokenizer
import torch
import scipy
import numpy as np
from transformers import pipeline

from openai import AzureOpenAI
from os import environ


import os, openai
from openai import AzureOpenAI
# Remplace par le chemin de ton fichier JSON de service account

# Charger les modèles une seule fois et les garder en mémoire
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
tts_model = VitsModel.from_pretrained("facebook/mms-tts-ewe").to(device)
tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-ewe")
stt_pipeline = pipeline("automatic-speech-recognition", model="abiyo27/whisper-small-ewe", device=0 if device.type == 'cuda' else -1)


AZURE_EMBEDDING_ENDPOINT="https://realtimekokou.openai.azure.com/openai/deployments/text-embedding-3-large/embeddings?api-version=2023-05-15"
AZURE_EMBEDDING_API_KEY="h5R1YOBt2Q5WU56488stKWc7GiO9nEG3Z344ITLK3mTb6uGkdlKLJQQJ99BAACYeBjFXJ3w3AAABACOGLM5j"
AZURE_CHAT_ENDPOINT="https://chatlearning.openai.azure.com/openai/deployments/gpt-35-turbo/chat/completions?api-version=2024-08-01-preview"
AZURE_CHAT_API_KEY="6xv3rz6Asc5Qq86B8vqjhKQzSTUZPmCcSuDm5CLEV5dj9m8gTHlNJQQJ99AKACYeBjFXJ3w3AAABACOGyHXT"
open_client = AzureOpenAI(
        api_key=AZURE_CHAT_API_KEY,
        api_version="2023-12-01-preview",
        azure_endpoint=AZURE_CHAT_ENDPOINT
    )

def chat(question):
    # Appel à l'API GPT
    chat_completion = open_client.chat.completions.create(
        model="gpt-35-turbo",
        messages=[
            {"role": "system", "content": "vous une IA qui peut comprendre et repondre "},
            {"role": "user", "content": question},
        ]
    )

    response = chat_completion.choices[0].message.content
    return response
