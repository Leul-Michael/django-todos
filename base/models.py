from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Create your models here

class User(AbstractUser):
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.username

class Todo(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    todo_list = models.ForeignKey('TodoList', on_delete=models.CASCADE)
    is_starred = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-updated_at', '-created_at']
    
    def __str__(self):
        return self.name
    
class TodoList(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['name', 'user']
    
    def __str__(self):
        return self.name
        