#!/bin/bash

cp ../LANGUAGES.json ./src/LANGUAGES.json
mkdir ./public/static/css
mkdir ./public/static/fonts
rsync -a ../landing/theme/static/css ./public/static
rsync -a ../landing/theme/static/fonts ./public/static
rsync -a ../landing/theme/static/img ./public/static