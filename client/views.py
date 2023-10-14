from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from cryptography.fernet import Fernet

import re
import os

from . import passwd
from .models import Questions
from . import encryptions

global user_number
user_number = 1

def mobile(request):
    MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
    
    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        return True
    else:
        return False
    
def init(request):
    theme = 'dark'
    theme = 'light'

    language = 'Spanish'
    language = 'English'

    is_mobile = mobile(request)

    if request.COOKIES.get('theme'):
        theme = request.COOKIES.get('theme')
    
    if request.COOKIES.get('language'):
        language = request.COOKIES.get('language')

    if request.method == 'GET':
        if request.GET.get('theme') == 'dark':
            theme = 'dark'
        elif request.GET.get('theme') == 'light':
            theme = 'light'

        if request.GET.get('language') == 'English':
            language = 'English'
        elif request.GET.get('language') == 'Spanish':
            language = 'Spanish'
    
    if len(Questions.objects.all()) != 0:
        questions = Questions.objects.first()

        if not questions.encrypted:
            try:
                key = encryptions.load_key('secure_key')
                secanwser0 = questions.secanwser0
                secanwser0 = encryptions.encrypt(secanwser0, key)
                questions.secanwser0 = secanwser0

                secanwser1 = questions.secanwser1
                secanwser1 = encryptions.encrypt(secanwser1, key)
                questions.secanwser1 = secanwser1

                secanwser2 = questions.secanwser2
                secanwser2 = encryptions.encrypt(secanwser2, key)
                questions.secanwser2 = secanwser2

                questions.encrypted = True

                questions.save()
                
            except:
                pass
            
    return theme, language, is_mobile

def handle_uploaded_file(f): 
	with open('client/Uploads/'+f.name, 'wb+') as destination: 
		for chunk in f.chunks(): 
			destination.write(chunk) 

def singup(request):
    theme, language, is_mobile = init(request)

    error_dic = {}
    refill = {}
    
    if request.method == 'POST':
        if not 'username' in request.POST:
            if language == "English":
                error_dic['username'] = "The username can't be empty"
            else:
                error_dic['username'] = "El nombre de usuario no puede ser vacío"
        else:
            if request.POST['username'] == '':
                if language == "English":
                    error_dic['username'] = "The username can't be empty"
                else:
                    error_dic['username'] = "El nombre de usuario no puede ser vacío"
            else:
                username = request.POST['username']
        if not 'password1' in request.POST:
            if language == "English":
                error_dic['password1'] = "The password can't be empty"
            else:
                error_dic['password1'] = "La contraseña no puede ser vacía"
        else:
            if request.POST['password1'] == '':
                if language == "English":
                    error_dic['password1'] = "The password can't be empty"
                else:
                    error_dic['password1'] = "La contraseña no puede ser vacía"
            else:
                password1 = request.POST['password1']
        if not 'password2' in request.POST:
            if language == "English":
                error_dic['password2'] = "You have to repeat the password"
            else:
                error_dic['password2'] = "Tienes que repetir la contraseña"
        else:
            if request.POST['password2'] == '':
                if language == "English":
                    error_dic['password2'] = "You have to repeat the password"
                else:
                    error_dic['password2'] = "Tienes que repetir la contraseña"
            else:
                password2 = request.POST['password2']
                if 'password1' in request.POST and 'password2' in request.POST:
                    if password1 != password2:
                        if language == "English":
                            error_dic['password2'] = "The passwords don't match"
                        else:
                            error_dic['password2'] = "Las contraseñas no coinciden"
                    else:
                        if not passwd.check_pass(password1):
                            if language == "English":
                                error_dic['password2'] = "Password should be at least 8 characters, should contain upper and lower characters, symbols and numbers"
                            else:
                                error_dic['password2'] = "La contraseña debe ser de al menos 8 caractéres, debe conterner letras mayúsculas y minúsculas, símbolos y números"

        if len(error_dic) != 0:
            if not 'username' in error_dic:
                refill['username'] = username

        else:
            user = User.objects.create_user(username=username, password=password1)

    if len(User.objects.all()) == user_number:
        user_bool = False
    else:
        user_bool = True

    if not user_bool:
        context = {
            'title':'SingUp',
            'error_dic':error_dic,
            'refill':refill,
            'theme':theme,
            'language':language,
            'is_mobile':is_mobile
        }
        
        response = render(request, 'Pages/singup.html', context)
        response.set_cookie(key='theme', value=theme)
        response.set_cookie(key='language', value=language)
        return response
    
    return redirect("singin")

