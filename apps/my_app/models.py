from django.db import models
import re, bcrypt
# Create your models here.
class UserManager(models.Manager):
    def registrationValidator(self, postData):
        matchingEmail = User.objects.filter(email=postData['email'])
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}

        if len(postData['fname']) == 0:
            errors['fname'] = "First name is required"

        if len(postData['lname']) == 0:
            errors['lname'] = "Last name is required"

        if len(postData['email']) == 0:
            errors['email'] = "Email is required"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email not in correct format"
        elif len(matchingEmail) != 0:
            errors['email'] = "Email already registered"


        if len(postData['pass']) == 0:
            errors['pass'] = "Password is required"
        elif len(postData['pass']) < 8:
            errors['pass'] = "Password must be at least 8 characters"
        elif postData['pass'] != postData['confirmPass']:
            errors['pass'] = "Passwords do not match"

        return errors

    def loginValidator(self, postData):
        matchingEmail = User.objects.filter(email=postData['email'])
        errors = {}

        if len(postData['email']) == 0:
            errors['email'] = "Email is required"
        elif len(matchingEmail) == 0:
            errors['email'] = "Email is not yet registered"

        if len(postData['pass']) == 0:
            errors['pass'] = "Password is required"
        if len(matchingEmail) > 0:
            if not bcrypt.checkpw(postData['pass'].encode(), matchingEmail[0].password.encode()):
                errors['pass'] = "Password is incorrect"

        return errors

class SignatureManager(models.Manager):
    def signatureValidator(self, postData):
        errors = {}

        if len(postData['fname']) == 0:
            errors['fname'] = "First name is required"
        elif len(postData['fname']) > 17:
            errors['fname'] = "First name cannot be more than 17 characters"

        if len(postData['lname']) == 0:
            errors['lname'] = "Last name is required"
        elif len(postData['lname']) > 17:
            errors['lname'] = "Last name cannot be more than 17 characters"

        if not postData['age']:
            errors['age'] = "Age is required"
        elif int(postData['age']) < 18:
            errors['age'] = "You must be 18 years old to sign"

        return errors


class Signature(models.Model):
    first_name=models.CharField(max_length=17)
    last_name=models.CharField(max_length=17)
    state=models.CharField(max_length=255)
    age=models.IntegerField()
    sex=models.CharField(max_length=255)
    comment=models.CharField(max_length=50)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=SignatureManager()


class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    admin=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()