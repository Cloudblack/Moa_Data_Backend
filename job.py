import json

import pandas as pd
from flask import Response, request
from flask_restx import Resource, Namespace, fields


"""
류성훈
"""

Job = Namespace('Job')

job_model = Job.model('job_model', {
    'job_json': fields.String(description='input job-data')
})


class JobHandler:
    FILE_PATH = './job.json'

    def read_json(self):
        with open(self.FILE_PATH, 'r') as f:
            return json.load(f)

    def write_json(self, new_job):
        with open(self.FILE_PATH, 'w') as f:
            json.dump(new_job, f, ensure_ascii=False, indent='\t')

    def duplicate_check(self, job_id):
        job_file = self.read_json()

        if job_id in list(job_file.key()):
            return Response(response=f'JOB_ID_ALREADY_EXIST', status=400, mimetype='application/json')

    def existence_check(self, job_id):
        job_file = self.read_json()

        if not job_id in list(job_file.key()):
            return Response(response=f'JOB_ID_DOES_NOT_EXIST', status=404, mimetype='application/json')


@Job.route('')
class JobPost(Resource):

    @Job.expect(job_model)
    def post(self):
        """
            job데이터를 받아 job file에 저장합니다.
        """
        data = json.loads(request.data)
        job_id = str(data['job_id'])
        job_file = JobHandler.read_json()

        JobHandler.duplicate_check(job_id)

        job_file[job_id] = {
            'job_name': data['job_name'],
            'task_list': data['task_list'],
            'property': data['property']
        }

        JobHandler.write_json(job_file)

        return Response(response='JOB_CREATE_SUCCESS', status=201, mimetype='application/json')


# 전달 받은 job_id를 job.json 파일에 찾아 삭제/수정
@Job.route('/<string:id>')
class JobUpdateDelete(Resource):
    def delete(self, job_id):
        """
            해당 job_id 데이터를 삭제합니다.
        """
        job_file = JobHandler.read_json()

        JobHandler.existence_check(job_id)

        result = job_file.pop(job_id)

        JobHandler.write_json(job_file)

        return Response(response=f'{result}', status=204, mimetype='application/json')

    @Job.expect(job_model)
    def put(self, job_id):
        """
            해당 job_id 데이터를 수정합니다.
        """
        data = json.loads(request.data)
        job_file = JobHandler.read_json()

        JobHandler.existence_check(job_id)

        """
            변경하고자 하는 job_id는 패스 파라미터로 url 에서 따오고
            변경하고자 하는 내용은 request.body에 담겨옴.
            이 경우 url에서 따온 job_id와 body에 담긴 job_id를 비교하는 로직
        """
        if str(job_id) != str(data['job_id']):
            return Response(response='요청한 job_id와 json의 job_id가 일치하지 않습니다.', status=400, mimetype='application/json')

        job_file[job_id] = {
            'job_name': data['job_name'],
            'task_list': data['task_list'],
            'property': data['property']
        }

        JobHandler.write_json(job_file)

        return Response(response=f'{job_file[job_id]}', status=200, mimetype='application/json')


@Job.route('/<string:id>/start')
class JobStart(Resource):
    def get(self, id):
        '''
            전달받은 job_id를 job file에서 찾아 task들을 실행합니다.
        '''
        with open('job.json', 'r') as f:
            job_file = json.load(f)

        if id not in job_file.keys():
            return Response(response='실행하려는 데이터의 job_id가 존재하지 않습니다.', status=404, mimetype='application/json')

        job_file = job_file[str(id)]

        # task_list에서 task_order추출 (read가 먼저 시작된다고 가정)
        task_list = job_file['task_list']
        task_order = []

        cur = 'read'
        while True:
            if task_list[cur] == []:
                task_order.append(cur)
                break
            else:
                task_order.append(cur)
                cur = task_list[cur][0]

        tasks_property = job_file['property']

        # task 기능별로 실행
        for task in task_order:
            task_property = tasks_property[task]
            if task == 'read':
                # read path/to/a.csv to DataFrame
                df = pd.read_csv(
                    task_property['filename'], sep=task_property['sep'])
            elif task == 'drop':
                if task_property['column_name'] not in list(df.columns):
                    Response(response='삭제하려는 column이 존재하지 않습니다.',
                             status=404, mimetype='application/json')
                else:
                    df = df.drop([task_property['column_name']],
                                 axis='columns')
            elif task == 'write':
                df.to_csv(
                    task_property['filename'], sep=task_property['sep'], na_rep='NaN', index=False)
                return Response(response='%s' % df.to_json(), status=200, mimetype='application/json')

        return Response(response='task 실행에 실패하였습니다.', status=400, mimetype='application/json')
