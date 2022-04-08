# The `medicine-for-ukraine` API

A Django 4.0.3 project that serves the Medicine for Ukraine project's REST API. Provides the means for accessing information on delivery addresses, recipients, items, and links. Data is pulled from a relational database, or the Google Sheets documents that are linked to the project.

## Requirements

The Medicine for Ukraine API requires the following.

- Python 3.8 (developed with Python 3.8.12).
- `virtualenv`, with an environment setup using `requirements.txt`.
- The Redis cache server (optional).

## Environment Variables

There are a number of environment variables that the API uses to instantiate itself. These can be found in the file `../.env.sample`. There is also a preconfigured file, `../.env.development`. This second file contains the variables needed to get the API to run on your local computer. See Step 3 below.

## Setting Up

To run the API on your local computer, you need to run the following commands.

### Configure your Environment

Your environment must be setup before you can run the API.

1. Activate your virtual environment.
2. If you have not installed the required Python packages, run `$ pip install -r requirements.txt`.
3. Set up the environment variables. From the `api` directory, run `$ source ../env.prep.sh ../.env.development`.
4. Verify the environment variables are configured with `$ echo $MEDICINE_SET`. This should return `true`.

### Setup the Database

If you have not yet setup the database locally, you must run these commands with your virtual environment activated. Note that if you change the database structure, you must also run `makemigrations` before running `migrate`.

1. `$ python manage.py migrate`
2. `$ python manage.py migrate medicine_api`
3. `$ python manage.py createsuperuser` (Follow the instructions to create a user account.)

Some sample data is also provided for you to use. To populate the database with sample data, run the following command.

`$ python manage.py populate_db`

The Medicine for Ukraine API also requires that a script periodically checks the links sheet to check if there have been any new links added, or changes to existing link metadata (e.g., price, whether the item is in stock, etc.). This is done via the `cron_item_populator.py` script. On the production server, this would be called every *x* minutes; you should also call this at least once to populate the `LinkMetadata` model.

`$ python manage.py cron_link_populator`

### Running the Server

Running the server will then involve you executing the following command.

`$ python manage.py runserver`

This by default will start the API server in debug mode on port `8000` of your local computer.