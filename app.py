import json

from flask import Flask, Response
from flask_cors import CORS
from flask_restx import Api, Resource

from utils.func import JobTask


app = Flask(__name__)
CORS(app)
api = Api(app)


class Job_json(Resource):

    def post(self, data):
        with open(self.FATH_JOB, 'w') as json_file:
            jobs = JobTask.read_job()
            job_id = str(data['job_id'])
            
            jobs[job_id] = {
                "job_name" : data["job_name"],
                "task_list" : data["task_list"],
                "property" : data["property"]
            }

            JobTask.write_json(jobs)

        return Response({"MESSAGE" : "JOB_CREATE_SUCCESS"}, status=201, mimetype="application/json")

    def get(self, job_id):
        pass
    

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
