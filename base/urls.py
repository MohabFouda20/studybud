from django.urls import path,include
from . import views

urlpatterns = [
    path('Login/', views.loginpage, name='login'),
    path('logout/', views.logoutuser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('', views.home , name= 'home'),
    
    path ('room/<str:pk>/', views.room , name = 'room'),
    path ('profile/<str:pk>/', views.userProfile , name = 'user-profile'),
    
    
    
    
    path ('UpdateUser/', views.updateUser , name = 'update-user'),
    path ('topics/', views.topicsPage , name = 'topics-page'),
    path ('activity/', views.activityPage , name = 'activity-page'),
    
    
    
    path('CreateRoom/', views.CreateRoom, name='create-room'),
    path('updateRoom/<str:pk>/', views.updateRoom, name='update-room'),
    path('deleteRoom/<str:pk>/', views.deleteRoom, name='delete-room'),
    path('deletemessage/<str:pk>/', views.deleteMessage, name='delete-message'),
]
