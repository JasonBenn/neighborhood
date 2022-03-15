#!/usr/bin/env bash

# Deploying
~/.pyenv/shims/python neighborhood/manage.py collectstatic  # push new styles to s3
/Users/jasonbenn/.pyenv/versions/3.10.0/envs/neighborhood/bin/gunicorn --chdir neighborhood neighborhood.wsgi
heroku config
heroku logs --tail

# Env
~/.pyenv/shims/pip install -r requirements.txt
~/.pyenv/shims/pip freeze > requirements-frozen.txt

# Django
~/.pyenv/shims/python neighborhood/manage.py runserver
~/.pyenv/shims/python neighborhood/manage.py load_tax_data

# Database
pg_dump neighborhood --table houses_zillowdata -f /Users/jasonbenn/code/neighborhood/neighborhood/data/backups/2022-03-07_zillow.sql
pg_dump neighborhood -f /Users/jasonbenn/Desktop/data/backups/2022-03-14_pm_neighborhood_ratings.sql
pg_restore --verbose --clean --no-acl --no-owner -h localhost -U jasonbenn -d neighborhood latest.dump
# CAREFUL: heroku pg:push postgresql://localhost:5432/neighborhood DATABASE_URL
