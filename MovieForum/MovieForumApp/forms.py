from django import forms
from .models import Actor, Director, Producer, Movie, Genre
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model


class CreateUserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'photo', 'password1', 'password2']


class EditUserForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']


class ActorForm(forms.ModelForm):
    class Meta:
        model = Actor
        fields = '__all__'
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'})
        }


class DirectorForm(forms.ModelForm):
    class Meta:
        model = Director
        fields = '__all__'


class ProducerForm(forms.ModelForm):
    class Meta:
        model = Producer
        fields = '__all__'


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'
        widgets = {
            'date_of_release': forms.DateInput(attrs={'type': 'date'}),
        }


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = '__all__'
