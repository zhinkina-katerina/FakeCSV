from django.db import models


class DataType(models.Model):
    title = models.CharField(max_length=120)
    data_type = models.CharField(max_length=120)
    minimum = models.IntegerField(blank=True)
    maximum = models.IntegerField(blank=True)

class Schema(models.Model):
    title = models.CharField(max_length=100)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    structure = models.TextField()