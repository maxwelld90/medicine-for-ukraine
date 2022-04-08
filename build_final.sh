#!/bin/sh

if [ $MEDICINE_ENVIRONMENT = production ]
then
    . virtualenvs/api/bin/activate;
    cd api;
    python manage.py collectstatic --clear --noinput;
    deactivate;

    cd ../;
    mkdir -p ../landing;
    rsync landing/out/ ../landing;
fi