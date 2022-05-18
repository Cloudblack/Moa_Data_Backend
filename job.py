import json
import re
import resource
from flask import Response, request
from flask_restx import Resource, Api, Namespace, fields
import pandas as pd


"""
류성훈
"""
    
Job = Namespace('Job')

job_model =Job.model('job_model', {
    'job_json': fields.String(description='input job-data')
})

# 전달 받은 job 정보를 job.json 파일에 저장
@Job.route('')
class JobPost(Resource):
    @Job.expect(job_model)
    def post(self):
        """
            job데이터를 받아 job file에 저장합니다.
        """
        data = json.loads(request.data)
        
        with open('job.json', 'r') as f:
            job_file = json.load(f)

        if str(data["job_id"]) in list(job_file.keys()):
            return Response(response="job_id가 이미 존재합니다.", status=400, mimetype="application/json")

        job_file[str(data['job_id'])] = {
                                "job_name": data['job_name'],
                                "task_list": data['task_list'],
                                "property": data['property']
                                 }                

        with open("job.json", "w") as json_file:
            json.dump(job_file, json_file,ensure_ascii=False, indent="\t")

        return Response(response="%s" % data, status=200, mimetype="application/json")


# 전달 받은 job_id를 job.json 파일에 찾아 삭제/수정
@Job.route('/<string:id>')
class JobUpdateDelete(Resource):
    def delete(self, id):
        """
            해당 job_id 데이터를 삭제합니다.
        """
        with open('job.json', 'r') as f:
            job_file = json.load(f)
            
        if id not in job_file.keys():
            return Response(response="삭제하려는 job_id가 존재하지 않습니다.", status=404, mimetype="application/json")
        
        result = job_file[id]
        del(job_file[id])
        with open("job.json", "w") as json_file:
            json.dump(job_file, json_file, indent="\t")

        return Response(response="%s" % result, status=200, mimetype="application/json")
    
    @Job.expect(job_model)
    def put(self, id):
        """
            해당 job_id 데이터를 수정합니다.
        """
        data = json.loads(request.data)

        with open('job.json', 'r', encoding='UTF-8') as f:
            job_file = json.load(f)

        if id not in job_file.keys():
            return Response(response="수정하려는 데이터의 job_id가 존재하지 않습니다.", status=404, mimetype="application/json")

        if str(id) != str(data['job_id']):
            return Response(response="요청한 job_id와 json의 job_id가 일치하지 않습니다.", status=400, mimetype="application/json")

        job_file[id] = {
                            "job_name": data['job_name'],
                            "task_list": data['task_list'],
                            "property": data['property']
                        }
        with open("job.json", "w", encoding='UTF-8') as json_file:
            json.dump(job_file, json_file, ensure_ascii=False, indent="\t")

        return Response(response="%s" % job_file[id], status=200, mimetype="application/json")


@Job.route('/<string:id>/start')
class JobStart(Resource):
    def get(self, id):
        """
            전달받은 job_id를 job file에서 찾아 task들을 실행합니다.
        """
        with open('job.json', 'r') as f:
            job_file = json.load(f)
        
        if id not in job_file.keys():
            return Response(response="실행하려는 데이터의 job_id가 존재하지 않습니다.", status=404, mimetype="application/json")
        
        job_file = job_file[str(id)]

        # task_list에서 task_order추출 (read가 먼저 시작된다고 가정)
        task_list = job_file["task_list"]
        task_order = []

        cur = 'read'
        while True:
            if task_list[cur] == []:
                task_order.append(cur)
                break
            else:
                task_order.append(cur)
                cur = task_list[cur][0]

        tasks_property = job_file["property"]

        # task 기능별로 실행
        for task in task_order:
            task_property = tasks_property[task]
            if task == 'read':
                # read path/to/a.csv to DataFrame
                df = pd.read_csv(task_property['filename'], sep=task_property['sep'])
            elif task == 'drop':
                if task_property["column_name"] not in list(df.columns):
                    Response(response="삭제하려는 column이 존재하지 않습니다.", status=404, mimetype="application/json")
                else:
                    df = df.drop([task_property["column_name"]], axis='columns')
            elif task == 'write':
                df.to_csv(task_property['filename'], sep=task_property['sep'], na_rep='NaN', index=False)
                return Response(response="%s" % df.to_json(), status=200, mimetype="application/json")

        return Response(response="task 실행에 실패하였습니다.", status=400, mimetype="application/json")