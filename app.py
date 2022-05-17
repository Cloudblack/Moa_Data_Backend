import json
import re
from flask import Flask, request, jsonify
from flask_api import status
from flask_restx import Api, resource

app = Flask(__name__)



@app.route('/')
def greeting():
    return "This is Test API!"

@app.route('/job', methods=['GET','POST'])
def post_job():
    
    if request.method == 'GET':
        with open('job.json','r') as f:
            json_data = json.load(f)
        print(json.dumps(json_data, indent="\t"))
        return json_data

    elif request.method == 'POST':

        data = json.loads(request.data)

        with open('job.json','r') as json_file:
            json_data = json.load(json_file)

        json_data.append(data)

        with open('job.json', 'w', encoding='utf-8') as make_file:
            json.dump(json_data, make_file, indent='\t')

        with open('job.json', 'r') as json_file:
            json_data = json.load(json_file)
        print(json.dumps(json_data, indent="\t"))
        return jsonify(json_data)
    
"""
data = {
    “job_id”: 1, 
    “job_name”: “Job1”,
    “task_list”: {"read": [“drop"], “drop":["write"], “write”:[]},
    “property”: {“read”: {“task_name”: “read”, “filename” : “path/to/a.csv”, “sep” :“,”}, “drop” : {“task_name”: “drop”, “column_name”: “date”}, “write” : {“task_name”: “write”, “filename” : “path/to/b.csv”, “sep”: “,”}
    }
"""

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)