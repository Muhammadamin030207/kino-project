from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Director, Genre, Movie


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'})
    )
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full name'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'})
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'full_name', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )


class DirectorForm(forms.ModelForm):
    class Meta:
        model = Director
        fields = ['country', 'birth_year', 'photo', 'awards']
        widgets = {
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'birth_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Birth year'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'awards': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Awards'}),
        }


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Genre name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description'}),
        }


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'poster', 'release_year', 'rating', 'genres']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Movie title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Description'}),
            'poster': forms.FileInput(attrs={'class': 'form-control'}),
            'release_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Release year'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'Rating'}),
            'genres': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
