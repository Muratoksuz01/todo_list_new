from django.shortcuts import render,redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView ,DeleteView,FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
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
"""
# class TaskList(ListView):#defauld olarak task_list.html kullnıyor
#     model=Task
#     context_object_name="tasks"
"""
class TaskList(LoginRequiredMixin,ListView):#bunu ekledik ve setting LOGİN_URL='login' yazdık
    model=Task
    context_object_name="tasks"
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['tasks']=context['tasks'].filter(user=self.request.user)#burada kim girdi ise onun task larını getiriyoruz
        context['count']=context['tasks'].filter(complete=False).count()

        search_input=self.request.GET.get("search-area") or ''# araam kısmı yapıldı ona göre filtreleme yapıyorum
        context["tasks"]=context["tasks"].filter(title__startswith=search_input)
        context["search_input"]=search_input
        return context
    

class TaskDetail(DetailView,LoginRequiredMixin):#defauld olarak task_detail.html kullnıyor
    model=Task
    context_object_name="task"
    template_name="base/task.html"
class TaskCreate(CreateView,LoginRequiredMixin):#task_form.html kullanıyor
    model=Task
    fields=["title","description","complete"]#form kısmında gösterilecekleri yazıyoruz 
    success_url=reverse_lazy("tasks")# bu foksiyon sanki redirect gibi calışıyor    
    def form_valid(self,form):#burada otomatik kım login oldu ise onun hesabına task i ekliyoruz 
        form.instance.user=self.request.user
        return super(TaskCreate,self).form_valid(form)
class TaskUpdate(UpdateView,LoginRequiredMixin):#burasıda task_form.html kullanıyor
    model=Task
    fields=["title","description","complete"]
    
    success_url=reverse_lazy("tasks")# bu foksiyon sanki redirect gibi calışıyor    
class TaskDelete(DeleteView,LoginRequiredMixin):
    model=Task
    context_object_name="task"
    success_url=reverse_lazy("tasks")
class RegisterPage(FormView):
    template_name='base/register.html'
    form_class=UserCreationForm
    redirect_authenticated_user= True
    success_url=reverse_lazy("tasks")
    def form_valid(self,form):
        user=form.save()
        if user is not None:
            login(self.request,user)
        return super(RegisterPage,self).form_valid(form)
    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated :
            return redirect("tasks")
        return super(RegisterPage,self).get(*args,**kwargs)


