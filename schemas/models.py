from django.db import models

class DataType(models.Model):
    title = models.CharField(max_length=120)
    data_type = models.CharField(max_length=120)
    minimum = models.IntegerField(blank=True)
    maximum = models.IntegerField(blank=True)
    has_editable_range = models.BooleanField(default=False)

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
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    structure = models.TextField()
    column_separator = models.CharField(max_length=10, default=',', choices=COLUMN_SEPARATOR_CHOICES)
    string_character = models.CharField(max_length=10, default='"', choices=STRING_CHARACTER_CHOICES)