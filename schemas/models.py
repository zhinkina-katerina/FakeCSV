from django.db import models
import json
from django.contrib.auth.models import User


class DataType(models.Model):
    title = models.CharField(max_length=120)
    data_type = models.CharField(max_length=120)
    minimum = models.IntegerField(blank=True)
    maximum = models.IntegerField(blank=True)
    has_editable_range = models.BooleanField(default=False)
    order = models.IntegerField(blank=True)


class Schema(models.Model):
    COLUMN_SEPARATOR_CHOICES = (
        (",", "Comma (,)"),
        (";", "Semicolon (;)"),
        ("|", "Pipe (|)"),
    )

    STRING_CHARACTER_CHOICES = (
        ('"', 'Double-quote (")'),
        ("*", "Asterisk (*)"),
    )

    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    structure = models.TextField()
    column_separator = models.CharField(max_length=10, default=',', choices=COLUMN_SEPARATOR_CHOICES)
    string_character = models.CharField(max_length=10, default='"', choices=STRING_CHARACTER_CHOICES)


class Dataset(models.Model):
    STRING_STATUS_CHOICES = (
        ('New', 'New'),
        ('In_process', 'In Process'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    )
    csv_file = models.FileField(upload_to='datasets/', null=True, blank=True)
    status = models.CharField(max_length=20, default='New', choices=STRING_STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)
    rows_quantity = models.IntegerField(default=0)
    url = models.URLField(default="")
    exception = models.TextField(default="")


class DataTypeProvider:
    def __init__(self):
        self.model = DataType

    def get_all(self):
        return self.model.objects.all()

    def get_items_have_range(self):
        result = {x.title: x.has_editable_range for x in self.get_all()}
        json_string = json.dumps(result, indent=4)
        return json_string

    def get_titles(self):
        return [(x.title, x.title) for x in self.get_all()]
