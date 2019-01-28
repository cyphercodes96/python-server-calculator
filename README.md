# REST api for TransferTo Calc #

Ensure to download `nanobox` which also requires `docker`:

https://docs.nanobox.io/install/

Run `nanobox start` inside the root directory of the application.

Nanobox allows us to run our application in two different environments:

# Development Environment: #

You'll be required to add a `DNS Alias` && set up `environment variables` to properly run and access the API.

Nanobox offers us a set of commands:

https://docs.nanobox.io/cli/

To add the `DNS Alias`, run:

`nanobox dns add local flask.local` # <--- The API will run under "http://`DNS Alias`:5000/api/v1"

As for the environment variables, you'll need the following:
  FLASK_APP = app.py
  JWT_SECRET_KEY = 3zpqvDJ22jkHPPPYpreD62k1RAc
  DEBUG = False
  MODE = DEV
  RESETPASS_SALT = jVdayk8WACSa123sS
  RESETPASS_SECRET_KEY = wUUDsPKE69PVVBJuekbN5KT

SALTS && KEYS can be changed however needed.

Run: `nanobox evar add local FLASK_APP=app.py JWT_SECRET_KEY=3zpqvDJ22jkHPPPYpreD62k1RAc DEBUG=False MODE=DEV RESETPASS_SALT=jVdayk8WACSa123sS RESETPASS_SECRET_KEY=wUUDsPKE69PVVBJuekbN5KT'

# Dry-run Environment: #

You'll be required to add a `DNS Alias` && set up `environment variables` to properly run and access the API.

Nanobox offers us a set of commands:
https://docs.nanobox.io/cli/

To add the `DNS Alias` under the dry-run environment, run:

`nanobox dns add dry-run flask.local` # <--- The API will run under "http://`DNS Alias`/api/v1"

As for the environment variables, you'll need the following:
  FLASK_APP = app.py
  JWT_SECRET_KEY = 3zpqvDJ22jkHPPPYpreD62k1RAc
  DEBUG = False
  MODE = DEV
  RESETPASS_SALT = jVdayk8WACSa123sS
  RESETPASS_SECRET_KEY = wUUDsPKE69PVVBJuekbN5KT

SALTS && KEYS can be changed however needed

Run: `nanobox evar add dry-run FLASK_APP=app.py JWT_SECRET_KEY=3zpqvDJ22jkHPPPYpreD62k1RAc DEBUG=False MODE=DEV RESETPASS_SALT=jVdayk8WACSa123sS RESETPASS_SECRET_KEY=wUUDsPKE69PVVBJuekbN5KT'


Use the `flask` command to interact with the application, which requires the
`FLASK_APP` environment variable to point to `app.py`, with eg:

    export FLASK_APP="app.py" ( if not already added as an environment variable, or was not detected inside nanobox after         running `nanobox run` )

If using [venv](https://docs.python.org/3/library/venv.html) the above line can # <--- recommended
be added to the end of `venv/bin/activate` to be set in the virtual environment.
To run flask's development server use `flask run`

### Instructions on getting the app running: ###
- Clone this repository.
- (Recommended) Have the project in a Python virtual env, with Python version 3.6
- Open up with an editor, PyCharm for example
- run "nanobox run python app.py" in project root directory
- Go to http://flask.local:5000/api/v1 to verify Swagger UI is up

### Some notes on Alembic (database migration tool) ###
Whenever you make a modification to the models.py (the data model), make sure to run `flask db migrate -m "commit message"`.
Then run `flask db upgrade` alternatively `flask db upgrade head`, which will update the database to the latest version.
Make sure there are no errors in the migration scripts and commit your migrations to git.

This is so everybody can stay in sync with the database and to keep a commit "history" of the database schema. 

### Automatic Deployement and Tests ###
This repo is connected to Semaphore for automatic deployment, so please always run the tests before a git push.
If you don't want to build, test and deploy your push automatically, just add the string "[ci skip]" inside your commit message.

# Live Deployed API: #
https://personal-calc-core.nanoapp.io/api/v1/

# Live CI / CD Using Semaphore: #
https://www.useloom.com/share/5b4f86aff162448ebc8d73cb80838558
