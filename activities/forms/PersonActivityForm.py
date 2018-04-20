# coding=utf-8
from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.auth.models import User
from django.db.models import BLANK_CHOICE_DASH

from activities.forms.BootstrapModelForm import BootstrapModelForm
from activities.models import PersonActivity
from currency.models import Entity


class PersonActivityForm(BootstrapModelForm):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        form = super(PersonActivityForm, self).__init__(*args, **kwargs)

    class Meta:
        model = PersonActivity
        exclude = []
        widgets = {
            'time_spent': forms.TimeInput(attrs={'class': 'form-control time-input'}),
        }