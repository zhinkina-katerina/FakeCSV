from django.db import models
import json
from django.contrib.auth.models import User



class DataTypeManager(models.Manager):
    def get_titles(self):
        # queryset = self.get_queryset()
        # result = [(x.title, x.title) for x in queryset]
        return 'result'

    def get_items_have_range(self):
        # queryset = self.get_queryset()
        # result = {x.title: x.has_editable_range for x in queryset}
        # jsonString = json.dumps(result, indent=4)
        return 'jsonString'


class DataType(models.Model):
    title = models.CharField(max_length=120)
    data_type = models.CharField(max_length=120)
    minimum = models.IntegerField(blank=True)
    maximum = models.IntegerField(blank=True)
    has_editable_range = models.BooleanField(default=False)
    order = models.IntegerField(blank=True)

    objects = DataTypeManager()


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

