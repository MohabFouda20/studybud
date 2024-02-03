from django.shortcuts import render,redirect
from .models import Room
from .forms import RoomForm
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
def CreateRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def updateRoom(request , pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method =='POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request , 'base/room_form.html', context)

def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request ,'base/delete.html', {'obj':room})