from django import forms
from .models import Journal


class JournalForm(forms.ModelForm):
    """
    A model form for a Task object.
    """
    class Meta:
        exclude = ['pk', 'owner']
        model = Journal
