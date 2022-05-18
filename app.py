from flask import Flask
from flask_restful import Api, Resource
from utils.utils import JobsHandler, TaskHandler

app = Flask(__name__)
api = Api(app)


class JobsAPI(Resource, JobsHandler):

    # job 정보 저장
    def post(self):
        response = self.get_response()
        jobs = self._get_all_jobs()

        jobs.append(response)

        self._control_job(jobs)
        return 201


class JobAPI(Resource, JobsHandler):
    """
        job 정보 수정
        {'job_name': 'test'}
    """
    def patch(self, job_id):
        try:
            jobs = self._get_all_jobs()
            _, job = self._indexing(job_id, jobs)
            data = self.get_response()

            job['job_name'] = data['job_name']

            self._control_job(jobs)
            return 'Success', 200
        except:
            return 204

    def delete(self, job_id):
        # job 정보 삭제
        try:
            jobs = self._get_all_jobs()
            index, _ = self._indexing(job_id, jobs)

            jobs.pop(index)

            self._control_job(jobs)
            return 'Success', 200
        except:
            return 204


class TaskAPI(Resource, JobsHandler):
    # job의 task 실행
    def get(self, job_id):
        jobs = self._get_all_jobs()
        _, job = self._indexing(job_id, jobs)

        task_handler = TaskHandler()
        for task in job['task_list'].keys():
            if task == 'read':
                task_handler.read(job)
            elif task == 'drop':
                task_handler.drop(job)
            elif task == 'write':
                task_handler.write(job)
        return 200


api.add_resource(JobsAPI, '/api/jobs')
api.add_resource(JobAPI, '/api/jobs/<int:job_id>')
api.add_resource(TaskAPI, '/api/jobs/<int:job_id>/task')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
