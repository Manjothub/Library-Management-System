
from django import forms
from django.contrib.auth.models import User
from . models import *

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"

class IssueBookForm(forms.ModelForm):
    class Meta:
        model = IssuedBook
        fields = "__all__"