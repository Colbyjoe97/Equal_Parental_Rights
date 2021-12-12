from django.shortcuts import render, redirect
from apps.my_app.models import *
from django.contrib import messages
import bcrypt
# Create your views here.
def index(request):
    return render(request, 'index.html')


def admin(request):
    return render(request, 'admin-register.html')

def register_admin(request):
    errors = User.objects.registrationValidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        request.session['errors'] = 1
    else:
        if request.POST['admin-code'] == "centrino39":
            hashedPass = bcrypt.hashpw(request.POST['pass'].encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(first_name=request.POST['fname'],last_name=request.POST['lname'],email=request.POST['email'],password=hashedPass)
            print(user)
        else:
            messages.error(request, "Admin code is incorrect")
    return redirect("/")