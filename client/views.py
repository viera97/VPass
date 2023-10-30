from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from cryptography.fernet import Fernet

import re
import os

from . import passwd
from .models import Questions, Entries, Incorrectban
from . import encryptions

#Number of users
global user_number
user_number = 1

#Geting if the devices is a mobile
def mobile(request):
    MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)
    
    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        return True
    else:
        return False

#Initializing coockies and encryptions
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
    
    try:
        if len(Incorrectban.objects.all()) == 0:
            incorrectban = Incorrectban(0)
            incorrectban.save()
    except:
        pass
    
    questionall = False

    try:
        if len(Questions.objects.all()) != 0:
            questionall = True
    except:
        questionall = False

    if questionall:
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

#Handle Uploads
def handle_uploaded_file(f): 
	with open('client/Uploads/'+f.name, 'wb+') as destination: 
		for chunk in f.chunks(): 
			destination.write(chunk) 

#HTML VIEWS
#-----------------------------------
#Views for handling logins
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

    if not len(User.objects.all()) == user_number:
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

                if len(Incorrectban.objects.all()) != 0:
                    incorrectban = Incorrectban.objects.first()
                    incorrectban.cont = 0
                    incorrectban.save()

                return redirect("/")
            except:
                if language == "English":
                    error_dic['password'] = "Incorrect password"
                else:
                    error_dic['password'] = "Contraseña incorrecta"

    if not len(User.objects.all()) == user_number:
        user_bool = False
    else:
        user_bool = True
    
    if not user_bool:
        return redirect("singup")
    
    if request.user.is_authenticated:
        return redirect("/")
    
    if Incorrectban.objects.all().first().cont == 2:
        delete = True
    else:
        delete = False

    context = {
            'title':'SingIn',
            'error_dic':error_dic,
            'refill':refill,
            'theme':theme,
            'language':language,
            'user_bool':user_bool,
            'is_mobile':is_mobile,
            'delete':delete
    }
    
    response = render(request, 'Pages/singin.html', context)
    response.set_cookie(key='theme', value=theme)
    response.set_cookie(key='language', value=language)
    return response

def check_password_status(request):
    try:
        if request.method == "GET":
            password = request.GET.get('pass')
            if not passwd.check_pass(password):
                return HttpResponse('insecure')
            else:
                #Hacer
                return HttpResponse('secure')
    except:
        return HttpResponse('None')
    
def genpasword(request):
    try:
        if request.method == "GET":
            number = request.GET.get('pass')
            password = passwd.generate(int(number))
            return HttpResponse(password)
    except:
        return HttpResponse('None')
    
def delete_data(request):
    theme, language, is_mobile = init(request)

    deleted = False

    if request.method == 'GET':
        if request.GET.get('delete_data') == "True":
            Entries.objects.all().delete()
            Questions.objects.all().delete()
            Incorrectban.objects.all().delete()
            User.objects.all().first().delete()
            
            try:
                f = open('secure_key', 'r')
                f.close()
                stored_key = True
            except:
                stored_key = False

            if stored_key:
                os.remove('secure_key')
                
            deleted = True


    if request.user.is_authenticated:
        return redirect("/")
    
    context = {
            'title':'Clean Data',
            'theme':theme,
            'language':language,
            'is_mobile':is_mobile,
            'deleted':deleted
    }

    response = render(request, 'Pages/delete_data.html', context)
    response.set_cookie(key='theme', value=theme)
    response.set_cookie(key='language', value=language)
    return response

