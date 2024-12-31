# sci_record.py

from datetime import datetime
from flask import jsonify, make_response, request
from django_api.api.models import SciRecord
from django_api.api.serializers import SciRecordSerializer
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from auth import token_required

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

#Placeholder
SCI_RECORD = {
    0:{
        "id": 0,
        "date": "1970-01-01",
        "time": "00:00",
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
# Function to return all records
def read_all():
    records = SciRecord.objects.all()
    serializer = SciRecordSerializer(records, many=True)
    return jsonify(serializer.data)  # Use Flask's jsonify

# Function to return one record by id
def read_one(id):
    try:
        record = SciRecord.objects.get(pk=id)
        serializer = SciRecordSerializer(record)
        return jsonify(serializer.data)  # Use Flask's jsonify
    except ObjectDoesNotExist:
        return make_response(jsonify({"error": "Record not found"}), 404)

# Function to create a new record
def create():
    # Get the request data
    data = request.json
    
    # Check if an 'id' is provided in the request. If not, let Django auto-increment it.
    id_provided = 'id' in data
    
    # Serialize the data and validate it
    serializer = SciRecordSerializer(data=data)
    
    if serializer.is_valid():
        try:
            # If an 'id' is provided, check for its validity and uniqueness
            if id_provided:
                # Ensure the 'id' is not empty or invalid
                if not isinstance(data['id'], int) or data['id'] <= 0:
                    return make_response(
                        jsonify({"error": "Invalid ID value. ID must be a positive integer."}),
                        status.HTTP_400_BAD_REQUEST
                    )
            
                # Explicitly check if the provided id already exists
                if SciRecord.objects.filter(id=data['id']).exists():
                    return make_response(
                        jsonify({"error": "Record with this ID already exists."}),
                        status.HTTP_400_BAD_REQUEST
                    )
                
                # Manually set the provided 'id' in the serializer's validated data
                serializer.validated_data['id'] = data['id']
                    
            
            # Save the record (this handles both auto-incrementing and manual ID)
            record = serializer.save()

            # Return a successful response with the created record's data
            return make_response(jsonify(serializer.data), status.HTTP_201_CREATED)

        # Handle any database integrity errors (e.g., unique constraints, duplicate keys)
        except IntegrityError as e:
            return make_response(
                jsonify({"error": "Integrity error: likely a duplicate ID or other issue."}),
                status.HTTP_400_BAD_REQUEST
            )

    # If the data is invalid, return validation errors
    return make_response(jsonify(serializer.errors), status.HTTP_400_BAD_REQUEST)

# Function to update an existing record
def update(id):
    try:
        record = SciRecord.objects.get(pk=id)
        for field, value in request.json.items():
            setattr(record, field, value)
        record.save()
        serializer = SciRecordSerializer(record)
        return make_response(jsonify(serializer.data), 200)  # Flask compatible response
    except SciRecord.DoesNotExist:
        return make_response(jsonify({"error": "Record not found"}), 404)
    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 400)

# Function to delete a record
def delete(id):
    try:
        record = SciRecord.objects.get(pk=id)
        record.delete()
        return make_response(jsonify({"message": f"Record {id} successfully deleted"}), 200)
    except SciRecord.DoesNotExist:
        return make_response(jsonify({"error": "Record not found"}), 404)

def delete_all():
    SciRecord.objects.all().delete()
    return make_response(jsonify({"success": "Records cleared"}), 200)