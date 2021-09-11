from django.contrib import messages
from django.shortcuts import redirect, render
import bcrypt
from .decorators import login_required
from .models import User, Trip 
import datetime




def index(request):

    return render(request, 'login.html')



def travels(request):
    user = request.session['user']
    user_id = request.session['user']['id']
    my_trips = Trip.objects.filter(creator = user_id)
    travellers = User.objects.get(id=user_id)
    trips = Trip.objects.filter(travellers = user_id)

    context = {
        'travellers' : travellers,
        'user': user,
        'my_trips': my_trips,
        'trips' : trips
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




def view(request, id):
    trip = Trip.objects.get(id=id)
    user = request.session['user']

    context = {
        'trip': trip,
        'user': user
    }
    return render(request, 'view.html', context)


def new_travel(request):
    user = request.session['user']
    destination = request.POST['destination']
    description = request.POST['description']
    travel_date_from = datetime.datetime.strptime(request.POST['travel_date_from'], "%Y-%m-%d").date()
    travel_date_to = datetime.datetime.strptime(request.POST['travel_date_to'], "%Y-%m-%d").date()
    user_id = request.session['user']['id']
    traveller = User.objects.get(id=user_id)

    new_travel = Trip.objects.create(destination = destination, description = description, travel_date_from = travel_date_from, travel_date_to = travel_date_to, creator_id = user_id)

    messages.success(request, f'Agregaste un nuevo viaje')
    return redirect("/travels")



def cancel(request, id):
    user = request.session['user']
    user_id = request.session['user']['id']
    trip = Trip.objects.get(id=id)
    trip.delete()



    return redirect("/travels")


def delete(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    trip.delete()

    return redirect("/travels")




