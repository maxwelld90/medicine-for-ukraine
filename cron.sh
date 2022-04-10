#!/bin/bash

#
# Code for launching the CRON job.
# Processes LinkMetadata from the Google Sheets source.
#

echo "Launching Medicine for Ukraine CRON job...";

[ ! -d "./virtualenvs/api/" ] && { echo "Virtual environment could not be found. Did you run make all?"; exit 1; }

source ./env.prep.sh .env.development;
. virtualenvs/api/bin/activate;
cd api;
python manage.py cron_link_populator;