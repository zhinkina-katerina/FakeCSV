import random
from faker import Faker
from django.conf import settings
from .models import Dataset, DataType
import csv
from django.core.files import File
import os
import cloudinary.uploader


class DatasetHandler():
    def __init__(self):
        self.DATATYPES = DataType.objects.all()
        self.rows_quantity = None
        self.schema = None
        self.dataset = None
        self.structure = None

    def generate_csv(self, dataset):
            self.dataset = dataset
            self.rows_quantity = dataset.rows_quantity
            self.schema = dataset.schema
            unsorted_structure = list(eval(self.schema.structure))
            self.structure = sorted(unsorted_structure, key=lambda d: d['order'])

            self.dataset.status = 'In_process'
            self.dataset.save()

            rows = self.get_csv_rows()
            self.set_to_file(rows)

            self.dataset.status = 'Completed'
            self.dataset.save()


    def sort_dictionary(self, dictionary):
        sorted_keys = sorted(dictionary, key=dictionary.get)
        sorted_dict = {}
        for i in sorted_keys:
            sorted_dict[i] = dictionary[i]
        return sorted_dict

    def get_csv_rows(self):
        rows = []
        for i in range(self.rows_quantity):
            row = {}
            for item in self.structure:
                title = item.get('title')
                row[title] = self.generate_value(item)
            rows.append(row)
        return rows

    def generate_value(self, item):
        fake = Faker()

        dict_types_of_data = {
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
        data_type = item.get('data_type')
        minimum, maximum = self.get_min_and_max(item, data_type)

        if (data_type == 'Integer'):
            return dict_types_of_data[data_type](minimum, maximum)
        if (data_type == 'Date'):
            return dict_types_of_data[data_type]()
        elif (data_type == 'Text'):
            average = (minimum + maximum) / 2
            while True:
                result = dict_types_of_data[data_type](nb_sentences=average)
                quantity_sentensec = len(result.split('. '))
                if (maximum > quantity_sentensec > minimum):
                    return result
        while True:
            result = dict_types_of_data[data_type]()
            if (maximum > len(result) > minimum):
                return result

    def get_min_and_max(self, item, data_type):
        minimum = item.get('minimum')
        if minimum == '':
            minimum = self.DATATYPES.get(title=data_type).minimum
        maximum = item.get('maximum')
        if maximum == '':
            maximum = self.DATATYPES.get(title=data_type).maximum
        minimum = int(minimum)
        maximum = int(maximum)
        return minimum, maximum

    def set_to_file(self, rows):

        date = str(self.dataset.created_at).replace(' ', '_') \
                   .replace(':', '-')[0:19]
        filename = f"dataset_{self.schema.id}_{date}.csv"
        path = str(settings.MEDIA_ROOT) + "\\datasets\\" + filename

        if (os.path.exists(path) and os.path.isfile(path)):
            os.remove(path)

        fieldnames = [x['title'] for x in self.structure]

        with open(path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile,
                                    fieldnames=fieldnames,
                                    delimiter=self.schema.column_separator,
                                    quotechar=self.schema.string_character
                                    )
            writer.writeheader()
            writer.writerows(rows)

        uploaded_file = cloudinary.uploader.upload(path, resource_type='raw')


        with open(path, mode='r', newline='') as csvfile:
            self.dataset.csv_file.save(filename, File(csvfile))
            csvfile.close()

        self.dataset.url = uploaded_file['secure_url']
        self.dataset.save()




