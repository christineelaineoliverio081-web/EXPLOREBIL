#!/usr/bin/env bash
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

# Copy media files to static files for production
cp -r media/* staticfiles/ 2>/dev/null || :

python manage.py collectstatic --no-input
python manage.py migrate