from django.db import models
from datetime import datetime, time
import re
import bcrypt

class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        # Length of the first name
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least two characters long"

        # Length of the last name
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least two characters long"

        print(postData['birthday'])
        # birthdate not in the past
        if postData['birthday'] == '': 
            errors['birthday'] = 'Must enter a birthday'
        elif datetime.strptime(postData['birthday'], '%Y-%m-%d') > datetime.now():
            
            errors['birthday'] = 'Birthdate must be in the past'


        # Email matches format
        email_regex = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['email']) == 0:
            errors['email'] = "You must enter an email"
        elif not email_regex.match(postData['email']):
            errors['email'] = "Must be a valid email"

        # Email is unique
        current_users = User.objects.filter(email=postData['email'])
        if len(current_users) > 0:
            errors['duplicate'] = "That email provided is already in use"

        # Password was entered (less than 8)
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characers long"
        if postData['password'] != postData['confirm_password']:
            errors['mismatch'] = "Your passwords do not match"

        return errors

    def login_validator(self, postData):
            errors = {}
            existing_user = User.objects.filter(email=postData['email'])
            if len(existing_user) != 1:
                errors['email'] = "User does not exist."
            
            # email has been entered
            if len(postData['email']) == 0:
                errors['email'] = "Email must be entered"
            
            # Password has been entered
            if len(postData['password']) < 8:
                errors['password'] = "Password must be at least 8 characters long"
            
            # if the email and password match
            elif bcrypt.checkpw(postData['password'].encode(), existing_user[0].password.encode()) != True:
                errors['mismatch'] = "Email and password do not match"
            return errors

class GameManager(models.Manager):
    def game_validator(self, postData):
        errors = {}
        if postData['game_name'] == '':
            errors['game_name'] = "Please enter a game name"
        if len(postData['game_name']) < 3:
                errors['game_name'] = "Game name must be at least 3 characters long"
        if postData['location'] == '':
            errors['location'] = "Please enter a location"
        if postData['start_date'] == '': 
            errors['start_date'] = "Must enter a date"
        elif datetime.strptime(postData['start_date'], '%Y-%m-%d') < datetime.now():           
            errors['start_date'] = 'Date cannot be in the past'
        if postData['start_time'] == '':
            errors['start_time'] = "Must provide a start time"
        return errors

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthday = models.DateField()
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    objects = UserManager()

class Game(models.Model):
    game_name = models.CharField(max_length=100)
    location = models.CharField(max_length=250)
    start_date = models.DateField(max_length=30)
    start_time = models.TimeField(default=datetime.now)
    players = models.ManyToManyField(User, related_name='games')
    creator = models.ForeignKey(User, related_name='game_creator', on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = GameManager()

