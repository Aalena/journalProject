from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# Create your views here.
from JournalApp.forms import JournalForm
from JournalApp.mixins import SuccessTaskListMixin, TaskOwnedByUserMixin
from JournalApp.models import Journal


class TaskListView(TemplateView):
    template_name = 'task_list.html'

    def get_queryset(self):
        return Journal.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        context['tasks'] = self.get_queryset()
        return context


class NewTaskView(SuccessTaskListMixin, CreateView):
    template_name = 'task.html'
    form_class = JournalForm

    def form_valid(self, form):
        task = form.save(commit=False)
        task.owner = self.request.user
        task.save()
        return HttpResponseRedirect(self.get_success_url())


class TaskView(TaskOwnedByUserMixin, SuccessTaskListMixin, UpdateView):
    """
        View to view and edit a task. Must be owner to edit a task. Redirect
        to task list upon completion.
    """
    template_name = 'task.html'
    form_class = JournalForm
    pk_url_kwarg = 'task_id'

    def get_queryset(self):
        if hasattr(self.request, 'user') and self.request.user.is_active:
            return Journal.objects.filter(owner = self.request.user)
        return Journal.objects.none()

    def get_context_data(self, **kwargs):
        context = super(TaskView, self).get_context_data(**kwargs)
        context['update'] = True
        return context

class DeleteTaskView(TaskOwnedByUserMixin, SuccessTaskListMixin, DeleteView):
    """
    View to delete a task. Must be owner to delete a task. Redirect
    to task list upon completion.
    """
    model = Journal
    pk_url_kwarg = 'task_id'