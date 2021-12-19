from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.urls import reverse
from apps.my_app.models import *
from django.contrib import messages
import bcrypt
from django.http import JsonResponse

# Create your views here.
def index(request):
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
            'signatures': Signature.objects.order_by('-created_at'),
            'total': len(Signature.objects.all())
        }
    else:
        context = {
            'states': us_states,
            'signatures': Signature.objects.order_by('-created_at'),
            'total': len(Signature.objects.all())
        }
    return render(request, 'index.html', context)


def sign(request):
    if request.method == "POST":
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
                Signature.objects.create(
                    first_name=request.POST['fname'],
                    last_name=request.POST['lname'],
                    age=request.POST['age'],
                    sex=request.POST['sex'],
                    state=request.POST['state']
                )
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
        request.session['errors'] = 1
        for key, value in errors.items():
            messages.error(request, value)
        if request.POST['admin-code'] != "centrino39":
            messages.error(request, "Admin code is incorrect")
        return redirect('/admin/register')
    else:
        if request.POST['admin-code'] == "centrino39":
            hashedPass = bcrypt.hashpw(request.POST['pass'].encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(first_name=request.POST['fname'],last_name=request.POST['lname'],email=request.POST['email'],admin=True,password=hashedPass)
            request.session['user'] = user.id
            return redirect("/")
        else:
            request.session['errors'] = "bad code"
            messages.error(request, "Admin code is incorrect")
            return redirect('/admin/register')



def login(request):
    errors = User.objects.loginValidator(request.POST)
    if len(errors) > 0:
        request.session['errors'] = 2
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/admin/register')
    else:
        user = User.objects.filter(email=request.POST['email'])
        request.session['user'] = user[0].id
        return redirect('/')


def admin_page(request):
    if 'user' in request.session:
        request.session['state_count'] = []
        us_states = [("AL","Alabama"),("AK","Alaska"),("AZ","Arizona"),("AR","Arkansas"),("CA", "California"),("CO", "Colorado"),
        ("CT","Connecticut"),("DC","Washington DC"),("DE","Delaware"),("FL","Florida"),("GA","Georgia"),
        ("HI","Hawaii"),("ID","Idaho"),("IL","Illinois"),("IN","Indiana"),("IA","Iowa"),("KS","Kansas"),("KY","Kentucky"),
        ("LA","Louisiana"),("ME","Maine"),("MD","Maryland"),("MA","Massachusetts"),("MI","Michigan"),("MN","Minnesota"),
        ("MS","Mississippi"),("MO","Missouri"),("MT","Montana"),("NE","Nebraska"),("NV","Nevada"),("NH","New Hampshire"),
        ("NJ","New Jersey"),("NM","New Mexico"),("NY","New York"),("NC","North Carolina"),("ND","North Dakota"),("OH","Ohio"),
        ("OK","Oklahoma"),("OR","Oregon"),("PA","Pennsylvania"),("RI","Rhode Island"),("SC","South Carolina"),("SD","South Dakota"),
        ("TN","Tennessee"),("TX","Texas"),("UT","Utah"),("VT","Vermont"),("VA","Virginia"),("WA","Washington"),("WV","West Virginia"),
        ("WI","Wisconsin"),("WY","Wyoming")]
        for i in us_states:
            signees = Signature.objects.filter(state=i[0])
            if len(signees) > 0:
                state = {
                    'state': i[1],
                    'count': len(signees)
                }
                request.session['state_count'].append(state)
        context = {
            'user': User.objects.get(id=request.session['user']),
            'states': sorted(request.session['state_count'], key=lambda x: -x['count'])
        }
        return render(request, 'admin-page.html', context)
    else:
        return redirect('/')







def bad_request(request):
    return redirect('/')