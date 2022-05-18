import json

from flask import Flask, request
from flask_cors import CORS
from flask_restx import Api, Resource

from func.func import JobTask, IndexTask


app = Flask(__name__)
CORS(app)
api = Api(app)


class Job_json(Resource):

    def post(self, data):
        with open(self.FATH_JOB, 'w') as json_file:
            job_list = JobTask.read_job()
            index_list = IndexTask.read_index()


            job_list.append(data)

            self._write_json(job_list, json_file)


    # todos = {}
    # count = 1

    # @api.route('/todos')
    # class TodoPost(Resource):
    #     def __init__(self):
    #         self.todos = todos
    #         self.count = count

    #     def post(self):
    #         idx = self.count
    #         self.count += 1
    #         todos[idx] = request.json.get('data')

    #         return {
    #             'todo_id': idx,
    #             'data': todos[idx]
    #         }

    # @api.route('/todos/<int:todo_id>')
    # class TodoSimple(Resource):
    #     def get(self, todo_id):
    #         return {
    #             'todo_id': todo_id,
    #             'data': todos[todo_id]
    #         }

    #     def put(self, todo_id):
    #         todos[todo_id] = request.json.get('data')
    #         return {
    #             'todo_id': todo_id,
    #             'data': todos[todo_id]
    #         }

    #     def delete(self, todo_id):
    #         del todos[todo_id]
    #         return {
    #             "delete" : "success"
    #         }

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
