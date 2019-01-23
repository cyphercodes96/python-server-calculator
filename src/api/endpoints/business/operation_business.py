import uuid

from src.database import db
from src.database.models import Operation
from src.util.logging import trace
from src.util.utc_parser import utcnow


@trace('debug')
def create_operation(numb0, operator, numb1, result, current_user_id):
    created_ts = utcnow()
    operation = Operation(
        user_id=current_user_id,
        number0=numb0,
        operator=operator,
        number1=numb1,
        result=result,
        created_ts=created_ts)
    db.session.add(operation)
    db.session.flush()
    db.session.commit()
    return operation

@trace('debug')
def search_operations(current_user_id, start_time, stop_time):
    filters = [Operation.user_id == current_user_id]
    if start_time:
        filters.append(Operation.created_ts >= start_time)
    if stop_time:
        filters.append(Operation.created_ts <= stop_time)
    return Operation.query.filter(*filters).all()