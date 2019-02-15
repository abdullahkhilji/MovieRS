#!/bin/sh
source /home/app/venv/bin/activate
flask db upgrade
flask translate compile
#exec gunicorn -b :5000 --access-logfile - --error-logfile - moviers:moviers
python /home/app/app.py
