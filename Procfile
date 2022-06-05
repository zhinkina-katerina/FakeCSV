release:python manage.py migrate
release:python  manage.py loaddata datatypes.json
web: python manage.py runserver 0.0.0.0:$PORT
worker: celery -A FakeCSV beat & celery -A FakeCSV worker -l INFO
