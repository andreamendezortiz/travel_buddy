from django.contrib import messages
from django.shortcuts import redirect, render
import bcrypt
from .decorators import login_required
from .models import User, Trip 
from datetime import date



@login_required
def travels(request):
    user = request.session['user']
    user_id = request.session['user']['id']
    my_trips = Trip.objects.filter(creator = user_id)
    traveller = User.objects.get(id=request.session['user']['id'])
    other_trips = Trip.objects.exclude(travellers = traveller).all
    trips = Trip.objects.filter(travellers=traveller).all()


    context = {
        'traveller' : traveller,
        'user': user,
        'my_trips': my_trips,
        'other_trips' : other_trips,
        'trips' : trips
    }
    return render(request, 'travels.html', context)



@login_required
def addtrip(request):
    trip = Trip.objects.all()
    user = User.objects.all()

    context = {
        'trip': trip,
        'user': user
    }
    return render(request, 'addtrip.html', context)



@login_required
def view(request, id):
    trip = Trip.objects.get(id=id)
    user = request.session['user']
    travellers = trip.travellers.all()

    context = {
        'trip': trip,
        'user': user,
        'travellers': travellers
    }
    return render(request, 'view.html', context)


@login_required
def new_travel(request):
    if request.method == 'GET':

        return render(request,'addtrip.html')
    
    errors = Trip.objects.validador_basico(request.POST)

    if len(errors) > 0:
            for key, error_msg in errors.items():
                messages.error(request, error_msg)
            return redirect('/new_travel')

    user = request.session['user']
    destination = request.POST['destination']
    description = request.POST['description']
    travel_date_from = request.POST['travel_date_from']
    travel_date_to = request.POST['travel_date_to']
    user_id = request.session['user']['id']
    traveller = User.objects.get(id=user_id)

    new_travel = Trip.objects.create(destination = destination, description = description, travel_date_from = travel_date_from, travel_date_to = travel_date_to, creator_id = user_id)

    messages.success(request, f'Agregaste un nuevo viaje')
    return redirect("/travels")


@login_required
def cancel(request, id):
    user = request.session['user']
    user_id = request.session['user']['id']
    trip = Trip.objects.get(id=id)
    trip.remove(user)

    messages.warning(request, "Cancelaste tu participación en el viaje indicado")

    return redirect("/travels")


@login_required
def delete(request, id):
    trip = Trip.objects.get(id=id)
    trip.delete()

    messages.warning(request, "Eliminaste el viaje indicado")

    return redirect("/travels")


@login_required
def join(request, id):

    trip = Trip.objects.get(id = id)
    user = User.objects.get(id=request.session['user']['id'])  
    trip.travellers.add(user)

    messages.success(request, "Te uniste a un viaje")

    return redirect('/travels')


