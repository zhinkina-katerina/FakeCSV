from celery import shared_task
from .models import Dataset
from .dataset_handler import DatasetHandler


@shared_task
def search_for_new_dataset():
    datasets = Dataset.objects.filter(status='New')
    for dataset in datasets:
        DatasetHandler().generate_csv(dataset)
