# REST api for TransferTo Calc #

Use the `flask` command to interact with the application, which requires the
`FLASK_APP` environment variable to point to `app.py`, with eg:

    export FLASK_APP="app.py"

If using [venv](https://docs.python.org/3/library/venv.html) the above line can
be added to the end of `venv/bin/activate` to be set in the virtual environment.
To run flask's development server use `flask run`, to load sample data use
`flask sample_data`.

### Instructions on getting the app running: ###
- Clone this repository.
- (Recommended) Have the project in a Python virtual env, with Python version 3.6
- Open up with an editor, PyCharm for example
- run "pip install -r requirements.txt" in project root directory
- Set up MySQL either installed locally or through docker, use standard port 3306
- In MYSQL, Create a database schema for the project, for example named 'calcdb'
- Ask for the _settings.cfg_ file, and add them a folder, _instance_ that you have to create manually
if you are using a virtual environment.
- Run the application. (either in IDE or command line `python app.py`)
- Go to http://localhost:8888/api/v1 to verify Swagger UI is up

### Some notes on Alembic (database migration tool) ###
Whenever you make a modification to the models.py (the data model), make sure to run `flask db migrate -m "commit message"`.
Then run `flask db upgrade` alternatively `flask db upgrade head`, which will update the database to the latest version.
Make sure there are no errors in the migration scripts and commit your migrations to git.

This is so everybody can stay in sync with the database and to keep a commit "history" of the database schema. 

### Automatic Deployement and Tests ###
This repo is connected to Semaphore for automatic deployment, so please always run the tests before a git push.
If you don't want to build, test and deploy your push automatically, just add the string "[ci skip]" inside your commit message.
