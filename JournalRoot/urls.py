"""JournalRoot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include

from JournalApp.views import TaskListView, NewTaskView, TaskView, DeleteTaskView
from JournalRoot.views import Home, register
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    # Home
    path('', Home.as_view(), name='home'),

    # Authentication and Registration
    path('login/', auth_views.login, name='login'),
    path('logout/', auth_views.logout, name='logout'),
    path('register/', register, name='register'),

    path('journals', login_required(TaskListView.as_view()) , name='journals'),
    path('journal', login_required(NewTaskView.as_view()), name='journal-add'),
    path('journal/<int:task_id>', login_required(TaskView.as_view()), name='journal-edit'),
    path('delete/<int:task_id>', login_required(DeleteTaskView.as_view()), name='journal-delete'),
    path('api/', include('JournalApp.api.urls', namespace='api'), name='api'), # This is to include api URL. We need to be login as admin to perform CRUD operations
    path('admin/', admin.site.urls),
]+staticfiles_urlpatterns()


