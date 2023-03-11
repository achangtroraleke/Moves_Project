from django.forms import ModelForm
from .models import Venue, User
from django.contrib.auth.forms import UserCreationForm

class VenueForm(ModelForm):
    class Meta:
        model = Venue
        fields = '__all__'
        exclude = ['poll', 'votes', 'host', 'address']

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']