import csv, io
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from . import views
from .models import Todo
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from todolist.resources import TodoExportResource
import tablib
from import_export import resources
from tablib import Dataset
from django.urls import reverse
import logging


@login_required
def todo_upload(request):
    prompt = {
        'order': 'Order of CSV fields should be Todo, Status with the header row included. Make sure there are no extra spaces added to csv as rows, commas are not used in fields.Only accepts CSV files.'
    }
    if request.method == "GET":
        return render(request, 'import.html', prompt)
    
    try:
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'This is not a csv file.')
            return HttpResponseRedirect(reverse("todo-upload"))

        if csv_file.multiple_chunks():
            messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
            return HttpResponseRedirect(reverse("todo-upload"))

        data_set = csv_file.read().decode('UTF-8')
        
        io_string = io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):

            if 'N' in column[1]:
                column[1]=False
            else:
                column[1]=True

            Todo.objects.create(
                user = request.user,
                text = column[0],
                is_completed = column[1]
            )
    
        context = {}
        return render(request, 'import.html', context)
    except Exception as e:
     	logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
     	messages.error(request,"Unable to upload file. "+repr(e))

    return HttpResponseRedirect(reverse("todo-upload"))


@login_required
def export(request):
    todo_resource = TodoExportResource()
    dataset = todo_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="todos.csv"'
    return response


class PieChartView(LoginRequiredMixin, generic.View):
    def get(self, request, *args, **kwargs):

        return render(request, 'piechart.html')


class PieChartData(LoginRequiredMixin, APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):

        completed_count = Todo.objects.filter(is_completed = 1).count()
        uncompleted_count = Todo.objects.filter(is_completed = 0).count()
        #to skip division by zero
        if completed_count + uncompleted_count == 0:
            return render(request, 'createorimport.html') 
        completed_percentage = (completed_count/(completed_count+uncompleted_count))*100
        uncompleted_percentage = (uncompleted_count/(completed_count+uncompleted_count))*100

        labels = ['Completed(' + str(completed_count) + ')', 'Not Completed(' + str(uncompleted_count) + ')']
        default_items = [round(completed_percentage), round(uncompleted_percentage)]
        data = {
            "labels":labels,
            "default":default_items,
        }
        return Response(data)

class TodoListView(generic.ListView):
    model = Todo
    paginate_by = 4


@login_required
def view_profile(request):
    context = {
        "user":request.user
    }
    return render(request, 'view_profile.html', context=context)

class TodoDetailView(LoginRequiredMixin,generic.DetailView):
    model = Todo


class TodoCreateView(LoginRequiredMixin, generic.CreateView):
    model = Todo
    fields = ["text", "is_completed"]

    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form)


@login_required
def delete_todo(request):
    todo = get_object_or_404(Todo, id=request.POST.get('todo_id'))

    if todo.user == request.user:
        todo.delete()

    else:
        messages.info(request, '*Not Allowed')

    return HttpResponseRedirect("/")


@login_required
def complete_todo(request):
    todo = get_object_or_404(Todo, id=request.POST.get('todo_id'))
    print(todo)
    if todo.user == request.user:
        print("checked user")
        if todo.is_completed:
            
            todo.is_completed = not todo.is_completed
            todo.save()
            print("todo is false now")
        else:
            
            todo.is_completed = not todo.is_completed
            todo.save()
            print("todo is true now")
    else:
        messages.info(request, '*Not Allowed')
        print('No permissions')

    return HttpResponseRedirect("/")
