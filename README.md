# Medicine for Ukraine

This is the Git repository for the [*Medicine for Ukraine*](https://medicineforukraine.org/) project.
This is a monorepo - we have several different components living here which all perform different functionality.

* `/api/` - houses the Python Django project which provides a REST API for communicating with the Google Sheet and backend database.
* `/front/` - houses the React app for the item request process.
* `/landing/` - houses the Python Pelican project that generates a series of static pages for the landing site (including the index and about pages).

In addition, the `LANGUAGES.json` file provides a list of all the languages that are supported by the `front` and `landing` components.
The `SHEETS.json` file also provides details on the Google spreadsheets that we are using (for recording link information and what items are actually required).

## Running the Project Locally

To run everything locally, you can go through the following steps. Note that for this to work, you need to have Python 3.8 installed, and a recent version of Node (David is using version v14.18).
You should also have developer tools installed, too. This includes `make` and Python virtual environments (i.e., the `virtualenv` command should be working).

1. **First, set up your environment variables.** There is a script and sample environment variables file you can use to do this.
`$ source ./env.prep.sh .env.development`

2. **Test your environment variables have been set up correctly.**
`$ echo $MEDICINE_SET`
This should return `true`.

3. **Make the project.** This will create the virtual environments and install all required packages (both for Python and Node), and build all files.
`$ make all`

4. **Setup the local database.** This will then create a small SQLite database. This step will also populate it with some sample data to get you started. Note that you should pass in your environment variables file to this script.
`$ ./create_db.sh .env.development`
You will be asked to enter a username, e-mail address, and password. This is for the superuser account that you can login to the server with once it is running.

5. **You can then run the two servers.** Content is accessible at port `8000`. The API server will be live on port `8001`.
`$ make devserver`