from django.urls import path
from . import views

app_name = "todo_app"

urlpatterns = [
    path("", views.task_list, name="task_list"),
    path("task/add/", views.task_create, name="task_create"),
    path("task/<int:pk>/", views.task_detail, name="task_detail"),
    path("task/<int:pk>/edit/", views.task_update, name="task_update"),
    path("task/<int:pk>/delete/", views.task_delete, name="task_delete"),
    path("task/<int:pk>/toggle/", views.task_toggle_status, name="task_toggle_status"),
    path("export/", views.export_tasks_excel, name="export_tasks_excel"),
]
