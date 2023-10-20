from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View

from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
# Create your views here.


def sign_in(request):
    page = "login"
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('list')

    return render(request, 'tasks/login_register.html', {'page': page})


def sign_out(request):
    logout(request)
    return redirect('sign_in')


def sign_up(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            user = authenticate(request, username=user.username, password=request.POST['password1'])
            if user is not None:
                login(request, user)
                return redirect('list')
    context = {'form': form, 'page': page}
    return render(request, 'tasks/login_register.html', context)


# @login_required(login_url='sign_in')
# def index(request):
#     tasks = Task.objects.all()
#     form = TaskForm()
#
#     if request.method == 'POST':
#         form = TaskForm(request.POST)
#         if form.is_valid():
#             form.save()
#         return redirect('/')
#
#     context = {'tasks': tasks, 'form': form}
#     return render(request, 'tasks/list.html', context)
@method_decorator(login_required(login_url='sign_in'), name='dispatch')
class Index(View):
    def get(self, request):
        tasks = Task.objects.all()
        form = TaskForm()
        context = {'tasks': tasks, 'form': form}
        return render(request, 'tasks/list.html', context)

    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
             form.save()
        return redirect('/')



@login_required(login_url='sign_in')
def current_day_tasks(request):
    date_from_request = request.GET.get('date')
    if date_from_request:
        date = timezone.datetime.strptime(date_from_request, "%Y-%m-%d").date()
        tasks = Task.objects.filter(date=date)
    else:
        tasks = Task.objects.all()

    context = {'tasks': tasks}
    return render(request, 'tasks/list_by_day.html', context)


# @login_required(login_url='sign_in')
# def update_task(request, pk):
#     task = Task.objects.get(id=pk)
#
#     form = TaskForm(instance=task)
#
#     if request.method == "POST":
#         form = TaskForm(request.POST, instance=task)
#         if form.is_valid():
#             form.save()
#         return redirect('/')
#
#     context = {'form': form}
#
#     return render(request, 'tasks/update_task.html', context)

@method_decorator(login_required(login_url='sign_in'), name='dispatch')
class Update(View):
    def get(self, request, pk):
        task = Task.objects.get(id=pk)
        form = TaskForm(instance=task)
        context = {'form': form}
        return render(request, 'tasks/update_task.html', context)

    def post(self, request, pk):
        task = Task.objects.get(id=pk)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('/')


@login_required(login_url='sign_in')
def delete_task(request, pk):
    item = Task.objects.get(id=pk)

    if request.method == 'POST':
        item.delete()
        return redirect('/')

    context = {'item': item}
    return render(request, 'tasks/delete.html', context)


@login_required(login_url='sign_in')
def complete_task(request, pk):
    item = Task.objects.get(id=pk)
    item.complete = True
    item.save()
    return redirect('/')
