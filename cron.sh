#!/bin/bash

#
# Code for launching the CRON job.
# Processes LinkMetadata from the Google Sheets source.
#

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <envfile_path>" >&2
  exit 1
fi

echo "Launching Medicine for Ukraine CRON job...";

[ ! -d "/srv/medicine-for-ukraine/git-repo/" ] && { echo "Are you running this script on the production server? Can't find path."; exit 1; }
[ ! -d "/srv/medicine-for-ukraine/git-repo/virtualenvs/api/" ] && { echo "Virtual environment could not be found. Did you run make all?"; exit 1; }

cd /srv/medicine-for-ukraine/git-repo;
source ./env.prep.sh $1;
. virtualenvs/api/bin/activate;
cd api;
python manage.py cron_link_populator;