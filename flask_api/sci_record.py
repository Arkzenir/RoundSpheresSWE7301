# sci_record.py

from datetime import datetime
from flask import abort, make_response
from flask import jsonify, request
from django_api.api.models import SciRecord

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

SCI_RECORD = {
    0:{
        "id": 0,
        "date": "01-01-1970",
        "time": "00.00",
        "time_offset": 0,
        "coordinate": [0.0,0.0],
        "air_tempature": 0.0,
        "humidity": 0.0,
        "wind_speed": 0.0,
        "wind_direction": 0.0,
        "precipitation": 0.0,
        "haze": 0.0,
        "water_tempature": 0.0,
        "notes": "",
        "timestamp": get_timestamp(),
    },
    1:{
        "id": 1,
        "date": "09-11-2001",
        "time": "09.03",
        "time_offset": -5,
        "coordinate": [40.7128,74.0060],
        "air_tempature": 20.0,
        "humidity": 1021,
        "wind_speed": 9.36,
        "wind_direction": 320.15,
        "precipitation": 29.5,
        "haze": 11.9,
        "water_tempature": 13.15,
        "notes": "Specific date, time, coord etc.",
        "timestamp": get_timestamp(),
    },
}

#def read_all():
#    return list(SCI_RECORD.values())

def read_all():
    records = SciRecord.objects.all()
    return jsonify(list(records))

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