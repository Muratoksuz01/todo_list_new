from django.shortcuts import render,redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView ,DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from .models import Task
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class TaskLogin(LoginView):#defauld olarak context form veriyor 
    template_name="base/login.html"
    fields="__all__"
    redirect_authenticated_user=True#defauld olarak false gelir 
    def get_success_url(self):
        return reverse_lazy("tasks")

# class TaskList(ListView):#defauld olarak task_list.html kullnıyor
#     model=Task
#     context_object_name="tasks"
class TaskList(LoginRequiredMixin,ListView):#bunu ekledik ve setting LOGİN_URL='login' yazdık
    model=Task
    context_object_name="tasks"
class TaskDetail(DetailView,LoginRequiredMixin):#defauld olarak task_detail.html kullnıyor
    model=Task
    context_object_name="task"
    template_name="base/task.html"
class TaskCreate(CreateView,LoginRequiredMixin):#task_form.html kullanıyor
    model=Task
    fields="__all__"
    success_url=reverse_lazy("tasks")# bu foksiyon sanki redirect gibi calışıyor    
class TaskUpdate(UpdateView,LoginRequiredMixin):#burasıda task_form.html kullanıyor
    model=Task
    fields="__all__"
    success_url=reverse_lazy("tasks")# bu foksiyon sanki redirect gibi calışıyor    
class TaskDelete(DeleteView,LoginRequiredMixin):
    model=Task
    context_object_name="task"
    success_url=reverse_lazy("tasks")