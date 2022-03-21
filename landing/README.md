# Medicine for Ukraine Static Site

This Pelican project creates the static HTML content required for the index and about pages.
Joined with the build of the React app, this completes the online offering.

Documentation in progress.

Root url: {{ ROOT_URL }}<br />
Site url: {{ SITEURL_ABSOLUTE }}<br />
Page name: {{ output_file }}<br />
Current page link (same language): {{ SITEURL_ABSOLUTE | link(output_file) }}<br />
Current page link (switching language): {{ ROOT_URL | switch_language_link('es', output_file) }}<br />