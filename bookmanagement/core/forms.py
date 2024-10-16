from django import forms
from .models import Book, Transaction   
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm




class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email



class UserLoginForm(forms.Form):
    user_id = forms.CharField(label='Username')
    password = forms.CharField(widget=forms.PasswordInput())
    
    

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'is_available']
