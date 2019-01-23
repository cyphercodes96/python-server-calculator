import datetime
import logging.config
from flask import Flask, Blueprint, send_from_directory, json
import json as j
from flask_cors import CORS
from flask_migrate import Migrate
from src.api.endpoints.login import ns as login_namespace, jwt
from src.api.endpoints.users import ns as users_namespace
from src.api.endpoints.operation import ns as operations_namespace
from src import database
from src.api.restplus import api
from src.database import db

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('settings.cfg')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(seconds=app.config['JWT_ACCESS_TOKEN_EXPIRES'])
logging.config.fileConfig('logging.conf')
log = logging.getLogger('rotating_log')

migrate = Migrate(app, db)

def is_production_mode():
    return app.config['MODE'] == 'PROD'

def initialize_app(flask_app):
    blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
    api.init_app(blueprint)
    api.add_namespace(operations_namespace)
    api.add_namespace(users_namespace)
    api.add_namespace(login_namespace)

    flask_app.register_blueprint(blueprint)
    db.init_app(flask_app)
    jwt.init_app(flask_app)
    CORS(flask_app)

    return flask_app


initialize_app(app)


@app.cli.command()
def drop_tables():
    """Drops all tables."""
    if is_production_mode():
        raise Exception("Can't drop tables when running in production mode.")
    database.drop_database()
    #drop alembic_version table
    db.engine.execute('DROP TABLE IF EXISTS alembic_version;')


@app.cli.command()
def create_tables():
    """Creates all tables."""
    if is_production_mode():
        raise Exception("Can't create tables when running in production mode.")
    database.create_database()


@app.cli.command()
def recreate_tables():
    """Drops all tables, then creates all tables."""
    if is_production_mode():
        raise Exception("Can't recreate tables when running in production mode.")
    database.reset_database()


@app.cli.command()
def sample_data():
    """Populate the database with sample data."""
    if is_production_mode():
        raise Exception("Can't populate database with sample data when running in production mode.")


@app.cli.command()
def docs():
    """Dumps the API service document."""
    print(j.dumps(api.__schema__, indent=5))


def main():
    log.info('>>>>> Starting development server at http://{}/api/v1 <<<<<'.format(app.config['SERVER_NAME']))
    app.run(host='0.0.0.0')


if __name__ == "__main__":
    main()
