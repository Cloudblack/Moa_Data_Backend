from flask import Flask, request
from flask_restful import Api, Resource
import json

app = Flask(__name__)
api = Api(app)


def open_json():
    file_path = "job.json"

    with open(file_path, 'r+') as file:
        jobs = json.load(file)
        return jobs['job']


class JsonAPI(Resource):

    def get(self, job_id):
        # 특정 job 실행, 아마 queue로..?
        pass

    def patch(self):
        # 특정 job 수정
        pass

    def delete(self, job_id):
        # 특정 job 삭제
        with open('job.json', 'r+') as file:
            jobs = json.load(file)
            for job in jobs['job']:
                if job_id == job['job_id']:
                    jobs['job'].pop(job_id)
            json.dumps(jobs)


class Create_json(Resource):
    # job 정보 저장
    def post(self):
        response = request.data.decode('utf-8')
        data = json.loads(response)

        with open('job.json', 'r+') as file:
            file_data = json.load(file)
            file_data["job"].append(data)
            file.seek(0)
            json.dump(file_data, file, indent=4)


api.add_resource(Create_json, '/api')
api.add_resource(JsonAPI, '/api/<int:job_id>')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
