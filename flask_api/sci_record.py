# sci_record.py

from datetime import datetime

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

SCI_RECORD = {
    "Temp":{
        "timestamp": get_timestamp(),
    }
}

def read_all():
    return list(SCI_RECORD.values())