def singin(request):
    theme, language, is_mobile = init(request)

    error_dic = {}
    refill = {}

    if request.method == 'POST':
        if not 'username' in request.POST:
            if language == "English":
                error_dic['username'] = "The username can't be empty"
            else:
                error_dic['username'] = "El nombre de usuario no puede ser vacío"
        else:
            if request.POST['username'] == '':
                if language == "English":
                    error_dic['username'] = "The username can't be empty"
                else:
                    error_dic['username'] = "El nombre de usuario no puede ser vacío"
            else:
                if len(User.objects.filter(username=request.POST['username'])) == 0:
                    if language == "English":
                        error_dic['username'] = "There is no user with this Username"
                    else:
                        error_dic['username'] = "No hay usuario con este nombre de usuario"
                else:
                    username = request.POST['username']

        if not 'password' in request.POST:
            if language == "English":
                error_dic['password'] = "The password can't be empty"
            else:
                error_dic['password'] = "La contraseña no puede ser vacía"
        else:
            if request.POST["password"] == "":
                if language == "English":
                    error_dic['password'] = "The password can't be empty"
                else:
                    error_dic['password'] = "La contraseña no puede ser vacía"
            else:
                password = request.POST['password']

        if len(error_dic) != 0:
            if not 'username' in error_dic:
                refill['username'] = username
        else:
            try:
                user = authenticate(request, username=username, password=password)
                login(request, user)
                return redirect("/")
            except:
                if language == "English":
                    error_dic['password'] = "Incorrect password"
                else:
                    error_dic['password'] = "Contraseña incorrecta"

    if len(User.objects.all()) == user_number:
        user_bool = False
    else:
        user_bool = True

    if request.user.is_authenticated:
        return redirect("/")
    
    context = {
            'title':'SingIn',
            'error_dic':error_dic,
            'refill':refill,
            'theme':theme,
            'language':language,
            'user_bool':user_bool,
            'is_mobile':is_mobile
    }    
    
    response = render(request, 'Pages/singin.html', context)
    response.set_cookie(key='theme', value=theme)
    response.set_cookie(key='language', value=language)
    return response

def singout(request):
    logout(request)
    return redirect("singup")

def hom2(request):
    theme = init(request)

    context = {
        'title':'Home',
        'theme':theme,
    }    

    response = render(request, 'Pages/hom2.html', context)
    response.set_cookie(key='theme', value=theme)
    return response

def home(request):
    theme, language, is_mobile = init(request)

    if not request.user.is_authenticated:
        return redirect("singin")

    context = {
        'title':'Home',
        'theme':theme,
        'language':language,
        'is_mobile':is_mobile,
    }

    response = render(request, 'Pages/home.html', context)
    response.set_cookie(key='theme', value=theme)
    response.set_cookie(key='language', value=language)
    return response

def configuration(request):
    theme, language, is_mobile = init(request)

    if not request.user.is_authenticated:
        return redirect("singin")

    context = {
        'title':'Configuration',
        'theme':theme,
        'language':language,
        'is_mobile':is_mobile
    }

    response = render(request, 'Pages/configuration.html', context)
    response.set_cookie(key='theme', value=theme)
    response.set_cookie(key='language', value=language)
    return response

