from django.urls import include, path
from django.contrib.auth.views import LogoutView
from .views import *
urlpatterns = [
    path("logout/",LogoutView.as_view(next_page="login"),name="logout"),
    path("login/",TaskLogin.as_view(),name="login"),
    path("register/",RegisterPage.as_view(),name="register"),

   
     path("",TaskList.as_view(),name="tasks"),
    path("task/<int:pk>",TaskDetail.as_view(),name="task"),
    path("create-tesk",TaskCreate.as_view(),name="task-create"),
    path("task-edit/<int:pk>",TaskUpdate.as_view(),name="task-edit"),
    path("task-delete/<int:pk>",TaskDelete.as_view(),name="task-delete"),



    
]
