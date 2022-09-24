from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt 
from .models import User, Skill, UserManager, SkillManager 

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

def create(request):
    errors = Skill.objects.skill_validator(request.POST)

    if len(errors) > 0  :
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/skill_form')
    else :
        user = User.objects.get(id = request.session['user_id'])
        skill = Skill.objects.create(
            location = request.POST['location'], 
            skill = request.POST['skill'], 
            profession = request.POST['profession'] ,
            time= request.POST['time'],
            posted_by = user
            )
            
        return redirect("/dashboard")

def one_skill(request,skill_id):
    context = {
        'skill': Skill.objects.get(id = skill_id)
    }
    return render(request, "skill.html", context)

def update(request, skill_id):
    errors = Skill.objects.skill_validator(request.POST)

    if len(errors) > 0  :
        for key, value in errors.items():  
            messages.error(request, value)
        return redirect('/dashboard')
    else :
        skill_update = Skill.objects.get(id = skill_id)
        skill_update.location = request.POST['location']
        skill_update.skill = request.POST['skill']
        skill_update.profession = request.POST['profession']
        skill_update.time = request.POST['time']
        skill_update.save()
        #return render(request, "edit.html") 
        return redirect("/dashboard")

def delete(request, skill_id):
    user = User.objects.get(id = request.session['user_id'])
    skill = Skill.objects.filter(id = skill_id)
    #if job.id == user.id:
    skill.delete()#is_removed = True delete()
    #job.save()
    return redirect('/dashboard')

def profile(request, user_id):
    context = {
        'user': User.objects.get(id = user_id)
    }
    return render(request, "user.html", context)
