from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import AudioFile
from .serializers import AudioFileSerializer
from rest_framework.decorators import api_view
from django.http import FileResponse, JsonResponse
import io
# Create your views here.


def index(request):
    return render(request, 'index.html')


@api_view(["POST"])
def send_audio(request):
    if "audio" not in request.FILES:
        return Response({"error": "Aucun fichier reçu"}, status=status.HTTP_400_BAD_REQUEST)

    audio_file = request.FILES["audio"]
    audio_instance = AudioFile.objects.create(file=audio_file)
    
    serializer = AudioFileSerializer(audio_instance)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

from pydub import AudioSegment 
import torch, librosa

# Charger les modèles une seule fois et les garder en mémoire
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
from transformers import pipeline
from pydub import AudioSegment
stt_pipeline = pipeline("automatic-speech-recognition", model="abiyo27/whisper-small-ewe", device=0 if device.type == 'cuda' else -1)

'''
@api_view(["POST"])
def ewe_voice_chat(request):
    """Retourne le même fichier audio reçu."""
    if "audio" not in request.FILES:
        return JsonResponse({"error": "Aucun fichier audio reçu"}, status=400)
    
    audio_file = request.FILES["audio"]
    #audio_bytes = audio_file.read()
    
    out_audio1 = io.BytesIO()
    out_audio = AudioSegment.from_file(io.BytesIO(audio_file.read()))
    out_audio.export(out_audio1, "mp3")
    out_audio1.seek(0)
    #audio, sr = librosa.load(audio_io, sr=16000)
    # Utiliser le modèle STT pour convertir l'audio en texte
    result = stt_pipeline(out_audio1)

    # Extraire le texte reconnu
    recognized_text = result['text']
    print("Recognition:", recognized_text)
    return FileResponse(audio_file, content_type="audio/wav")
'''













from .api import *

# ewe_assistant/views.py
from google.cloud import translate
from google.cloud import translate_v2 as translate
import os
import uuid
from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from .models import Conversation, Message
import speech_recognition as sr
from gtts import gTTS
import os

from google.cloud import translate
from google.cloud import translate_v2 as translate
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./premium-axis-450910-f6-8c3d28f15cef.json"

def translate_text(text: str, target_language: str = "ee"):
    """
    Traduit un texte en Ewe en utilisant Google Cloud Translation API.
    """
    client = translate.Client.from_service_account_json(f'{settings.BASE_DIR}/app/premium-axis-450910-f6-8c3d28f15cef.json')
    result = client.translate(text, target_language=target_language)

    return result["translatedText"]


def ask_ai_voice_to_voice(path):

   # Utilisation du pipeline STT directement à partir de l'audio en mémoire
    text_out = stt_pipeline(path)
    text_out = text_out["text"].split('>')[-1]
    test_ewe_to_fr = translate_text(text_out, target_language='fr')
    chat_response = chat(str(test_ewe_to_fr))
    text_out = translate_text(chat_response, target_language='ee')
    print("Text: ", text_out)

    # Tokenisation de l'entrée
    inputs = tokenizer(text_out, return_tensors="pt").to(device)
    output= ""
    with torch.no_grad():
        output = tts_model(**inputs).waveform

    audio_np = output.squeeze(0).cpu().numpy()
    return audio_np, tts_model.config.sampling_rate


@api_view(['POST'])
def ewe_voice_chat(request):
    """
    Fonction pour gérer les requêtes de chat vocal en langue Ewe
    """
    if 'audio' not in request.FILES:
        return Response({'error': 'Aucun fichier audio fourni'}, status=400)
    
    # Récupère le fichier audio
    audio_file = request.FILES['audio']
    
    # Enregistre temporairement le fichier audio
    file_extension = os.path.splitext(audio_file.name)[1]
    temp_filename = f"temp_{uuid.uuid4()}{file_extension}"
    temp_path = os.path.join(settings.MEDIA_ROOT, temp_filename)
    
    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
    
    with open(temp_path, 'wb+') as destination:
        for chunk in audio_file.chunks():
            destination.write(chunk)
    # Utilise SpeechRecognition pour transcrire l'audio
    transcription = ""

    try:
        result = stt_pipeline(temp_path)
        # Extraire le texte reconnu
        transcription = result['text']
        print("Transcription:  ",transcription)
        
    except Exception as e:
        print(f"Erreur de transcription: {e}")
        transcription = "Désolé, je n'ai pas pu comprendre l'audio."
    
    # Supprimer le fichier temporaire
    try:
        os.remove(temp_path)
    except:
        pass
    
    # Traiter la transcription et générer une réponse
    # Ici, vous pouvez intégrer un modèle de langue ou une API externe
    response_text = generate_response(transcription)
    
    # Générer la réponse audio en Ewe
    audio_url = generate_audio_response(response_text)
    
    # Enregistrer la conversation en base de données
    conversation_id = request.data.get('conversation_id')
    save_messages(conversation_id, transcription, response_text, audio_url)
    
    return Response({
        'transcription': transcription,
        'response': response_text,
        'audio_url': audio_url
    })

