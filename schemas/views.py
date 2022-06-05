from django.shortcuts import redirect, get_object_or_404, HttpResponse
from django.views.generic import ListView, TemplateView, View
import json
from .models import Schema, DataType, Dataset
from .forms import SchemaForm, DataTypeForm
from django.contrib.auth.mixins import LoginRequiredMixin


class SchemeList(LoginRequiredMixin, ListView):
    template_name = 'index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SchemeList, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Schema.objects.filter(user=self.request.user)


class SchemeCreateView(LoginRequiredMixin, TemplateView):
    template_name = "create_schema.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SchemeCreateView, self).get_context_data(**kwargs)
        context['object_list'] = self.get_queryset().all()
        context['form_schema_options'] = SchemaForm()
        context['form_data_type'] = DataTypeForm()
        context['items_have_range'] = self.get_queryset().get_items_have_range()
        return context

    def get_queryset(self):
        return DataType.objects

    def post(self, request, *args, **kwargs):
        new_schema_obj = request.POST.get('json_object')
        new_schema_json = json.loads(new_schema_obj)
        Schema.objects.create(
            title=new_schema_json['schema']['title'],
            column_separator=new_schema_json['schema']['column_separator'],
            string_character=new_schema_json['schema']['string_character'],
            structure=new_schema_json['schema_columns'],
            user=request.user
        )
        return HttpResponse(status=200)



class SchemeEditView(SchemeCreateView):
    template_name = "edit_schema.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SchemeEditView, self).get_context_data(**kwargs)
        schema = Schema.objects.get(id=self.kwargs['id'])
        initial_dict = {
            "title": schema.title,
            "column_separator": schema.column_separator,
            "string_character": schema.string_character,
        }
        forms = []
        structure = list(eval(schema.structure))
        for item in structure:
            forms.append(DataTypeForm(initial=item))
        # context['object_list']=self.get_queryset().all()
        context['form_schema_options'] = SchemaForm(initial=initial_dict)
        context['forms'] = forms
        context['object'] = schema
        # context['items_have_range'] = self.get_queryset().get_items_have_range()
        return context

    def post(self, request, *args, **kwargs):
        new_schema_obj = request.POST.get('json_object')
        new_schema_json = json.loads(new_schema_obj)
        schema_id = self.kwargs['id']
        schema = Schema.objects.get(id=schema_id)
        schema.title = new_schema_json['schema']['title']
        schema.column_separator = new_schema_json['schema']['column_separator']
        schema.string_character = new_schema_json['schema']['string_character']
        schema.structure = new_schema_json['schema_columns']
        schema.save()
        return HttpResponse(status=200)


class DeleteSchemaView(LoginRequiredMixin, View):
    def get(self, request, id, *args, **kwargs):
        return redirect('schema_view')

    def post(self, request, id, *args, **kwargs):
        schema = get_object_or_404(Schema, id=id)
        Dataset.objects.filter(schema=schema).delete()
        schema.delete()
        return redirect('schema_view')


class DatasetView(LoginRequiredMixin, ListView):
    template_name = "dataset_list.html"

    def post(self, request, id, *args, **kwargs):
        id_schema = request.POST.get('id')
        Dataset.objects.create(
            status="New",
            schema=Schema.objects.filter(id=id_schema).first(),
            rows_quantity=request.POST.get('rows'),
            user=request.user
        )
        return redirect('dataset_list', id=id)

    def get_queryset(self, **kwargs):
        schema_id = self.kwargs['id']
        return Dataset.objects.all().filter(schema=schema_id).order_by("-created_at")
