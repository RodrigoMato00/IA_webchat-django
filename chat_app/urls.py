from django.urls import path
from . import views

urlpatterns = [
    #path('', views.chat_with_url, name='chat_with_url'),
    path('chat-interface/', views.chat_interface_view, name="chat_interface_view"),
    path('login/', views.LoginView.as_view(), name='login'),
    path('chat-api/', views.chat_api_view, name='chat_api_view'),
]
