from django.contrib import messages
from django.shortcuts import redirect, render
import bcrypt
from .decorators import login_required
from .models import User, Trip 


@login_required
def index(request):

    context = {
        'saludo': 'Hola'
    }
    return render(request, 'index.html', context)


def travels(request):
    trip = Trip.objects.all()
    user = User.objects.all()

    context = {
        'trip': trip,
        'user': user
    }
    return render(request, 'travels.html', context)


def addtrip(request):
    trip = Trip.objects.all()
    user = User.objects.all()

    context = {
        'trip': trip,
        'user': user
    }
    return render(request, 'addtrip.html', context)


def destination(request, id):
    trip = Trip.objects.all()
    user = User.objects.all()

    context = {
        'trip': trip,
        'user': user
    }
    return render(request, 'destination.html', context)



