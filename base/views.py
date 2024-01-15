from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, logout, login as login_user, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django import forms
from .forms import UserRegistrationForm, Listform, TaskForm
from .models import TodoList, Todo

User = get_user_model()

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        list_query = request.GET['list'] if request.GET.get('list') != None else ''
        lists = TodoList.objects.filter(user=request.user)
        
        if lists.count() > 0 and list_query == '':
            list_query = lists.first().name
            
        tasks = Todo.objects.filter(todo_list__user=request.user, is_starred=True, is_completed=False) if list_query == '' or list_query == 'starred' else Todo.objects.filter(Q(todo_list__name__icontains=list_query), todo_list__user=request.user)
        pending_tasks = [task for task in tasks if not task.is_completed]
        completed_tasks = [task for task in tasks if task.is_completed]
        context = {'lists': lists, 'list': list_query, 'tasks': pending_tasks, 'completed_tasks': completed_tasks}
        return render(request, 'base/home.html', context)
    else:
        return render(request, 'base/home.html')

    return render(request, 'base/home.html', context)

def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
        
            if user is not None:
                login_user(request, user)
                return redirect('home')
            else:
                messages.add_message(request, messages.ERROR, "Invalid Email / Password.")   
        except Exception as e:
            messages.add_message(request, messages.ERROR, "User not found! Register please.")   
        
            
                
    context = {'page': 'login'}
    return render(request, "base/auth.html", context)

def sing_up(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    form = UserRegistrationForm()
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.email = user.email.lower()
            user.save()
            login_user(request, user)
            return redirect('home')
        
    context = {'page': 'sign_up', 'form': form}
    return render(request, "base/auth.html", context)

def signout(request):
    logout(request)
    return redirect('home')
    

@login_required(login_url='login')
def createNewList(request):
    form = Listform(user=request.user)
    if request.method == "POST":
        lists = TodoList.objects.filter(user=request.user)
        if lists.count() >= 10:
            messages.add_message(request, messages.ERROR, "Maximum allowed number of lists reached.")
            return redirect('home') 
        else:
            form = Listform(user=request.user, data= request.POST)
            if form.is_valid(): 
                new_list = form.save(commit=False)
                new_list.user = request.user
                new_list.save()
                return redirect(reverse('home') + '?list=' + str(new_list))
            
    context = {'form': form}    
    return render(request, "base/new-list.html", context)  

@login_required(login_url='login')
def updateList(request, id):
    todo_list = get_object_or_404(TodoList, name=id, user=request.user)
    form = Listform(user=request.user, instance=todo_list)
    
    if request.user != todo_list.user:
        return HttpResponse('Your are not allowed here!!')
    if request.method == "POST":
        form = Listform(user= request.user, data= request.POST, instance=todo_list)
        if form.is_valid(): 
            updated_todo = form.save(commit=False)
            todo_list.name = updated_todo.name
            todo_list.save()
            return redirect(reverse('home') + '?list=' + str(todo_list))

    if request.method == "DELETE":
        todo_list.delete()
        return redirect('home')
          
    context = {'form': form, 'list': todo_list}    
    return render(request, "base/update-list.html", context)  

@login_required(login_url='login')
def createListTask(request, id):
    form = TaskForm()
    if request.method == "POST":
        current_list = TodoList.objects.get(name=id, user=request.user)
        if current_list != None:
            form = TaskForm(request.POST)
            if form.is_valid(): 
                new_task = form.save(commit=False)
                new_task.todo_list = current_list
                new_task.user = request.user
                new_task.save()
                return redirect(reverse('home') + '?list=' + id)
            else:
                messages.add_message(request, messages.ERROR, "List not found!")
                return redirect('home') 
    context = {'form': form}    
    return render(request, "base/new-task.html", context)  

@login_required(login_url='login')
def viewTask(request, id):
    task = get_object_or_404(Todo, id=id, todo_list__user=request.user)
    context = {'task': task}
    return render(request, "base/task.html", context)  

@login_required(login_url='login')
def updateTask(request, id):
    todo = get_object_or_404(Todo, id=id, todo_list__user=request.user)
    form = TaskForm(instance=todo)
    
    if todo == None:
        messages.add_message(request, messages.ERROR, "Task not found!")
        return redirect('home') 
    if request.method == "POST":
        form = TaskForm(data= request.POST, instance=todo)
        if form.is_valid(): 
            updated_todo = form.save(commit=False)
            todo.name = updated_todo.name
            todo.description = updated_todo.description
            todo.save()
            return redirect('view-task', id=id)

    if request.method == "DELETE":
        todo.delete()
        return redirect('home')
          
    context = {'form': form, 'task': todo}    
    return render(request, "base/update-task.html", context)  

@login_required(login_url='login')
def starTask(request, id):
    req_from = request.PATCH['from'] if request.PATCH.get('from') != None else None

    if request.method == "PATCH":
        print(req_from)
        task = get_object_or_404(Todo, id=id, todo_list__user=request.user)
        task.is_starred = not task.is_starred
        task.save()
    return redirect(req_from, id=id) if req_from != None else redirect('home')   
 

@login_required(login_url='login')
def completeTask(request, id):
    req_from = request.PATCH['from'] if request.PATCH.get('from') != None else None
    
    if request.method == "PATCH":
        print(req_from)
        task = get_object_or_404(Todo, id=id, todo_list__user=request.user)
        task.is_completed = not task.is_completed
        task.save()
    return redirect(req_from, id=id) if req_from != None else redirect('home')   


