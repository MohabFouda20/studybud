from django.shortcuts import render,redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Room, Topic , Message , User
from .forms import RoomForm ,UserForm ,mUserCreation
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login ,logout
from django.contrib import messages
from django.http import HttpResponse

def loginpage(request):
    page = 'login'
    
    
    if request.user.is_authenticated :
        return redirect('home')
    
    if request.method=='POST':
        email = request.POST.get('email')#.lower()
        password= request.POST.get('password')
        try :
            user=User.objects.get(email=email)
        except:
            messages.error(request , 'user does not exist .')
        
        user = authenticate(request , email=email , password=password)
        if user is not None :
            login(request, user)   
            return redirect('home') 
        else :
            messages.error(request , 'username or Password is not correct')
            
    context={'page':page}
    return render(request, 'base/login_rig.html', context)


def logoutuser(request):
    
    logout(request)
    return redirect('home')


def registerPage(request):
    form = mUserCreation()
    if request.method== 'POST':
        form = mUserCreation(request.POST)
        if form.is_valid():
            user= form.save(commit =False)
            user.username = user.username.lower()
            user.save()
            login(request , user)
            return redirect('home')
        else :
            messages.error(request , 'An error happened during registration')   
            
    return render(request ,'base/login_rig.html', {'form': form} )

def home(request):
    
    q= request.GET.get('q')if request.GET.get('q')!=None else ''
    rooms = Room.objects.filter(
    Q(topic__name__icontains=q)|
    Q(name__icontains=q)|
    Q(description__icontains=q)
    )
    topics =Topic.objects.all()[0:5]
    
    rooms_count=rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    
    
    context ={'rooms':rooms, 'topics':topics , 'rooms_count':rooms_count  , 'room_messages' :room_messages}
    return render(request, 'base/home.html' , context )



def room(request,pk):
    room =Room.objects.get(id=pk)
    body = request.POST.get('body')
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body= body
        )
        room.participants.add(request.user)
        return redirect('room' , pk=room.id)
    
    
    context= {'room':room ,'room_messages': room_messages ,'participants':participants }
    return render(request,'base/room.html', context)


def userProfile(request ,pk):
    user = User.objects.get(id=pk)
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    
    rooms = user.room_set.all()
    context ={'user':user ,'rooms':rooms ,'room_messages' : room_messages , 'topics':topics}
    return render(request , 'base/profile.html' , context)



@login_required(login_url= 'login')
def CreateRoom(request):
    form = RoomForm()
    topics= Topic.objects.all()
    if request.method == 'POST':
        topic_name= request.POST.get('topic')
        topic , created = Topic.objects.get_or_create(name =topic_name)
        Room.objects.create(
            host = request.user,
            topic = topic , 
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        return redirect('home')
    
    
    
    
    # old way in creating old room
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit= False)
        #     room.host =request.user
        #     room.save()
        #     return redirect('home')
        
        
        
    context = {'form': form , 'topics' :topics}
    return render(request, 'base/room_form.html', context)



@login_required(login_url= 'login')
def updateRoom(request , pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics= Topic.objects.all()
    if request.user!= room.host:
        return HttpResponse('you are not the creator for this room')
        
        
    
    if request.method =='POST':
        topic_name= request.POST.get('topic')
        topic , created = Topic.objects.get_or_create(name =topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect ('home')
        
        
        
        # form = RoomForm(request.POST, instance=room)
        # if form.is_valid():
        #     form.save()
        #     return redirect('home')
    context = {'form':form , 'topics' :topics , 'room':room}
    return render(request , 'base/room_form.html', context)


@login_required(login_url= 'login')
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.user!= room.host and not request.user.is_superuser :
        return HttpResponse('you are not allowed')
    
    
    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request ,'base/delete.html', {'obj':room})

@login_required(login_url= 'login')
def deleteMessage(request,pk):
    message=Message.objects.get(id=pk)
    if request.user!= message.user:
        return HttpResponse('you are not allowed')
    
    
    if request.method=='POST':
        message.delete()
        return redirect('home')
    return render(request ,'base/delete.html', {'obj':message})

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm( instance=user )
    if request.method == 'POST':
        form = UserForm(request.POST , request.FILES , instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile' , pk = user.id)
    
    context = { 'form' : form} 
    return render(request  , 'base/edit-user.html' , context)


def topicsPage(request):
    q= request.GET.get('q')if request.GET.get('q')!=None else ''
    topics = Topic.objects.filter(name__icontains=q)
    
    
    return render(request , 'base/topics.html' ,{'topics':topics})

def activityPage(request):
    room_messages = Message.objects.all()
    
    
    return render(request , 'base/activity.html' ,{'room_messages' : room_messages})