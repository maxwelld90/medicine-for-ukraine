# Medicine for Ukraine

This is the Git repository for the [*Medicine for Ukraine*](https://medicineforukraine.org/) project.
This is a monorepo - we have several different components living here which all perform different functionality.

* `/api/` - houses the Python Django project which provides a REST API for communicating with the Google Sheet and backend database.
* `/front/` - houses the React app for the item request process.
* `/landing/` - houses the Python Pelican project that generates a series of static pages for the landing site (including the index and about pages).

In addition, the `LANGUAGES.json` file provides a list of all the languages that are supported by the `front` and `landing` components.

## Running the Project Locally

To run the project locally, start the API in its own process.

```bash
$ export MEDICINE_ENVIRONMENT=debug
$ virtualenv -p python3.8 medicine_api
$ . medicine_api/bin/activate
$ cd api/
$ pip install -Ur requirements.txt
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```

Then run the `Makefile` in the repository root.

```bash
$ make all
$ make devserver
```

Point your browser to `http://127.0.0.1:3000`. You should see the landing page.