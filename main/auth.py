from django.contrib import messages
from django.shortcuts import redirect, render
import bcrypt
from .models import User


def logout(request):
    if 'user' in request.session:
        del request.session['user']
    
    return redirect("/login")
    

def login(request):
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
                messages.error(request, "Usuario o Email  incorrectos.")
        else:
            messages.error(request, "Usuario o password incorrectos.")



        return redirect("/login")
    else:
        return render(request, 'login.html')


def register(request):
    if request.method == "POST":
        errors = User.objects.validador_basico(request.POST)
        # print(errors)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            
            request.session['register_username'] =  request.POST['username']

        else:
            request.session['register_username'] = ""

            password_encryp = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode() 

            usuario_nuevo = User.objects.create(
                username = request.POST['username'],
                password=password_encryp,
            )

            messages.success(request, "El usuario fue agregado con exito.")
            

            request.session['user'] = {
                "id" : usuario_nuevo.id,
                "username": f"{usuario_nuevo.username}"
            }
            return redirect("/")

        return redirect("/register")
    else:
        return render(request, 'register.html')
