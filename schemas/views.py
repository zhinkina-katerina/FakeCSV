from django.shortcuts import redirect, get_object_or_404, HttpResponse
from django.views.generic import ListView, TemplateView, View
import json
from .models import Schema, Dataset, DataTypeProvider
from .forms import SchemaForm, DataTypeForm
from django.contrib.auth.mixins import LoginRequiredMixin


class SchemeList(LoginRequiredMixin, ListView):
    template_name = 'index.html'

    def get_queryset(self):
        return Schema.objects.filter(user=self.request.user).order_by("created_at")


class SchemeCreateView(LoginRequiredMixin, TemplateView):
    template_name = "create_schema.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SchemeCreateView, self).get_context_data(**kwargs)
        data_type_provider = DataTypeProvider()
        context['object_list'] = data_type_provider.get_all()
        context['form_schema_options'] = SchemaForm()
        context['form_data_type'] = DataTypeForm()
        context['items_have_range'] = data_type_provider.get_items_have_range()
        return context

    def post(self, request, *args, **kwargs):
        new_schema_json = json.loads(request.POST.get('json_object', {}))
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
        forms = [DataTypeForm(initial=item) for item in list(eval(schema.structure))]
        context['form_schema_options'] = SchemaForm(initial=initial_dict)
        context['forms'] = forms
        context['object'] = schema
        return context

    def post(self, request, *args, **kwargs):
        new_schema_json = json.loads(request.POST.get('json_object'))
        schema = Schema.objects.get(id=self.kwargs['id'])
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
        Dataset.objects.create(
            status="New",
            schema=Schema.objects.filter(id=id).first(),
            rows_quantity=request.POST.get('rows'),
            user=request.user
        )
        return redirect('dataset_list', id=id)

    def get_queryset(self, **kwargs):
        schema_id = self.kwargs['id']
        return Dataset.objects.all().filter(schema=schema_id).order_by("created_at")
