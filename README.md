# FakeCSV

The purpose of this project is create CSV files with fake (dummy) data.
The user can create a scheme according to which the CSV file will be created, specify the number of rows. The file will be generated by Celery and Faker and is available for download (the file is located on Cloudinary).

You can check the project on Hiroku:
https://fakecsvplaneks.herokuapp.com/
Please use these login details.
Login: admin_2
Password: admin_2

# Technology

- Python 3.7

- Django 3.2.13

- Celery + Redis

- Faker

- Cloudinary

- Postgresql

- Heroku


# Installation 

## Local

1. Clone the repository

2. Create a virtual environment in the root folder `python -m venv venv`

3. Activate the virtual environment `venv\Scripts\activate.bat`

4. Install the dependencies `pip install -r requirements.txt`

5. Copy and fill in with your data `cp .env.example .env`

6. Run database migrations `python manage.py migrate`
 
7. Run fixteres  `python manage.py loaddata datatypes.json`

8. In terminal-1 run celery-beat
`celery -A alarm_in_Ukraine beat`

9. ВIn terminal-2 run celery worker
`celery -A alarm_in_Ukraine worker -l INFO`

10. To start the server, enter `python manage.py runserver`


## Heroku
1. Set up environment variables Heroku in Setting/Config_Vars

2. Log in to your Heroku

3. Use Git to clone app's source code to your local machine

4. Deploy app to Heroku using Git - `git push heroku main`




