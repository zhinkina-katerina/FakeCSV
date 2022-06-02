from django.shortcuts import render
from django.views.generic import ListView
from .models import Schema

class SchemeList(ListView):
    template_name = 'index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SchemeList, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Schema.objects.all()
