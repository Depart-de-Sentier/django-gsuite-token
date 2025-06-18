# django-gsuite-token

A very simple plugin that can use GSuite as the email backend for Django apps

## Installation

* Set the environment variable `GOOGLE_TOKEN_FILEPATH` to the filepath of the `token.json` file produced when following the [quickstart Python procedure](https://developers.google.com/gmail/api/quickstart/python).
* Add this line to the Django settings: `EMAIL_BACKEND='django_gsuite_token.GSuiteEmailBackend'`
