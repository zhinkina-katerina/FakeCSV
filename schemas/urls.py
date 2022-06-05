from django.urls import path
from . import views

urlpatterns = [
    path('', views.SchemeList.as_view(), name='schema_view'),
    path('<int:id>/dataset', views.DatasetView.as_view(), name="dataset_list"),
    path('create_schema/', views.SchemeCreateView.as_view(), name='schema_create'),
    path('delete_schema/<int:id>/', views.DeleteSchemaView.as_view(), name='schema_delete'),
    path('edit_schema/<int:id>/', views.SchemeEditView.as_view(), name='schema_edit')
]