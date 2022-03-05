#!/usr/bin/env bash

# Env
~/.pyenv/shims/pip install -r requirements.txt
~/.pyenv/shims/pip freeze > requirements-frozen.txt

# Django
~/.pyenv/shims/python neighborhood/manage.py runserver
~/.pyenv/shims/python neighborhood/manage.py load_tax_data