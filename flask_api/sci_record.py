# sci_record.py

from datetime import datetime
from flask import abort, make_response


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

SCI_RECORD = {
    "Temp":{
        "id": 0,
        "timestamp": get_timestamp(),
    }
}

def read_all():
    return list(SCI_RECORD.values())

def create(record):
    id = record.get("id")

    if id and id not in id:
        SCI_RECORD[id] = {
            "id": id,
            "timestamp": get_timestamp(),
        }
        return SCI_RECORD[id], 201

    else:
        abort(
            406,
            f"Scientific record with id {id} already exists",
        )

def read_one(id):
    if id in SCI_RECORD:
        return SCI_RECORD[id]
    else:
        abort(
            404,
            f"Record with id {id} not found"
        )

def update(id, record):
    if id in SCI_RECORD:
        # add updates to fields
        SCI_RECORD[id]["timestamp"] = get_timestamp()
        return SCI_RECORD[id]
    else:
        abort(
            404,
            f"Record with id {id} not found"
        )

def delete(id):
    if id in SCI_RECORD:
        del SCI_RECORD[id]
        return make_response(
            f"{id} successfully deleted",
            200
        )
    else:
        abort(
            404,
            f"Person with last name {id} not found"
        )