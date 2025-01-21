#!/bin/sh
set -e
python3 manage.py migrate --noinput
python3 manage.py super
python3 manage.py generate_data
python3 manage.py runserver 0.0.0.0:8000