def restoreaccount(request):
    theme, language, is_mobile = init(request)

    empty = False
    question = ''
    questions_check = ''
    p = 1
    restored = False

    incorrect = 0

    if request.method == "POST":
        if 'language' in request.POST:
            language = request.POST['language']

        if 'p' in request.POST:
            p = int(request.POST['p'])

    if language == "English":
        questions_dic = {
            "Q0":"Place you want to visit.",
            "Q1":"Name of your first pet.",
            "Q2":"City were you born.",
            "Q3":"Favorite Movie.",
            "Q4":"Sport you practice or like the most.",
            "Q5":"Name of your best childhood friend.",
            "Q6":"Name of the first book you read.",
            "Q7":"Food you prefer.",
            "Q8":"Your mother's maiden name.",
            "Q9":"Musical instrument you know how to play or would like to learn.",
        }
    else:
        questions_dic = {
            "Q0":"Lugar que quieres visitar.",
            "Q1":"Nombre de tu primera mascota.",
            "Q2":"Ciudad donde naciste.",
            "Q3":"Pelicula Favorita.",
            "Q4":"Deporte que practicas o te gusta más.",
            "Q5":"Nombre de tu mejor amigo/a de la infancia.",
            "Q6":"Nombre del primer libro que leíste.",
            "Q7":"Comida que prefieres.",
            "Q8":"Apellido de soltera de tu madre.",
            "Q9":"Instrumento musical que sabes tocar o te gustaría aprender.",
        }
    
    error_dic = {}

    if request.user.is_authenticated:
        return redirect("/")
    
    if len(Questions.objects.all()) == 0:
        empty = True

    if not empty:
        questions = Questions.objects.first()
        if p == 1:
            question = questions_dic[questions.secquestions0]
        elif p == 2:
            question = questions_dic[questions.secquestions1]
        elif p == 3:
            question = questions_dic[questions.secquestions2]

    if request.method == "POST":
        if "anwser" in request.POST:
            anwser = request.POST['anwser']
            cont = 0
            for i in anwser.split(' '):
                if i == "":
                    cont += 1
            if cont == len(anwser.split(' ')):
                if language == "English":
                    error_dic['anwser'] = "The anwser can't be empty."
                else:
                    error_dic['anwser'] = "La respuesta no puede ser vacía."
            else:
                if p == 1:
                    realanwser = questions.secanwser0.lower()
                elif p == 2:
                    realanwser = questions.secanwser1.lower()
                elif p == 3:
                    realanwser = questions.secanwser2.lower()
            
                if anwser.lower() != realanwser:
                    incorrect = int(request.POST['incorrect']) + 1
                    print(incorrect)
                    if incorrect == 1:
                        if language == "English":
                            error_dic['anwser'] = 'Incorrect anwser. You have one more try'
                        else:
                            error_dic['anwser'] = 'Respuesta incorrecta. Tienes otro intento'

                    elif incorrect == 2:
                        if language == "English":
                            error_dic['anwser'] = 'Incorrect anwser.'
                        else:
                            error_dic['anwser'] = 'Respuesta incorrecta.'

                        incorrectban = Incorrectban.objects.all().first()
                        incorrectban.cont = int(incorrectban.cont) + 1
                        incorrectban.save()

                else:
                    p = p+1

                    questions = Questions.objects.first()
                    if p == 1:
                        question = questions_dic[questions.secquestions0]
                    elif p == 2:
                        question = questions_dic[questions.secquestions1]
                    elif p == 3:
                        question = questions_dic[questions.secquestions2]
                    elif p == 4:
                        questions_check = True

        else:
            if "questions_check" in request.POST:
                password1 = request.POST['password1']
                if not passwd.check_pass(password1):
                    if language == "English":
                        error_dic['password'] = "Password should be at least 8 characters, should contain upper and lower characters, symbols and numbers"
                    else:
                        error_dic['password'] = "La contraseña debe ser de al menos 8 caractéres, debe contener mayúsculas y minúsculas, símbolos y números"
                else:
                    password2 = request.POST['password2']
                    if password1 != password2:
                        if language == "English":
                            error_dic['password'] = "Passwords do not match"
                        else:
                            error_dic['password'] = "Las contraseñas no coinciden"
                    else:
                        user = Questions.objects.all().first().From_User
                        user.set_password(password1)
                        user.save()
                        questions_check = True
                        restored = True

            else:
                if language == "English":
                    error_dic['anwser'] = "The anwser can't be empty."
                else:
                    error_dic['anwser'] = "La respuesta no puede ser vacía."

    incorrectban = Incorrectban.objects.all().first()


    if len(Questions.objects.all()) != 0:
        user = Questions.objects.all().first().From_User
    else:
        user = ''

    context = {
            'title':'Restore Password',
            'theme':theme,
            'language':language,
            'is_mobile':is_mobile,
            'empty':empty,
            'question':question,
            'p':p,
            'error_dic':error_dic,
            'incorrect':incorrect,
            'incorrectban':incorrectban,
            'questions_check':questions_check,
            'user':user,
            'restored':restored
    }

    response = render(request, 'Pages/restoreaccount.html', context)
    return response

def singout(request):
    logout(request)
    return redirect("singup")

