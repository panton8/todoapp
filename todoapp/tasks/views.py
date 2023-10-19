from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
# Create your views here.


def index(request):
    tasks = Task.objects.all()
    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')

    context = {'tasks': tasks, 'form': form}
    return render(request, 'tasks/list.html', context)


def current_day_tasks(request):
    date_from_request = request.GET.get('date')
    if date_from_request:
        date = timezone.datetime.strptime(date_from_request, "%Y-%m-%d").date()
        tasks = Task.objects.filter(date=date)
    else:
        tasks = Task.objects.all()

    context = {'tasks': tasks}
    return render(request, 'tasks/list_by_day.html', context)

def updateTask(request, pk):
    task = Task.objects.get(id=pk)

    form = TaskForm(instance=task)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
        return redirect('/')

    context = {'form': form}

    return render(request, 'tasks/update_task.html', context)


def deleteTask(request, pk):
    item = Task.objects.get(id=pk)

    if request.method == 'POST':
        item.delete()
        return redirect('/')

    context = {'item': item}
    return render(request, 'tasks/delete.html', context)


def completeTask(request, pk):
    item = Task.objects.get(id=pk)
    item.complete = True
    item.save()
    return redirect('/')