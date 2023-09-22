from django.shortcuts import render, redirect
import requests
from bs4 import BeautifulSoup
from langchain.llms import OpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain.schema import BaseOutputParser

from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from drf_yasg.openapi import Schema, TYPE_STRING, TYPE_OBJECT, IN_QUERY, Parameter
from rest_framework import serializers, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from urllib.parse import urlparse

from requests.sessions import Session


from django.contrib.auth.models import User

import numpy as np

# Parsea la salida de una llamada a LLM a una lista separada por comas
class CommaSeparatedListOutputParser(BaseOutputParser):
    def parse(self, text: str):
        """Parse the output of an LLM call."""
        return text.strip().split(", ")

#validacion de la url
def is_valid_url(url):
    try:
        print(url)
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

# Version uno
def chat_with_url(request):

    if 'chat_record' not in request.session:
        request.session['chat_record'] = {'url': '', 'conversations': []}

    if request.method == "POST":
        url = request.POST.get('url', '')
        user_message = request.POST.get('user_message', '')

        if not user_message:
            return render(request, 'chat_page.html', {'chat_record': request.session['chat_record']})

        if url != request.session['chat_record']['url']:
            request.session['chat_record'] = {'url': url, 'conversations': []}

        try:
            if not is_valid_url(url):
                chat_response = "Por favor, proporciona una URL válida."

            else:
                print ('pasamos url: ', url)
                response = requests.get(url, timeout=10)
                soup = BeautifulSoup(response.content, 'html.parser')
                chat_content = soup.get_text()

                template = f"You are an assistant aware of the content from the website at URL: {url}. The content of the website is: '{chat_content}'. Answer user questions based on this content."
                human_template = user_message

                chat_prompt = ChatPromptTemplate.from_messages([
                    ("system", template),
                    ("human", human_template),
                ])

                chain = chat_prompt | OpenAI(openai_api_key='TOKEN_OPEN_AI') | CommaSeparatedListOutputParser()
                chat_response = chain.invoke({"url": url, "user_message": user_message})

        except Exception as e:
            chat_response = f"Error: {str(e)}"

        request.session['chat_record']['conversations'].append({
            'question': user_message,
            'answer': chat_response
        })
        request.session.modified = True

        return render(request, 'chat_page.html', {'chat_record': request.session['chat_record']})

    return render(request, 'url_input.html')

## Logica del chat con la url
def chat_logic(url, user_message):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        chat_content = soup.get_text()

        template = f"You are an assistant aware of the content from the website at URL: {url}. The content of the website is: '{chat_content}'. Answer user questions based on this content."
        human_template = user_message

        chat_prompt = ChatPromptTemplate.from_messages([
            ("system", template),
            ("human", human_template),
        ])

        chain = chat_prompt | OpenAI(openai_api_key='TOKEN_OPEN_AI') | CommaSeparatedListOutputParser()
        chat_response = chain.invoke({"url": url, "user_message": user_message})

        return chat_response, None

    except Exception as e:
        return None, str(e)

# def chat_with_url(request):
#     if 'chat_record' not in request.session:
#         request.session['chat_record'] = {'url': '', 'conversations': []}

#     if request.method == "POST":
#         url = request.POST.get('url', '')
#         user_message = request.POST.get('user_message', '')

#         if not user_message:
#             return render(request, 'chat_page.html', {'chat_record': request.session['chat_record']})

#         if url != request.session['chat_record']['url']:
#             request.session['chat_record'] = {'url': url, 'conversations': []}

#         chat_response, error = chat_logic(url, user_message)

#         if error:
#             chat_response = f"Error: {error}"

#         request.session['chat_record']['conversations'].append({
#             'question': user_message,
#             'answer': chat_response
#         })
#         request.session.modified = True

#         return render(request, 'chat_page.html', {'chat_record': request.session['chat_record']})

#     return render(request, 'url_input.html')

# vista para la interfaz del chat
def chat_interface(request):
    return render(request, 'chat_interface.html')

# se usa para setear el user agent y simular que es un navegador
def set_default_user_agent():
    default_headers = requests.utils.default_headers()
    default_headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    })
    Session().headers.update(default_headers)

# vista que contiene la logica para el web chat
def chat_interface_view(request):
    current_url = request.POST.get('url', None)
    previous_url = request.session.get('previous_url', None)
    chat_history = request.session.get('chat_history', [])

    if current_url != previous_url:
        chat_history = []
        request.session['previous_url'] = current_url

    user_message = request.POST.get('user_message', None)

    if current_url and user_message:
        if is_valid_url(current_url):
            set_default_user_agent()
            chat_response, error = chat_logic(current_url, user_message)
            chat_history.append(("You", user_message))
            if chat_response:
                chat_history.append(("Response", chat_response))
            if error:
                chat_history.append(("Error", error))
            request.session['chat_history'] = chat_history
        else:
            error = "Please provide a valid URL and a message."

    return render(request, 'chat_interface.html', {
        'messages': chat_history,
        'url': current_url
    })


#serializador para los parametros de entrada
class ChatSerializer(serializers.Serializer):
    url = serializers.URLField()
    user_message = serializers.CharField()
#swagger
@swagger_auto_schema(
    method='post',
    operation_description="Chat with a given URL",
    request_body=ChatSerializer,
    responses={
        200: Schema(type=TYPE_OBJECT, properties={
            'question': Schema(type=TYPE_STRING, description='User provided question'),
            'answer': Schema(type=TYPE_STRING, description='Answer generated from the chat')
        }),
        400: 'Error message',
        500: 'Error message'
    },
)
@api_view(['POST'])
@parser_classes([JSONParser])
@permission_classes([IsAuthenticated])
# vista para el chat con la api
def chat_api_view(request):
    authentication_classes = [TokenAuthentication]
    serializer = ChatSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    url = serializer.validated_data.get('url')
    user_message = serializer.validated_data.get('user_message')

    if not url or not user_message:
        return Response({'error': 'URL and user_message fields are required.'}, status=400)

    chat_response, error = chat_logic(url, user_message)

    if error:
        return Response({'error': error}, status=500)

    return Response({
        'question': user_message,
        'answer': chat_response
    }, status=200)


######## sector autenticacion ########
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class LoginView(ObtainAuthToken):
    # This view is used to login the user
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        # This method is used to post the login data
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user_serialized = UserSerializer(user)
        return Response({'token': token.key, 'user': user_serialized.data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@swagger_auto_schema(
    operation_description="Obtener usuario a partir del token",
    responses={200: UserSerializer()}
)
# vista para obtener el usuario a partir del token
def get_user_from_token(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)