def home(request):
    theme, language, is_mobile = init(request)

    search = ''
    emptysearch = False

    if not request.user.is_authenticated:
        return redirect("singin")

    entries = Entries.objects.all()

    if len(entries) == 0:
        empty = True
    else:
        empty = False

    entryidbool = False

    if request.method == 'GET':
        entryid = request.GET.get('entryid')
        try:
            entryid = int(entryid)
            entryidbool = True
        except:
            entryidbool = False
        
        if entryidbool:
            selectedentry = Entries.objects.filter(id=entryid)
            if len(selectedentry) == 0:
                entryidbool = False
            else:
                selectedentry = selectedentry.first()
                if request.GET.get('search'):
                    search = request.GET.get('search')
                    if 'search' != '':
                        entries = Entries.objects.filter(name__icontains = search) | Entries.objects.filter(username__icontains = search) | Entries.objects.filter(url__icontains = search)
                        if len(entries) == 0:
                            emptysearch = True
                        else:
                            emptysearch = False
        else:
            if request.GET.get('delete'):
                entryid = request.GET.get('delete')
                try:
                    entryid = int(entryid)
                    entryidbool = True
                except:
                    entryidbool = False

                if entryidbool:
                    if len(Entries.objects.filter(id=entryid)) != 0:
                        deleteentry = Entries.objects.filter(id=entryid).first()
                        deleteentry.delete()
                        entryidbool = False
                        entries = Entries.objects.all()

    if request.method == 'POST':
        if 'search' in request.POST:
            search = request.POST['search']
            if not empty:
                entries = Entries.objects.filter(name__icontains = search) | Entries.objects.filter(username__icontains = search) | Entries.objects.filter(url__icontains = search)
                selectedentry = entries.first()
                entryidbool = True
                if len(entries) == 0:
                    emptysearch = True
                else:
                    emptysearch = False


    if entryidbool:
        context = {
            'title':'Home',
            'theme':theme,
            'language':language,
            'is_mobile':is_mobile,
            'empty':empty,
            'entries':entries,
            'selectedentry':selectedentry,
            'search':search,
            'emptysearch':emptysearch
        }

    else:
        context = {
            'title':'Home',
            'theme':theme,
            'language':language,
            'is_mobile':is_mobile,
            'empty':empty,
            'entries':entries,
            'search':search,
            'emptysearch':emptysearch
        }

    response = render(request, 'Pages/home.html', context)
    response.set_cookie(key='theme', value=theme)
    response.set_cookie(key='language', value=language)
    return response

def mobilehomeentry(request):
    theme, language, is_mobile = init(request)

    selectedentry = ''
    search = ''

    if not request.user.is_authenticated:
        return redirect("singin")
    
    if request.method == "GET":

        if request.GET.get('entryid'):
            entryid = request.GET.get('entryid')
            try:
                entryid = int(entryid)
                entryidbool = True
            except:
                entryidbool = True

            if entryidbool:
                if len(Entries.objects.filter(id=entryid)) != 0:
                    selectedentry = Entries.objects.filter(id=entryid).first()
                    empty = False
                    if request.GET.get('search'):
                        search = request.GET.get('search')
                else:
                    empty = True

        if request.GET.get('delete'):
            deleteentry = request.GET.get('delete')

            try:
                deleteentry = int(deleteentry)
                entryidbool = True
            except:
                entryidbool = False
            
            if entryidbool:
                if len(Entries.objects.filter(id=deleteentry)) != 0:
                    deleteentry = Entries.objects.filter(id=deleteentry).first()
                    deleteentry.delete()
                    return redirect("/")
                
    context = {
            'title':'Home mobile',
            'theme':theme,
            'language':language,
            'is_mobile':is_mobile,
            'selectedentry':selectedentry,
            'empty':empty,
            'search':search
        }
    
    response = render(request, 'Pages/mobilehomeentry.html', context)
    response.set_cookie(key='theme', value=theme)
    response.set_cookie(key='language', value=language)
    return response

