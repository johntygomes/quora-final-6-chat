# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('rooms/<str:roomname>/', views.room, name='room'),
]