# Python Stack Week 7 project: Finance Manager

## Dependencies:
* Python 3.11
* venv
* pip3

## Instalation:
`$ python3 -m venv venv`
`$ source venv/bin/activate` (Mac/Linux) or `venv\Scripts\activate.bat` (Windows)
`$ pip install -r requirements.txt`

### Configuring env variables
1. Copy envsample content to .env file
`$ cat envsample >> .env`
1. Generate SECRET_KEY env variable and add it to .env file
`echo "SECRET_KEY="$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())') >> .env`


### Runing project:
If everything goes well it will be running on http://127.0.0.1:8000/perfil/home/ with command:
`$ python manage.py runserver`
