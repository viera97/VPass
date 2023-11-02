from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("mobilehomeentry", views.mobilehomeentry, name='mobilehomeentry'),
    path("addentry", views.add_entry, name='addentry'),
    path("editentry", views.editentry, name='editentry'),

    path("configuration", views.configuration, name='configuration'),
    path("securityquestions", views.securityquestions, name="securityquestions"),
    path("encryptdata", views.encryptdata, name="encryptdata"),

    path("singup", views.singup, name='singup'),
    path("singout", views.singout, name='singout'),
    path("singin", views.singin, name='singin'),
    path('delete_data', views.delete_data, name='delete_data'),
    path("restoreaccount", views.restoreaccount, name='restoreaccount'),

    path("check_password_status", views.check_password_status, name='check_password_status'),
    path("genpasword", views.genpasword, name='genpasword'),
    path("otpsecretget", views.otpsecretget, name='otpsecretget'),
    
    path("hom2", views.hom2, name='hom2'),
    path("test", views.test, name='test'),
    path("test2", views.test2, name='test2'),
]