def encryptdata(request):
    theme, language, is_mobile = init(request)

    key = ""
    error_dic = {}

    if request.method == "GET":
        if request.GET.get("generate"):
            if request.GET.get("generate") == "True":
                encryptions.write_key("secure_key_aux")
                key = encryptions.load_key("secure_key_aux")
                key = str(key).split("'")[1]
                
        
        if request.GET.get("delete_key"):
            if request.GET.get("delete_key") == "True":
                os.remove('secure_key')
    
    if request.method == "POST":
        if 'key' in request.POST:
            key = encryptions.load_key("secure_key_aux")
            encryptions.write_final_key(key)
            os.remove("secure_key_aux")
        
        else:
            if "inputfile" in request.FILES:
                encryptions.save_key_from_file(request.FILES["inputfile"])
                key = encryptions.load_key("secure_key_aux")
                try:
                    Fernet(key)
                    encryptions.write_final_key(key)
                    os.remove("secure_key_aux")
                except:
                    if language == "English":
                        error_dic['file'] = "Incorrect file"
                    else:
                        error_dic['file'] = "Archivo incorrecto"
            else:
                if "pastekey" in request.POST:
                    key = request.POST["pastekey"]
                    encryptions.write_key_paste("secure_key_aux", key)
                    key = encryptions.load_key("secure_key_aux")
                    try:
                        Fernet(key)
                        os.remove("secure_key_aux")
                        encryptions.write_final_key(key)
                    except:
                        if language == "English":
                            error_dic['pastekey'] = "The key is not valid"
                        else:
                            error_dic['pastekey'] = "La llave no es válida"
                    """
                    try:
                        Fernet(key)
                        f = open('secure_key', 'w')
                        f.write(key)
                        f.close()

                    except:
                        if language == "English":
                            error_dic['pastekey'] = "The key must be a 35 lenght key"
                        else:
                            error_dic['pastekey'] = "La llave debe ser de 35 caracteres"
                    """

    if not request.user.is_authenticated:
        return redirect("singin")
    
    try:
        f = open('secure_key', 'r')
        f.close()
        stored_key = True
    except:
        stored_key = False

    context = {
        'title':'Configuration',
        'theme':theme,
        'language':language,
        'is_mobile':is_mobile,
        'key':key,
        'error_dic':error_dic,
        'stored_key':stored_key
    }

    response = render(request, 'Pages/encryptdata.html', context)
    response.set_cookie(key='theme', value=theme)
    response.set_cookie(key='language', value=language)
    return response

def securityquestions(request):
    theme, language, is_mobile = init(request)

    questionnumber = 1
    disabledquestions = []
    error_dic = {}

    total_anwser = ''
    total_question = ''
    success = ''
    porcent = 0
    already = False

    if request.method == 'POST':
        if 'question' in request.POST:
            question = request.POST['question']
            if request.POST['anwser'] == "":
                error_dic['anwser'] = "The anwser can't be empty"
            else:
                cont = 0
                for i in request.POST['anwser'].split(' '):
                    if i == "":
                        cont += 1
                if cont == len(request.POST['anwser'].split(' ')):
                    error_dic['anwser'] = "The anwser can't be empty"

                else:
                    anwser = request.POST['anwser']
                    total_question = request.POST['total_question']
                    total_anwser = request.POST['total_anwser']
                    questionnumber = int(request.POST['questionnumber'])+1

            if len(error_dic) == 0:
                total_question += question+';'
                total_anwser += anwser+';'
                for i in total_question.split(';'):
                    disabledquestions.append(i)

                if questionnumber == 2:
                    porcent = 40

                if questionnumber == 3:
                    porcent = 80

                if questionnumber == 4:
                    porcent = 100

        else:
            total_question = request.POST['total_question']
            total_anwser = request.POST['total_anwser']

            total_question = total_question.split(';')
            total_anwser = total_anwser.split(';')

            user = request.user
            try:
                question = Questions(secquestions0=total_question[0], secanwser0 = total_anwser[0],
                                     secquestions1=total_question[1], secanwser1 = total_anwser[1],
                                     secquestions2=total_question[2], secanwser2 = total_anwser[2],
                                     From_User = user)
                question.save()
                success = True
            except:
                success = False

            questionnumber = 5
            porcent = 100
            

    if not request.user.is_authenticated:
        return redirect("singin")

    if not request.method == 'POST':
        if len(Questions.objects.filter(From_User=request.user)) != 0:
            already = True

    context = {
        'title':'Configuration',
        'theme':theme,
        'language':language,
        'questionnumber':questionnumber,
        'error_dic':error_dic,
        'disabledquestions':disabledquestions,
        'total_anwser':total_anwser,
        'total_question':total_question,
        'porcent':porcent,
        'success':success,
        'already':already,
        'is_mobile':is_mobile

    }

    response = render(request, 'Pages/securityquestions.html', context)
    response.set_cookie(key='theme', value=theme)
    response.set_cookie(key='language', value=language)
    return response