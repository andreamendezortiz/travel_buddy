from django.urls import path
from . import views, auth

urlpatterns = [
    path('', views.index),
    path('register', auth.register),
    path('login', auth.login),
    path('logout', auth.logout),
    path('travels', views.travels),
    path('addtrip', views.addtrip),
    path('travels/destination/<id>', views.destination)
]
