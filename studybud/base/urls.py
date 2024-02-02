from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.home , name= 'home'),
    path ('room/<str:pk>/', views.room , name = 'room'),
    path('CreateRoom/', views.CreateRoom, name='create_room'),
]
