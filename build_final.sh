#!/bin/sh

if [ $MEDICINE_ENVIRONMENT = production ]
then
    . virtualenvs/api/bin/activate;
    cd api;
    python manage.py collectstatic --clear --noinput;
    deactivate;

    cd ../;

    mv ./landing/out/static/browserconfig.xml ./landing/out/browserconfig.xml;
    mv ./landing/out/static/favicon.ico ./landing/out/favicon.ico;
    mv ./landing/out/static/manifest.json ./landing/out/manifest.json;

    mkdir -p ../landing;
    rsync -r landing/out/ ../landing;
fi