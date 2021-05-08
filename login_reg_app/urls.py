from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('success', views.success),
    path('logout', views.logout),
    path('success/createGameForm', views.createGameForm),
    path('success/createGame', views.createGame),
    path('game/<int:id>', views.generate_game),
    path('game/edit/<int:id>', views.edit_game),
    path('game/update/<int:id>', views.update_game),
    path('game/<int:id>/delete', views.delete_game),
    path('signup/<int:id>', views.signup),
]
