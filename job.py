import json
import pandas as pd
import os.path

from collections import deque
from flask import Response, request
from flask_restx import Resource, Namespace, fields


"""
    작성자 : 류성훈, 권상현
    리뷰어 : 김석재, 권상현, 정미정
"""


Job = Namespace('Job')

job_model = Job.model('job_model', {
    'job_json': fields.String(description='input job-data')
})


class JobHandler():
    """
        권상현
        job.json 파일을 불러오거나 새로 쓰기 위한 클래스입니다.
    """
    FILE_PATH = './job.json'

    def read_json(self, job_id=None):
        with open(self.FILE_PATH, 'r') as f:
            job_file = json.load(f)

            if job_id:
                return job_file[str(job_id)]

            return job_file

    def write_json(self, new_job):
        with open(self.FILE_PATH, 'w') as f:
            json.dump(new_job, f, indent='\t')


@Job.route('')
class JobPostListGetView(Resource):
    job_handler = JobHandler()

    @Job.expect(job_model)
    def post(self):
        """
            류성훈
            job데이터를 받아 job file에 저장합니다.
        """
        data = json.loads(request.data)
        job_id = data['job_id']
        job_file = self.job_handler.read_json()

        if job_file.get(str(job_id), None):
            return Response(
                response='MESSAGE : JOB_ID_ALREADY_EXIST',
                status=409, mimetype='application/json'
            )

        job_file[job_id] = {
            'job_name': data['job_name'],
            'task_list': data['task_list'],
            'property': data['property']
        }

        self.job_handler.write_json(job_file)

        return Response(
            response='MESSAGE : JOB_CREATE_SUCCESS', status=201, mimetype='application/json'
        )

    def get(self):
        """
            권상현
            전제 job list를 불러옵니다.
        """
        job_file = self.job_handler.read_json()

        return Response(
            response=f'MESSAGE : SUCCESS,\nDATA = \n{job_file}',
            status=200, mimetype='application/json'
        )


# 전달 받은 job_id를 job.json 파일에 찾아 삭제/수정
@Job.route('/<string:job_id>')
class JobRetrieveUpdateDeleteView(Resource):
    job_handler = JobHandler()

    def get(self, job_id):
        """
            권상현
            패스파라미터로 입력 받은 job_id를 검색해 불러옵니다.
        """
        job = self.job_handler.read_json(job_id)

        return Response(
            response=f'MESSAGE : SUCCESS,\nDATA = \n{job}',
            status=200, mimetype='application/json'
        )

    def delete(self, job_id):
        """
            류성훈
            해당 job_id 데이터를 삭제합니다.
        """
        job_file = self.job_handler.read_json()

        if job_file.get(str(job_id), None) is None:
            return Response(
                response='MESSAGE : JOB_ID_DOES_NOT_EXIST',
                status=404, mimetype='application/json'
            )

        else:
            del(job_file[job_id])
            self.job_handler.write_json(job_file)

        return Response(
            response='MESSAGE : JOB_DELETE_SUCCESS',
            status=204, mimetype='application/json'
        )

    @Job.expect(job_model)
    def put(self, job_id):
        """
            류성훈
            해당 job_id 데이터를 수정합니다.
        """
        data = json.loads(request.data)
        job_file = self.job_handler.read_json()

        if not job_file.get(str(job_id), None):
            return Response(
                response='MESSAGE : JOB_ID_DOES_NOT_EXIST',
                status=404, mimetype='application/json'
            )

        """
            변경하고자 하는 job_id는 패스 파라미터로 url 에서 따오고
            변경하고자 하는 내용은 request.body에 담겨옴.
            이 경우 url에서 따온 job_id와 body에 담긴 job_id를 비교하는 로직
        """
        if str(job_id) != str(data['job_id']):
            return Response(
                response='MESSAGE : DIS_MATCH_JOB_ID',
                status=400, mimetype='application/json'
            )

        job_file[job_id] = {
            'job_name': data['job_name'],
            'task_list': data['task_list'],
            'property': data['property']
        }

        self.job_handler.write_json(job_file)

        return Response(
            response=f'MESSAGE : SUCCESS,\nDATA = \n{job_file[job_id]}',
            status=200, mimetype='application/json'
        )


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
        self.df = pd.read_csv(
            self.in_path, self.job_data["property"]["read"]['sep'])

    def drop(self):
        if self.job_data["property"]["drop"]['column_name'] not in list(self.df.columns):
            return Response(response='MESSAGE : COLUMN_DOES_NOT_EXIST',
                            status=404, mimetype='application/json')
        self.df = self.df.drop("date", axis=1)

    def write(self):
        self.df.to_csv(self.out_path)


@Job.route('/<string:job_id>/start')
class JobStart(Resource):

    def __init__(self, _):
        self.job_data = JobHandler().read_json()

    def _get_order(self, job_id):
        finder = FindOrder(self.job_data[str(job_id)]["task_list"])
        return finder()

    def get(self, job_id):
        '''
            전달받은 job_id를 job file에서 찾아 task들을 실행합니다.
        '''

        task_excutor = TaskExcutor(self.job_data[str(job_id)])
        if task_excutor.exist:
            return Response(
                response='MESSAGE : TASK_ALREADY_EXIST', 
                status=400, mimetype='application/json'
            )

        for task in self._get_order(job_id):
            result = getattr(task_excutor, task)()
            if result:
                return result

        return Response(
            response=task_excutor.df.to_json(), 
            status=200, mimetype='application/json'
        )


'''
@Job.route('/<string:job_id>/start')
class JobStartView(Resource):
    """
        류성훈
    """
    job_handler = JobHandler()
    def get(self, job_id):
        """
            전달받은 job_id를 job file에서 찾아 task들을 실행합니다.
        """
        job_file = self.job_handler.read_json()[str(job_id)]
        self.job_handler.existence_check(job_id)
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
'''