from __future__ import unicode_literals
from django.shortcuts import render, redirect
from apps.my_app.models import *
from django.contrib import messages
import bcrypt
# Create your views here.
def index(request):
    # users = User.objects.all()
    # for user in users:
    #     user.delete()
    if 'user' in request.session:
        context = {
            'user': User.objects.get(id=request.session['user'])
        }
    else:
        context = {}
    return render(request, 'index.html', context)


def admin(request):
    if 'errors' in request.session:
        context = {
            'errorType': request.session['errors']
        }
    else:
        context = {}
    return render(request, 'admin-register.html', context)

def register_admin(request):
    errors = User.objects.registrationValidator(request.POST)
    print(request.POST)
    if len(errors) > 0:
        request.session['errors'] = "register"
        for key, value in errors.items():
            messages.error(request, value)
        if request.POST['admin-code'] != "centrino39":
            request.session['errors'] = "bad code"
            messages.error(request, "Admin code is incorrect")
        return redirect('/admin/register')
    else:
        if request.POST['admin-code'] == "centrino39":
            hashedPass = bcrypt.hashpw(request.POST['pass'].encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(first_name=request.POST['fname'],last_name=request.POST['lname'],email=request.POST['email'],admin=True,password=hashedPass)
            request.session['user'] = user.id
            print(f"THIS IS THE NEW USER: {user}")
            print(f"THIS IS THE NEW USER SESSION: {request.session['user']}")
            return redirect("/")
        else:
            request.session['errors'] = "bad code"
            messages.error(request, "Admin code is incorrect")
            return redirect('/admin/register')
