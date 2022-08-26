#!/bin/bash
python3 -m venv env
source env/bin/activate
python3 -m pip install -r requirements.txt
cd DjangoDelights || exit
python3 manage.py migrate --run-syncdb
python3 manage.py loaddata initial_db.json