def editentry(request):
    theme, language, is_mobile = init(request)

    if not request.user.is_authenticated:
        return redirect("singin")
    
    entryidbool = False
    state = False
    search = ''
    error_dic = {}

    if request.method == 'GET':
        if request.GET.get('entry'):
            selectedentry = request.GET.get('entry')
            try:
                selectedentry = int(selectedentry)
                if len(Entries.objects.filter(id=selectedentry)) != 0:
                    entryidbool = True
                else:
                    entryidbool = False
            except:
                entryidbool = False

            if entryidbool:
                selectedentry = Entries.objects.filter(id=selectedentry).first()
            
            if request.GET.get("state"):
                if request.GET.get("state") == "mobilehomeentry":
                    state = True
                else:
                    state = False
                    
            if request.GET.get('search'):
                search = request.GET.get('search')

    if request.method == 'POST':
        if 'state' in request.POST:
            if request.POST['state'] == "True":
                state = True
            else:
                state = False

        if 'entry' in request.POST:
            entry = request.POST['entry']

            try:
                entry = int(entry)
                if len(Entries.objects.filter(id=entry)) != 0:
                    entryidbool = True
                else:
                    entryidbool = False

            except:
                entryidbool = False
            
            if entryidbool:
                selectedentry = Entries.objects.filter(id=entry).first()

        if 'search' in request.POST:
            search = request.POST['search']
        
        if not 'name' in request.POST:
            if language == "English":
                error_dic['name'] = "The name can't be empty"
            else:
                error_dic['name'] = "El nombre no puede ser vacío"
        else:
            name = request.POST['name']
            if name == "":
                if language == "English":
                    error_dic['name'] = "The name can't be empty"
                else:
                    error_dic['name'] = "El nombre no puede ser vacío"
            else:
                cont = -1
                for i in name.split(" "):
                    if i == "":
                        cont += 1

                if len(name) == cont:
                    if language == "English":
                        error_dic['name'] = "The name can't be empty"
                    else:
                        error_dic['name'] = "El nombre no puede ser vacío"

        username = request.POST['username']
        if username == "":
            if language == "English":
                error_dic['username'] = "The username can't be empty"
            else:
                error_dic['username'] = "El nombre de usuario no puede ser vacío"
        else:
            cont = -1
            for i in username.split(" "):
                if i == "":
                    cont += 1

            if len(username) == cont:
                if language == "English":
                    error_dic['username'] = "The username can't be empty"
                else:
                    error_dic['username'] = "El nombre de usuario no puede ser vacío"
        
        password = request.POST['password']
        if password == "":
            if language == "English":
                error_dic['password'] = "The password can't be empty"
            else:
                error_dic['password'] = "La contraseña no puede ser vacía"
        else:
            cont = -1
            for i in password.split(" "):
                if i == "":
                    cont += 1
            
            if len(password) == cont:
                if language == "English":
                    error_dic['password'] = "The password can't be empty"
                else:
                    error_dic['password'] = "La contraseña no puede ser vacía"
        
        url = request.POST['url']
        if url == "":
            if language == "English":
                error_dic['url'] = "The url can't be empty"
            else:
                error_dic['url'] = "La url no puede ser vacía"
        else:
            cont = -1
            for i in url.split(" "):
                if i == "":
                    cont += 1
            
            if len(url) == cont:
                if language == "English":
                    error_dic['url'] = "The url can't be empty"
                else:
                    error_dic['url'] = "La url no puede ser vacía"
        
        selectedentry_aux = {}
        selectedentry_aux['id']=selectedentry.id

        if not "name" in error_dic:
            selectedentry_aux['name'] = name
        else:
            selectedentry_aux['name'] = selectedentry.name

        if not 'username' in error_dic:
            selectedentry_aux['username'] = username
        else:
            selectedentry_aux['username'] = selectedentry.username
        
        if not 'password' in error_dic:
            selectedentry_aux['password'] = password
        else:
            selectedentry_aux['password'] = selectedentry.password
        
        if not 'url' in error_dic:
            selectedentry_aux['url'] = url
        else:
            selectedentry_aux['url'] = selectedentry.url

        selectedentry = selectedentry_aux

        if len(error_dic) == 0:
            entry = Entries.objects.filter(id=selectedentry_aux['id']).first()

            entry.name = selectedentry_aux['name']
            entry.username = selectedentry_aux['username']
            entry.password = selectedentry_aux['password']
            entry.url = selectedentry_aux['url']

            entry.save()

            if state:
                return redirect(f"/mobilehomeentry?entryid={selectedentry_aux['id']}&search={search}")
            else:
                return redirect(f"/?entryid={selectedentry_aux['id']}&search={search}")

    context = {
            'title':'Edit',
            'theme':theme,
            'language':language,
            'is_mobile':is_mobile,
            'entryidbool':entryidbool,
            'selectedentry':selectedentry,
            'state':state,
            'search':search,
            'error_dic':error_dic,
        }
    
    response = render(request, 'Pages/editentry.html', context)
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
                if len(Questions.objects.all()) != 0:
                    questions = Questions.objects.first()
                    if questions.encrypted:
                        key = encryptions.load_key("secure_key")

                        secanwser0 = encryptions.decrypt(questions.secanwser0, key)
                        questions.secanwser0 = secanwser0

                        secanwser1 = encryptions.decrypt(questions.secanwser1, key)
                        questions.secanwser1 = secanwser1

                        secanwser2 = encryptions.decrypt(questions.secanwser2, key)
                        questions.secanwser2 = secanwser2

                        questions.encrypted = False
                        questions.save()

                        key = ""
                        
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

def hom2(request):
    theme = init(request)

    context = {
        'title':'Home',
        'theme':theme,
    }    

    response = render(request, 'Pages/hom2.html', context)
    response.set_cookie(key='theme', value=theme)
    return response

def test(request):
    return render(request, 'Pages/hom3.html')

def test2(requet):
    print('holaaaa!!!!5')
    return HttpResponse('cosa')
