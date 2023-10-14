from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name='home'),

    path("configuration", views.configuration, name='configuration'),
    path("securityquestions", views.securityquestions, name="securityquestions"),
    path("encryptdata", views.encryptdata, name="encryptdata"),

    path("singup", views.singup, name='singup'),
    path("singout", views.singout, name='singout'),
    path("singin", views.singin, name='singin'),

    path("hom2", views.hom2, name='hom2'),
]