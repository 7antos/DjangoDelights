py -m venv env
.\env\Scripts\activate & py -m pip install -r requirements.txt & cd DjangoDelights & python manage.py migrate --run-syncdb & python manage.py loaddata initial_db.json