from django.shortcuts import render

# Create your views here.
def room(request,roomname):
  print(roomname)
  context = {
    "roomname": roomname
  }
  return render(request, 'chat/room.html',context)