@api_view(['POST'])
def ewe_text_chat(request):
    """
    Fonction pour gérer les requêtes de chat textuel en langue Ewe
    """
    data = request.data
    message = data.get('message', '')
    
    if not message:
        return Response({'error': 'Message vide'}, status=400)
    
    # Traiter le message et générer une réponse
    response_text = generate_response(message)
    
    # Générer la réponse audio en Ewe
    audio_url = generate_audio_response(response_text)
    
    # Enregistrer la conversation en base de données
    conversation_id = data.get('conversation_id')
    save_messages(conversation_id, message, response_text, audio_url)
    
    return Response({
        'response': response_text,
        'audio_url': audio_url
    })

@api_view(['GET'])
def get_conversations(request):
    """
    Récupérer la liste des conversations
    """
    conversations = Conversation.objects.all().order_by('-updated_at')
    data = [{'id': conv.id, 'title': conv.title, 'updated_at': conv.updated_at} for conv in conversations]
    return Response(data)

@api_view(['GET'])
def get_conversation_messages(request, conversation_id):
    """
    Récupérer les messages d'une conversation spécifique
    """
    try:
        conversation = Conversation.objects.get(id=conversation_id)
        messages = conversation.messages.all().order_by('created_at')
        data = [{
            'id': msg.id,
            'role': msg.role,
            'content': msg.content,
            'audio_url': msg.audio_file.url if msg.audio_file else None,
            'created_at': msg.created_at
        } for msg in messages]
        return Response({
            'conversation': {
                'id': conversation.id,
                'title': conversation.title,
                'created_at': conversation.created_at
            },
            'messages': data
        })
    except Conversation.DoesNotExist:
        return Response({'error': 'Conversation non trouvée'}, status=404)

@api_view(['POST'])
def create_conversation(request):
    """
    Créer une nouvelle conversation
    """
    title = request.data.get('title', 'Nouvelle conversation')
    conversation = Conversation.objects.create(title=title)
    return Response({
        'id': conversation.id,
        'title': conversation.title,
        'created_at': conversation.created_at
    })

# Fonctions utilitaires
def generate_response(Question):
    """
    Fonction pour générer une réponse à partir d'un message
    Ici vous pouvez intégrer un modèle de langue ou une API externe
    """
    # Exemple d'utilisation
    #Question = "Amekae nye United States of America ƒe dukplɔla fifia?"
    test_ewe_to_fr = translate_text(Question, target_language='fr')
    chat_response = chat(str(test_ewe_to_fr))
    test_fr_to_ewe = translate_text(chat_response, target_language='ee')
    print(f"Texte traduit en Ewe: {test_fr_to_ewe}")
    return  test_fr_to_ewe 

import soundfile as sf

def generate_audio_response(text):
    """
    Fonction pour convertir le texte en audio avec gTTS
    """
    # Créer un nom de fichier unique
    audio_filename = f"response_{uuid.uuid4()}.mp3"
    audio_path = os.path.join(settings.MEDIA_ROOT, 'audio_responses', audio_filename)
    
    # Créer le dossier s'il n'existe pas
    os.makedirs(os.path.dirname(audio_path), exist_ok=True)
    
    # Générer l'audio avec gTTS - utiliser 'fr' si 'ee' n'est pas disponible
    try:
        inputs = tokenizer(text, return_tensors="pt").to(device)

        with torch.no_grad():
            output = tts_model(**inputs).waveform

        audio_np = output.squeeze(0).cpu().numpy()
        sampling_rate = tts_model.config.sampling_rate
        sf.write(audio_path, audio_np, samplerate=sampling_rate, format="MP3")

        """tts = gTTS(text=text, lang='fr', slow=False)
        tts.save(audio_path)"""
        return f"{settings.MEDIA_URL}audio_responses/{audio_filename}"
    except Exception as e:
        print(f"Erreur de génération audio: {e}")
        return None

def save_messages(conversation_id, user_message, assistant_response, audio_url=None):
    """
    Enregistrer les messages dans la base de données
    """
    try:
        # Récupérer ou créer une conversation
        if conversation_id:
            try:
                conversation = Conversation.objects.get(id=conversation_id)
            except Conversation.DoesNotExist:
                conversation = Conversation.objects.create()
        else:
            conversation = Conversation.objects.create()
        
        # Enregistrer le message de l'utilisateur
        Message.objects.create(
            conversation=conversation,
            role='user',
            content=user_message
        )
        
        # Enregistrer la réponse de l'assistant
        audio_file = None
        if audio_url:
            # Extraire le nom du fichier depuis l'URL
            audio_file = audio_url.replace(settings.MEDIA_URL, '')
        
        Message.objects.create(
            conversation=conversation,
            role='assistant',
            content=assistant_response,
            audio_file=audio_file
        )
        
        # Mettre à jour le titre de la conversation si c'est le premier message
        if conversation.messages.count() <= 2:  # 2 nouveaux messages
            # Utiliser le début du message utilisateur comme titre
            title = user_message[:50] + '...' if len(user_message) > 50 else user_message
            conversation.title = title
            conversation.save()
            
        return conversation.id
    except Exception as e:
        print(f"Erreur lors de l'enregistrement des messages: {e}")
        return None






