from django.shortcuts import render, redirect
from django.views.generic import ListView, View, TemplateView
from .models import Schema, DataType
from .forms import SchemaForm, DataTypeForm

class SchemeList(ListView):
    template_name = 'index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SchemeList, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Schema.objects.all()


class SchemeEditView(TemplateView):
    template_name = "edit_schema.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SchemeEditView, self).get_context_data(**kwargs)

        context['object_list']=self.get_queryset().all()
        context['form_schema_options'] = SchemaForm()
        context['form_data_type'] = DataTypeForm()
        context['items_have_range'] = self.get_queryset().get_items_have_range()
        return context

    def get_queryset(self):
        return DataType.objects
