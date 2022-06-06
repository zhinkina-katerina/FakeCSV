from django.forms import ModelForm, widgets
from .models import Schema, DataType, DataTypeProvider


class SchemaForm(ModelForm):
    class Meta:
        model = Schema
        fields = ('title', 'column_separator', 'string_character')

        widgets = {
            'title': widgets.TextInput(attrs={
                'class': 'form-control',
                'required': 'required'
            }),
            'column_separator': widgets.Select(attrs={
                'class': 'form-select',
                'required': 'required'
            }),
            'string_character': widgets.Select(attrs={
                'class': 'form-select',
                'required': 'required'
            })
        }


class DataTypeForm(ModelForm):
    class Meta:
        model = DataType
        fields = ('title', 'data_type', 'has_editable_range', 'minimum', 'maximum', 'order')
        widgets = {
            'data_type': widgets.Select(
                choices=DataTypeProvider().get_titles(),
                attrs={
                    'id': 'id_selector',
                    'class': 'form-select',
                }
            ),
            'title': widgets.TextInput(attrs={
                'class': 'form-control',
            }),
            'minimum': widgets.TextInput(attrs={
                'class': 'form-control',
            }),
            'maximum': widgets.TextInput(attrs={
                'class': 'form-control',
            }),
            'order': widgets.TextInput(attrs={
                'class': 'form-control',
            }),
        }
