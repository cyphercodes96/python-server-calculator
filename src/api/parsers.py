import werkzeug
from flask_restplus import reqparse
from flask_restplus.inputs import boolean
from src.util.utc_parser import parse


operation_arguments = reqparse.RequestParser()
operation_arguments.add_argument('start_time', type=parse, location='args', required=False)
operation_arguments.add_argument('end_time', type=parse, location='args', required=False)
