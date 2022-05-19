from cgitb import handler
import json
import os.path
from collections import deque
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
        with open(self.FILE_PATH, 'r', encoding="UTF-8") as f:
            return json.load(f)

    def write_json(self, new_job):
        with open(self.FILE_PATH, 'w') as f:
            json.dump(new_job, f, ensure_ascii=False, indent='\t')

    def duplicate_check(self, job_id):
        job_file = self.read_json()
        if job_id in list(job_file.keys()):
            return Response(response=f'JOB_ID_ALREADY_EXIST', status=400, mimetype='application/json')

    def existence_check(self, job_id):
        job_file = self.read_json()
        
        if job_id in list(job_file.keys()):
            return Response(response=f'JOB_ID_DOES_NOT_EXIST', status=404, mimetype='application/json')


@Job.route('')
class JobPost(Resource):
    
    @Job.expect(job_model)
    def post(self):
        """
            job데이터를 받아 job file에 저장합니다.
        """
        handler = JobHandler()
        data = json.loads(request.data)
        job_id = str(data['job_id'])
        job_file = handler.read_json()
        handler.duplicate_check(job_id)

        job_file[job_id] = {
            'job_name': data['job_name'],
            'task_list': data['task_list'],
            'property': data['property']
        }

        handler.write_json(job_file)
        return Response(response='JOB_CREATE_SUCCESS', status=201, mimetype='application/json')


# 전달 받은 job_id를 job.json 파일에 찾아 삭제/수정
@Job.route('/<string:id>')
class JobUpdateDelete(Resource):
    def delete(self, id):
        """
            해당 id 데이터를 삭제합니다.
        """
        job_file = JobHandler().read_json()
        print(job_file)
        print(id)
        
        if JobHandler().existence_check(id):

            result = job_file.pop(id)

        JobHandler().write_json(job_file)

        return Response(response=f'{result}', status=204, mimetype='application/json')

    @Job.expect(job_model)
    def put(self, job_id):
        """
            해당 job_id 데이터를 수정합니다.
        """
        data = json.loads(request.data)

        job_file = JobHandler().read_json()

        JobHandler().existence_check(job_id)

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

        JobHandler().write_json(job_file)

        return Response(response=f'{job_file[job_id]}', status=200, mimetype='application/json')



class FindOrder:
    """
    김석재
    DAG 를 활용해 순서를 정하는 함수
    """

    def __init__(self, task_list):
        self.task_count = {}
        self.task_list = task_list
        self.qu = deque()
        self.result = []
        # _find_qu 함수를 재활용 하기위해 =1 값으로 통일
        for x in self.task_list:
            self.task_count[x] = 1

    def _find_qu(self, qu=None):
        """
        실행 순서대로 큐를 쌓는 함수
        첫번째만 qu가없어 모든 진입차수를 -1 해주고 시작한다
        (시작값을 1로 줬기때문에 0을 찾는것과 마찬가지)
        qu가 있을때는 qu다음에 나오는 값들의 진입값만 -1을 하고
        진입차수가 0인것을 찾아 qu에 넣는다
        """
        if qu:
            task_list = self.task_list[qu]
        else:
            task_list = self.task_list

        for x in task_list:
            self.task_count[x] -= 1

            if self.task_count[x] == 0:
                self.qu.append(x)

    def __call__(self):
        """
        받은 데이터를 바탕으로 진입차수를 계산한 후
        큐 스택이 없어질때까지 반목문을 돌며 순서를 찾는다
        순환되는 데이터라면 큐 스택이 쌓이지않는다
        """
        for x in self.task_list:
            for y in self.task_list[x]:
                self.task_count[y] += 1
        self._find_qu()

        while self.qu:
            select_qu = self.qu.popleft()
            self.result.append(select_qu)
            self._find_qu(select_qu)

        if not self.result:
            return "CIRCULATION_VALUE"

        return self.result


class TaskExcutor:
    """
    김석재
    앞서 구한 순서를 바탕으로 task들을 실행 한다
    이미 실행한 태스크로 결과값이 나와있다면 결과값을 제공
    (현재는 중복되어있다는 말만 뜸)
    """

    def __init__(self, job_data):
        self.job_data = job_data
        self.in_path = f'./{self.job_data["property"]["read"]["filename"]}'
        self.out_path = f'./{self.job_data["property"]["write"]["filename"]}'
        self.exist = None
        if os.path.isfile(self.out_path):
            self.exist = "RESULT_ALREADY_EXIST"

    def read(self):
        self.df = pd.read_csv(self.in_path,self.job_data["property"]["read"]['sep'])

    def drop(self):
        if self.job_data["property"]["drop"]['column_name'] not in list(self.df.columns):
            return Response(response='삭제하려는 column이 존재하지 않습니다.',
                             status=404, mimetype='application/json')
        self.df = self.df.drop("date", axis=1)

    def write(self):
        self.df.to_csv(self.out_path)


@Job.route('/<string:id>/start')
class JobStart(Resource):
    
    def __init__(self, nothing):
        with open("job.json", "r") as f:
            self.job_data = json.load(f)
    
    def _get_order(self, id):
        finder = FindOrder(self.job_data[str(id)]["task_list"])
        return finder()
    
    def get(self, id):
        '''
            전달받은 job_id를 job file에서 찾아 task들을 실행합니다.
        '''         
        
        task_excutor = TaskExcutor(self.job_data[str(id)])
        if task_excutor.exist:
            return Response(response='task 실행에 실패하였습니다.', status=400, mimetype='application/json') 

        for task in self._get_order(id):
            result = getattr(task_excutor, task)()
            if result:
                return result                
        return Response(response=task_excutor.df.to_json(), status=200, mimetype='application/json')
        
       
        