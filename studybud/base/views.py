from django.shortcuts import render
# from django.http import HttpResponse


rooms =[
    {'id':1 , 'name':'lets learn python'},
    {'id':2 , 'name':'lets learn js'},
    {'id':3 , 'name':'lets learn php'},
    {'id': 4 , 'name' : 'what the heelll'},
]

def home(request):
    return render(request, 'home.html' , {'rooms' : rooms } )



def room(request,pk):
    return render(request,'room.html')
# Create your views here.
