import random
from faker import Faker
from django.conf import settings
from .models import DataType
import csv
from django.core.files import File
import os
import cloudinary.uploader
from pathlib import Path


class DatasetHandler:
    def __init__(self):
        self.DATATYPES = DataType.objects.all()
        self.rows_quantity = None
        self.schema = None
        self.dataset = None
        self.structure = None

        fake = Faker()
        self.dict_types_of_data = {
            'Full name': fake.name,
            'Email': fake.ascii_email,
            'Domain name': fake.domain_name,
            'Phone number': fake.phone_number,
            'Company name': fake.company,
            'Text': fake.paragraph,
            'Integer': random.randint,
            'Address': fake.address,
            'Date': fake.date,
            'Job': fake.job,
        }

    def generate_csv(self, dataset):
        self.dataset = dataset
        self.rows_quantity = dataset.rows_quantity
        self.schema = dataset.schema
        unsorted_structure = list(eval(self.schema.structure))
        self.structure = sorted(unsorted_structure, key=lambda x: x['order'])

        self.dataset.status = 'In_process'
        self.dataset.save()

        try:
            rows = self.get_rows_for_csv()
            self.set_to_file(rows)

            self.dataset.status = 'Completed'
            self.dataset.save()

        except Exception as e:
            self.dataset.status = 'Failed   '
            self.dataset.exception = str(e)
            self.dataset.save()



    def get_rows_for_csv(self):
        rows = []
        for _ in range(self.rows_quantity):
            rows.append({item.get('title'): self.generate_value(item) for item in self.structure})
        return rows

    def generate_value(self, item):
        data_type = item.get('data_type')
        minimum, maximum = self.get_min_and_max(item, data_type)

        if data_type == 'Integer':
            return self.dict_types_of_data[data_type](minimum, maximum)
        if data_type == 'Date':
            return self.dict_types_of_data[data_type]()
        elif data_type == 'Text':
            average = (minimum + maximum) / 2
            while True:
                result = self.dict_types_of_data[data_type](nb_sentences=average)
                quantity_sentence = len(result.split('. '))
                if maximum > quantity_sentence > minimum:
                    return result
        while True:
            result = self.dict_types_of_data[data_type]()
            if maximum > len(result) > minimum:
                return result

    def get_min_and_max(self, item, data_type):
        minimum = int(item.get('minimum') if item.get('minimum') != "" else self.DATATYPES.get(title=data_type).minimum)
        maximum = int(item.get('maximum') if item.get('maximum') != "" else self.DATATYPES.get(title=data_type).maximum)

        return minimum, maximum

    def set_to_file(self, rows):
        created_date = str(self.dataset.created_at).replace(' ', '_').replace(':', '-')[0:19]
        filename = f'dataset_{self.schema.id}_{created_date}.csv'
        path = Path(settings.MEDIA_ROOT).joinpath("datasets").joinpath(filename)

        if path.is_file():
            os.remove(path)

        fieldnames = [x['title'] for x in self.structure]

        with open(path, 'w', newline='') as f:
            writer = csv.DictWriter(
                f,
                fieldnames=fieldnames,
                delimiter=self.schema.column_separator,
                quotechar=self.schema.string_character
            )
            writer.writeheader()
            writer.writerows(rows)

        uploaded_file = cloudinary.uploader.upload(path, resource_type='raw')

        with open(path, mode='r', newline='') as f:
            self.dataset.csv_file.save(filename, File(f))

        self.dataset.url = uploaded_file['secure_url']
        self.dataset.save()
