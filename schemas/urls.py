from django.urls import path
from . import views

urlpatterns = [
    path('', views.SchemeList.as_view(), name='schema_view'),
]