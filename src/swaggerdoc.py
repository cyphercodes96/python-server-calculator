from flask import json

from src.api.restplus import api

print(json.dumps(api.__schema__))