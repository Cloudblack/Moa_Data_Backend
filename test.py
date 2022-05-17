import json

import requests

BASE_URL = "http://127.0.0.1/"
data = {
    "job_id": 5,
    "job_name": "Job5",
    "task_list": {
        "read": [
            "drop"
        ],
        "drop": [
            "write"
        ],
        "write": [

        ]
    },
    "property": {
        "read": {
            "task_name": "read",
            "filename": "path/to/a.csv",
            "sep": ","
        },
        "drop": {
            "task_name": "drop",
            "column_name": "date"
        },
        "write": {
            "task_name": "write",
            "filename": "path/to/b.csv",
            "sep": ","
        }
    }
}
# response = requests.post(BASE_URL + 'api', data=json.dumps(data))
response = requests.delete(BASE_URL + 'api/3')
