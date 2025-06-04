#!/bin/bash
npm install

# Générer le CSS Tailwind
npm run build-css

python3 -m pip install -r requirements.txt
python3 manage.py migrate --noinput
python3 manage.py collectstatic --noinput