from django.shortcuts import render, redirect
from time import gmtime, strftime, localtime
from django.contrib import messages
from .models import User, UserManager, Game, GameManager
import bcrypt

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST': 
        errors = User.objects.reg_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')       
        # hash the password
        hashed_pw = bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt()).decode()
        # create a user
        new_user = User.objects.create(
            first_name=request.POST['first_name'], 
            last_name=request.POST['last_name'], 
            birthday=request.POST['birthday'],
            email=request.POST['email'],
            password=hashed_pw
        )
        # create a session
        request.session['user_id'] = new_user.id
        return redirect('/success')
    return redirect('/')    

#log in
def login(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        this_user = User.objects.filter(email=request.POST['email'])
        request.session['user_id'] = this_user[0].id
        return redirect('/success')
    return redirect('/')

# render the success page
def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    this_user = User.objects.filter(id=request.session['user_id'])
    context = {
        'user': this_user[0],
        'all_games': Game.objects.all()
    }
    return render(request, 'success.html', context)

#log out
def logout(request):
    request.session.flush()
    return redirect('/')

def createGameForm(request):
    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'createGameForm.html', context)

def createGame(request):
    if request.method == 'POST':
        errors = Game.objects.game_validator(request.POST)
        # check if the errors dictionary has anything in it
        if len(errors) != 0:
            # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
            for key, value in errors.items():
                messages.error(request, value)
            # redirect the user back to the form to fix the errors
            return redirect('/success/createGameForm')
        else:
            this_user = User.objects.get(id=request.session['user_id'])   
            
            game = Game.objects.create(
                game_name = request.POST['game_name'],
                location = request.POST['location'],
                start_date = request.POST['start_date'],
                creator = this_user
            )
            game.players.add(this_user)
            return redirect('/success')
    return redirect('/')

def generate_game(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    this_user = User.objects.filter(id=request.session['user_id'])
    context = {
        'user': this_user[0],
        'one_game': Game.objects.get(id=id)
    }
    return render(request, 'one_game.html', context)

def edit_game(request, id):
    this_game = Game.objects.get(id=id)
    if this_game.creator.id != request.session['user_id']:
        messages.error(request, "Cannot edit other person's game.")
        return redirect(f'/game/{id}')
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'one_game': Game.objects.get(id=id)
    }
    return render(request, 'one_game_edit.html', context)

def update_game(request, id):
    if request.method == 'POST':
        errors = Game.objects.game_validator(request.POST)
        # check if the errors dictionary has anything in it
        if len(errors) > 0:
            # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
            for key, value in errors.items():
                messages.error(request, value)
            # redirect the user back to the form to fix the errors
            return redirect(f'/game/edit/{id}')

        else:
            game_to_update = Game.objects.get(id=id)
            game_to_update.game_name = request.POST['game_name']
            game_to_update.location = request.POST['location']
            game_to_update.start_date = request.POST['start_date']
            game_to_update.save()
        return redirect('/success')
    return redirect('/')

def delete_game(request, id):
    this_game = Game.objects.get(id=id)
    if this_game.creator.id != request.session['user_id']:
        messages.error(request, "Cannot delete other person's game.")
        return redirect(f'/game/{id}')
    game_to_delete = Game.objects.get(id=id)
    game_to_delete.delete()
    return redirect('/success')

def signup(request, id):
    this_user = User.objects.get(id=request.session['user_id'])
    this_game = Game.objects.get(id=id)
    this_game.players.add(this_user)
    return redirect(f'/game/{id}')

    
