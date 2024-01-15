from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login, name="login"),
    path('sign_up/', views.sing_up, name="sign_up"),
    path('logout/', views.signout, name="logout"),
    path('list/new/', views.createNewList, name="new-list"),
    path('list/<str:id>/', views.updateList, name="update-list"),
    path('list/<str:id>/new/', views.createListTask, name="new-task"),
    path('todo/<str:id>/', views.viewTask, name="view-task"),
    path('todo/<str:id>/starred/', views.starTask, name="star-task"),
    path('todo/<str:id>/complete/', views.completeTask, name="complete-task"),
    path('todo/<str:id>/update', views.updateTask, name="update-task"),
]
