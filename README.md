# Flask-User starter app v1.0

This code base serves as starting point for writing your next Flask application.

This branch is for Flask-User v1.0.

For Flask-User v0.6, see [the Flask-User-Starter-App v0.6 branch](https://github.com/lingthio/Flask-User-starter-app/tree/v0.6).

## Code characteristics

* Tested on Python 2.6, 2.7, 3.3, 3.4, 3.5 and 3.6
* Well organized directories with lots of comments
    * app
        * commands
        * models
        * static
        * templates
        * views
    * tests
* Includes test framework (`py.test` and `tox`)
* Includes database migration framework (`alembic`)
* Sends error emails to admins for unhandled exceptions


## Setting up a development environment

We assume that you have `git` and `virtualenv` and `virtualenvwrapper` installed.

    # Clone the code repository into ~/dev/my_app
    mkdir -p ~/dev
    cd ~/dev
    git clone https://github.com/lingthio/Flask-User-starter-app.git my_app

    # Create the 'my_app' virtual environment
    mkvirtualenv -p PATH/TO/PYTHON my_app

    # Install required Python packages
    cd ~/dev/my_app
    workon my_app
    pip install -r requirements.txt


# Configuring SMTP

Copy the `local_settings_example.py` file to `local_settings.py`.

    cp app/local_settings_example.py app/local_settings.py

Edit the `local_settings.py` file.

Specifically set all the MAIL_... settings to match your SMTP settings

Note that Google's SMTP server requires the configuration of "less secure apps".
See https://support.google.com/accounts/answer/6010255?hl=en

Note that Yahoo's SMTP server requires the configuration of "Allow apps that use less secure sign in".
See https://help.yahoo.com/kb/SLN27791.html


## Initializing the Database

    # Create DB tables and populate the roles and users tables
    python manage.py init_db

    # Or if you have Fabric installed:
    fab init_db


## Running the app

    # Start the Flask development web server
    python manage.py runserver

    # Or if you have Fabric installed:
    fab runserver

Point your web browser to http://localhost:5000/

You can make use of the following users:
- email `user@example.com` with password `Password1`.
- email `admin@example.com` with password `Password1`.


## Running the automated tests

    # Start the Flask development web server
    py.test tests/

    # Or if you have Fabric installed:
    fab test


## Trouble shooting

If you make changes in the Models and run into DB schema issues, delete the sqlite DB file `app.sqlite`.


## See also

* [FlaskDash](https://github.com/twintechlabs/flaskdash) is a starter app for Flask
  with [Flask-User](https://readthedocs.org/projects/flask-user/)
  and [CoreUI](https://coreui.io/) (A Bootstrap Admin Template).

## Acknowledgements

With thanks to the following Flask extensions:

* [Alembic](http://alembic.zzzcomputing.com/)
* [Flask](http://flask.pocoo.org/)
* [Flask-Login](https://flask-login.readthedocs.io/)
* [Flask-Migrate](https://flask-migrate.readthedocs.io/)
* [Flask-Script](https://flask-script.readthedocs.io/)
* [Flask-User](http://flask-user.readthedocs.io/en/v0.6/)

<!-- Please consider leaving this line. Thank you -->
[Flask-User-starter-app](https://github.com/lingthio/Flask-User-starter-app) was used as a starting point for this code repository.


## Authors

- Ling Thio -- ling.thio AT gmail DOT com


------------------------------------------




The first time you install you do:
python -m venv venv
venv\Scripts\activate.bat
pin install -r requirements.txt
python manage.py init_db  (this adds the sql db to the root folder)
python manage.py runserver
Open browser

After adding the Category and Book models you do:

Delete db from file explorer
python manage.py init_db  (this adds the sql db to the root folder)
python manage.py runserver
DELETE COOKIES! (https://github.com/lingthio/Flask-User/issues/238)
Open browser

This app comes from https://github.com/lingthio/Flask-User-starter-app.  According to the readme doc this is the users you can use:
You can make use of the following users:

email user@example.com with password Password1.
email admin@example.com with password Password1.
---------
After getting cloning the repo (https://github.com/lingthio/Flask-User-starter-app) the general idea is to modify it so it runs like my repo flask_book_plus_auth:

CUSTOMIZE FLASK_USER (https://flask-user.readthedocs.io/en/latest/customizing_forms.html)
  Create app/templates/flask_user folder
  Add templates from venv flask_user library
  Replace app/layout.html with new one (modify paths in nav slightly)
  Modify app/flask_user/common_base so it extends layout.html instead of flask_user_layout
  In app/settings.py change following lines to:
    USER_AFTER_LOGIN_ENDPOINT = 'books.home_page'
    USER_AFTER_LOGOUT_ENDPOINT = 'books.home_page'

CREATE BOOK BLUEPRINT AND BOOKS TEMPLATE FOLDER

Create app/templates/books folder.
Add book templates to folder
Modify paths in breadcrumbs of each template to point to books blueprint

Create new routes in app:
  Get routes from from my repo flask_book_plus_auth app.py
  Create a book_views.py blueprint (use main_views as model)
      Because I'm using the alchemy sql engine I have to make changes
      Change execute_sql to db.engine.execute_sql
      Make minor modifications to sql statements
        Unlike Tom's sql engine sqlalchemy wasn't returning a list of dictionaries.  So had to add extra code to do that conversion
  Change @app.route  to @main_blueprint.route (??still necessary??)
  Prepend "/books" to route url  (?? still necessary)
Took context processor that allows isAdmin function to run in nav template and placed it in app/_init_.py/create_app function.  (If you leave it in the blueprint it wont be available to the flask_user views)

REMOVE main_views.py BLUEPRINT:
Also need to remove reference to it in:
views/_init__.py
app/init__py
