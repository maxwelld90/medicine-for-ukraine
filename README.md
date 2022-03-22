# Medicine for Ukraine

This is the Git repository for the [*Medicine for Ukraine*](https://medicineforukraine.org/) project.
This is a monorepo - we have several different components living here which all perform different functionality.

* `/api/` - houses the Python Django project which provides a REST API for communicating with the Google Sheet and backend database.
* `/front/` - houses the React app for the item request process.
* `/landing/` - houses the Python Pelican project that generates a series of static pages for the landing site (including the index and about pages).

In addition, the `LANGUAGES.json` file provides a list of all the languages that are supported by the `front` and `landing` components.

More documentation will be written up shortly. Refer to the `README` files in each respective directory for instructions on how to run each component locally.