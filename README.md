# Python Stack Week 7 project: Finance Manager

## Dependencies:
* Python 3.11
* venv
* pip3

## Instalation:
`$ python3 -m venv venv` <br>
`$ source venv/bin/activate` (Mac/Linux) or `venv\Scripts\activate.bat` (Windows) <br>
`$ pip install -r requirements.txt` <br>

### Configuring env variables
1. Copy envsample content to .env file <br>
`$ cat envsample >> .env`
1. Generate SECRET_KEY env variable and add it to .env file <br>
`echo "SECRET_KEY="$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())') >> .env`


### Runing project:
If everything goes well it will be running on http://127.0.0.1:8000/perfil/home/ with command: <br>
`$ python manage.py runserver`
