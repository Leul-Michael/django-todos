from typing import Union
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import TodoList, Todo

User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Your Username', 'autoFocus': True}), required=True)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Your Email'}), required=True)
    password1 = forms.CharField(label='Password', min_length=8, widget=forms.PasswordInput(attrs={'placeholder': 'Your Password'}), required=True)
    password2 = forms.CharField(label='Confirm Password', min_length=8, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}), required=True, error_messages={'password_mismatch': 'Passwords do not match.'})
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username = username.lower()).exists():
            raise  forms.ValidationError("This username is already in use.")
        return username
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email = email.lower()).exists():
            raise  forms.ValidationError("This email address is already in use.")
        return email
    

class Listform(forms.ModelForm):
    name = forms.CharField(label='List Name', min_length=2, max_length=50, widget=forms.TextInput(attrs={'placeholder': 'name', 'autoFocus': True}), required=True)
    class Meta:
        model = TodoList
        fields = ['name']
    
    def __init__(self, user: User, *args, **kwargs):
        super().__init__(*args, **kwargs)    
        self.user = user
        
    def clean_name(self):
        name = self.cleaned_data.get('name')
        
        # Check for unique name, but exclude the current instance if updating
        if self.instance.id:
            existing_list = TodoList.objects.filter(user=self.user, name=name.lower()).exclude(id=self.instance.id)
        else:
            existing_list = TodoList.objects.filter(user=self.user, name=name.lower())
            
        if existing_list.exists() or (name.lower() == 'starred'):
            raise  forms.ValidationError("Name is already in use.")
        else:
            return name.lower()    


class TaskForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['name', 'description']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'autoFocus': True,
            'placeholder': 'Name'
        }) 
        self.fields['description'].widget.attrs.update({
            'placeholder': 'description...'
        })