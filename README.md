# Flask app (Dutch Atm)

## Setting up a development environment

`git` and `virtualenv`` installed.

    git clone https://github.com/lingthio/Flask-User-starter-app.git my_app

    # Create the 'venv' virtual environment

    virtualenv venv

    # Install required Python packages

    pip install -r requirements.txt


## Initializing the Database
    # Add DB url in local env variable
    SQLALCHEMY_DATABASE_URI = postgres://{user}:{password}@{hostname}:{port}/{database-name}
    
    # Create DB tables and populate the roles and users tables
    flask db init

    # migrate db:
    flask db migrate


Point your web browser to http://localhost:5000/


## Running the automated tests

    python -m unittest tests


With thanks to the following Flask extensions:

* [Alembic](http://alembic.zzzcomputing.com/)
* [Flask](http://flask.pocoo.org/)
* [Flask-Migrate](https://flask-migrate.readthedocs.io/)
