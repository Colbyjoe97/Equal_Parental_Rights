from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.urls import reverse
from apps.my_app.models import *
from django.contrib import messages
import bcrypt
# Create your views here.
def index(request):
    # signees = Signature.objects.all()
    # for s in signees:
    #     s.delete()
    us_states = [("AL","Alabama"),("AK","Alaska"),("AZ","Arizona"),("AR","Arkansas"),("CA", "California"),("CO", "Colorado"),
    ("CT","Connecticut"),("DC","Washington DC"),("DE","Delaware"),("FL","Florida"),("GA","Georgia"),
    ("HI","Hawaii"),("ID","Idaho"),("IL","Illinois"),("IN","Indiana"),("IA","Iowa"),("KS","Kansas"),("KY","Kentucky"),
    ("LA","Louisiana"),("ME","Maine"),("MD","Maryland"),("MA","Massachusetts"),("MI","Michigan"),("MN","Minnesota"),
    ("MS","Mississippi"),("MO","Missouri"),("MT","Montana"),("NE","Nebraska"),("NV","Nevada"),("NH","New Hampshire"),
    ("NJ","New Jersey"),("NM","New Mexico"),("NY","New York"),("NC","North Carolina"),("ND","North Dakota"),("OH","Ohio"),
    ("OK","Oklahoma"),("OR","Oregon"),("PA","Pennsylvania"),("RI","Rhode Island"),("SC","South Carolina"),("SD","South Dakota"),
    ("TN","Tennessee"),("TX","Texas"),("UT","Utah"),("VT","Vermont"),("VA","Virginia"),("WA","Washington"),("WV","West Virginia"),
    ("WI","Wisconsin"),("WY","Wyoming")]
    if 'user' in request.session:
        context = {
            'user': User.objects.get(id=request.session['user']),
            'states': us_states,
            'signatures': Signature.objects.all(),
            'total': len(Signature.objects.all())
        }
    else:
        context = {
            'states': us_states,
            'signatures': Signature.objects.all(),
            'total': len(Signature.objects.all())
        }
    return render(request, 'index.html', context)


def sign(request):
    duplicate = False
    errors = Signature.objects.signatureValidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
    else:
        signatures = Signature.objects.filter(first_name=request.POST['fname'], last_name=request.POST['lname'], age=request.POST['age'], state=request.POST['state'])
        for s in signatures:
            print(s.first_name, s.last_name)
        if len(signatures) == 0:
            Signature.objects.create(first_name=request.POST['fname'],last_name=request.POST['lname'],age=request.POST['age'],sex=request.POST['sex'],state=request.POST['state'],comment=request.POST['comment'])
        else:
            messages.error(request, "You cannot sign more than once")
    return redirect("/")





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
            # print(f"THIS IS THE NEW USER: {user}")
            # print(f"THIS IS THE NEW USER SESSION: {request.session['user']}")
            return redirect("/")
        else:
            request.session['errors'] = "bad code"
            messages.error(request, "Admin code is incorrect")
            return redirect('/admin/register')


def admin_page(request):
    if 'user' in request.session:
        context = {
            'user': User.objects.get(id=request.session['user'])
        }
        return render(request, 'admin-page.html', context)
