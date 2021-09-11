from django.contrib import messages
from django.shortcuts import redirect, render
import bcrypt
from .decorators import login_required
from .models import User, Trip 
import datetime 




def index(request):
    if request.method == "POST":
        user = User.objects.filter(username=request.POST['user'])
    if user:
        log_user = user[0]

        if bcrypt.checkpw(request.POST['password'].encode(), log_user.password.encode()):

            user = {
                "id" : log_user.id,
                "user": f"{log_user}",
                }

            request.session['user'] = user
            messages.success(request, "Logueado correctamente.")
            return redirect("/travels")
        else:
            messages.error(request, "Usuario o password incorrectos.")
    else:
        messages.error(request, "Usuario o password incorrectos.")




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

    return redirect(request, "/travels")



def join(request, id):

    trip = Trip.objects.get(id=id)
    user = User.objects.get(id=request.session['user']['id'])  
    trip.travellers.add(user)

    messages.success(request, "Te uniste a un viaje")

    return redirect('/travels')


