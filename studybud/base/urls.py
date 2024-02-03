from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.home , name= 'home'),
    path ('room/<str:pk>/', views.room , name = 'room'),
    path('CreateRoom/', views.CreateRoom, name='create-room'),
    path('updateRoom/<str:pk>/', views.updateRoom, name='update-room'),
    path('deleteRoom/<str:pk>/', views.deleteRoom, name='delete-room'),
]
