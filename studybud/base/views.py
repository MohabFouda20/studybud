from django.shortcuts import render
from .models import Room
# from django.http import HttpResponse


# rooms =[
#     {'id':1 , 'name':'lets learn python'},
#     {'id':2 , 'name':'lets learn js'},
#     {'id':3 , 'name':'lets learn php'},
#     {'id': 4 , 'name' : 'what the heelll'},
# ]

def home(request):
    rooms = Room.objects.all()
    context ={'rooms':rooms}
    return render(request, 'base/home.html' , context )



def room(request,pk):
    room =Room.objects.get(id=pk)
    # for i in rooms:      # before the database and models 
    #     if i['id'] == int (pk):
    #         room =i
    context= {'room':room}
    
    
    return render(request,'base/room.html', context)
# Create your views here.
