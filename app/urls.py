
from django.contrib import admin
from django.urls import path, include
from .views import *
urlpatterns = [
 
    path('', index, name='index'),
    path('send_audio/', send_audio, name='send_audio'),
    
    path('ewe_voice_chat/', ewe_voice_chat, name='ewe_voice_chat'),
    path('ewe_text_chat/', ewe_text_chat, name='ewe_text_chat'),
    path('conversations/', get_conversations, name='get_conversations'),
    path('conversation/<int:conversation_id>/', get_conversation_messages, name='get_conversation_messages'),
    path('conversation/create/', create_conversation, name='create_conversation'),

]
