from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt 
from .models import User, Skill

# Create your views here.
def index(request):
    return render(request,"LogReg.html")

def register(request):
    if request.method == 'GET':
        return redirect('/')
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0 :
        for key, value in errors.items():
            messages.error(request,value)
            return redirect('/')
    else:
        new_user = User.objects.create(first_name = request.POST['first_name'], last_name= request.POST['last_name'], email = request.POST['email'], password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode())
        request.session['user_id'] = new_user.id
        request.session['greeting'] = new_user.first_name
        return redirect('/dashboard')

    
def login(request):
    user = User.objects.filter(email = request.POST['email'])
    if user:
        user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['user_id']= user.id
            request.session['greeting'] = user.first_name
            return redirect('/dashboard')
    return redirect("/dashboard")

def logpage(request):
    return render(request, "login.html")
    
def logout(request):
    request.session.flush()
    return redirect('/')

def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id = request.session['user_id'])
    #user_jobs = jobs_id
    context = {
        'user': user,
        'skills': Skill.objects.all(),
        
        #'jobs_only':Job.objects.get(id = request.POST['book_id'])
        #'user_jobs': Job.objects.filter(jobs = user)
    }
    return render(request, "dashboard.html",context)

def skill_form(request):
    return render(request,"create_skill.html")