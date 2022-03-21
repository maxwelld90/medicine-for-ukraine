# Medicine for Ukraine Static Site

This Pelican project creates the static HTML content required for the index and about pages.
Joined with the build of the React app, this completes the online offering.

## Running Locally

To run this locally, you need to do the following.

1. Create a new virtual environment. Python 3.8 or higher should work fine. (Tested on Python 3.8.12)
2. Install the requirements, using `pip install -r requirements.txt`
3. Run the command `make devserver`.
4. Navigate your browser to `http://127.0.0.1:8000/`.

## How it Works

We create a series of Markdown pages in the `content/pages/` directory. These pages are duplicated for each language we use (with each language using its own subdirectory). At the top of each Markdown file are a series of variable. An example is shown below.

```markdown
Title: Landing Page
Slug: index
Lang: de
save_as: index.html
showlinks: yes
```

Change the `Lang` variable to match the language being used. Ensure it complies with the code as shown in `LANGUAGES.json` (in the repository root).

Templates are in the `theme/templates/` directory. `page.html` is the main one.

## Referencing Variables

* The root URL (of the entire website) is referenced using ``{{ ROOT_URL }}``. E.g., it may yield `http://127.0.0.1:8000/`.
* The site URL (for a specific language) if referecned using ``{{ SITEURL_ABSOLUTE }}``. E.g., for English it may yield `http://127.0.0.1:8000/en/`.
* The current page name is specified by ``{{ output_file }}``.
* To link to the current document, use ``{{ SITEURL_ABSOLUTE | link(output_file) }}``.
* To link to the same page, in a different language, use ``{{ ROOT_URL | switch_language_link('es', output_file) }}``. Change ``es`` to whatever language code you wish.