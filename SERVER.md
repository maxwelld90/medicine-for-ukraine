# Instructions for Server Deployment

**Updated: 1 March 2022**

## Updating the Server

Update the server by updating this repository. At present, the static website is hosted on the server at `/srv/medicine-for-ukraine/git-repo/`. If you make a change to the repository and wish to see the change reflected online, `cd` to this directory and simply `git pull`.

## Updating Static Content

At present, the static page is located in the repository at `landing/index.html`. Right now, we just edit the HTML file directly, but if this gets more complex we'll have to consider something like Jekyll for our static content.

You can see the page structure consists of a series of language blocks. You can edit each of these blocks as you see fit. Please make sure each paragraph fits inside `<p></p>` tags. To highlight the paragraph in red (for urgent things) you can do `<p class="urgent">...</p>`.

## Multilingual Edits
There's some JavaScript that is able to show and hide selective elements on the page depending on what language the user selects at any time.

Assign a class of `multilingual` to *any* element that you wish to assign to a specific language. Add a further class to identify the language, like `pl` for Polish. See the example below.

```html
<h1 class="multilingual pl">Pomóż Ukrainie!</h1>
```

Or this `<p></p>` example.

```html
<p class="urgent multilingual pl">
    Potrzebujemy 2000 krótkofalówek dla oddziałów frontowych.
</p>
```

This example above is a Polish message, with the `urgent` class applied (making it stand out).

The language code (e.g., `pl`) **MUST** match the codes at the top of the document, where the links are placed to select a language.

```html
<ul>
    <!-- Language Links -->
    <li><a href="#" class="multilingual-selector" data-language="EN">EN</a></li>
    <li><a href="#" class="multilingual-selector" data-language="ES">ES</a></li>
    <li><a href="#" class="multilingual-selector" data-language="PL">PL</a></li>
</ul>
```

To add a new language, just copy the `<li>` element and replace the `data-language` attribute with the code for the language. Don't forget to also change the text displayed to the user (the text inside the `<a>` tag).

The `data-language` attribute is **converted to lowercase to match with the class you assign to an element**. For example, the following language link

```html
<li><a href="#" class="multilingual-selector" data-language="IT">IT</a></li>
```

Will show the following element

```html
<p class="multilingual it">
    Grazie!
</p>
```

But will also hide this.

```html
<p class="multilingual en">
    Thank you!
</p>
```

Hopefully this will be made easier as we develop the site!
Contact David if you have any questions.