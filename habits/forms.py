from django import forms
from .models import Habit

class MarkCompletedForm(forms.Form):
    habit_id = forms.IntegerField(widget=forms.HiddenInput())