from django.urls import path
from . import views, auth

urlpatterns = [
    path('', views.index),
    path('register', auth.register),
    path('login', auth.login),
    path('logout', auth.logout),
    path('travels', views.travels),
    path('addtrip', views.addtrip),
    path('new_travel', views.new_travel),
    path('view/<id>', views.view),
    path('cancel', views.cancel),
    path('delete', views.delete)
]
