from django.urls import path
from . import views

urlpatterns = [
    path('', views.SchemeList.as_view(), name='schema_view'),
    path('edit_schema/', views.SchemeEditView.as_view(), name='schema'),
]