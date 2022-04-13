#!/bin/bash

#
# Code for creating the database.
#

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <envfile_path>" >&2
  exit 1
fi

source ./env.prep.sh $1;
. virtualenvs/api/bin/activate;
cd api;
python manage.py makemigrations;
python manage.py migrate;
python manage.py createsuperuser;