from django.urls import path
from . import views
from .views import PieChartView, PieChartData

urlpatterns = [
    path('', views.TodoListView.as_view(), name='index'),
    path('upload-csv', views.todo_upload, name='todo-upload'),
    path('export', views.export, name='export'),
    path('statistics', views.PieChartView.as_view(), name='stats'),
    path('api/chart/data', views.PieChartData.as_view()),
    path('profile', views.view_profile, name='view_profile'),
    path('todo/new', views.TodoCreateView.as_view(), name='todo-create'),
    path('todo/<int:pk>', views.TodoDetailView.as_view(), name='particulartodo'),
    path('todo/delete', views.delete_todo, name='todo-delete'),
    path('todo/delete/api', views.delete_it),
    path('todo/complete', views.complete_todo, name="complete_todo"),
]