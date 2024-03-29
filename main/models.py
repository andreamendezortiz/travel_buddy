from django.db import models
import re
from datetime import date, datetime

# Create your models here.
class UserManager(models.Manager):
    def validador_basico(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        SOLO_LETRAS = re.compile(r'^[a-zA-Z. ]+$')

        errors = {}

        if len(postData['username']) < 3:
            errors['username_len'] = "usuario debe tener al menos 3 caracteres de largo";

        if len(postData['password']) < 8:
            errors['password'] = "contraseña debe tener al menos 8 caracteres";

        if postData['password'] != postData['password_confirm'] :
            errors['password_confirm'] = "contraseña y confirmar contraseña no son iguales. "

        
        return errors


class User(models.Model):
    CHOICES = (
        ("user", 'User'),
        ("admin", 'Admin')
    )
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=70)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return f"{self.username}"

    def __repr__(self):
        return f"{self.username}"


class TripManager(models.Manager):
    def validador_basico(self, postData):
        errors = {}
        
        if len(postData['destination']) < 1:
            errors['destination_len'] = "Debes agregar un destino"
        if len(postData['description']) < 1:
            errors['description_len'] = "Debes agregar un plan"
        if (postData['travel_date_from']) == "":
            errors['travel_date_from'] = "Debes agregar la fecha de inicio del viaje"
        if (postData['travel_date_to']) == "":
            errors['travel_date_to'] = "Debes agregar la fecha de término del viaje"

        return errors



class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    travel_date_from = models.DateTimeField()
    travel_date_to = models.DateTimeField()
    travellers = models.ManyToManyField(User,related_name="other_trips")
    creator = models.ForeignKey(User, related_name="my_trips", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()

    def __str__(self):
        return f"{self.destination} {self.id}"

    def __repr__(self):
        return f"{self.destination} {self.id}"


