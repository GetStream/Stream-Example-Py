#!/bin/bash

python manage.py migrate
python manage.py after_deploy
