from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create-move/<str:pk>', views.createMove, name='create-move'),
    path('add-vote/<str:pk>', views.addVote, name='add-vote'),
    path('create-poll', views.createPoll, name='create-poll'),

    path('login', views.loginUser, name='login'),
    path('logout', views.logoutUser, name='logout'),

    path('register', views.registerUser, name='register'),
    
]