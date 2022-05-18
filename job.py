import json
import re
from flask import request, jsonify
from flask_restx import Resource, Api, Namespace
import pandas as pd


"""
류성훈
"""
    
Job = Namespace('Job')

# 전달 받은 job 정보를 job.json 파일에 저장
@Job.route('')
class JobPost(Resource):
    # Job file 저장
    def post(self):
        data = json.loads(request.data)
        
        with open('job.json', 'r') as f:
            job_file = json.load(f)
    
        job_file[str(data['job_id'])] = {
                                "job_name": data['job_name'],
                                "task_list": data['task_list'],
                                "property": data['property']
                                 }                

        with open("job.json", "w") as json_file:
            json.dump(job_file, json_file, indent="\t")

        return job_file


# 전달 받은 job_id를 job.json 파일에 찾아 삭제/수정
@Job.route('/<string:id>')
class JobUpdateDelete(Resource):
    # 해당 job_id 데이터 삭제
    def delete(self, id):
        with open('job.json', 'r') as f:
            job_file = json.load(f)
            
        if id not in job_file.keys():
            return jsonify("삭제하려는 데이터의 job_id가 존재하지 않습니다.") # 예외처리 해주기
        
        del(job_file[id])

        with open("job.json", "w") as json_file:
            json.dump(job_file, json_file, indent="\t")

        return job_file # 삭제에 성공했다는 처리
    
    # 해당 job_id 데이터 수정
    def put(self, id):
        data = json.loads(request.data)

        with open('job.json', 'r') as f:
            job_file = json.load(f)

        if id not in job_file.keys():
            return jsonify("수정하려는 데이터의 job_id가 존재하지 않습니다.") # 예외처리 해주기

        job_file[id] = {
                            "job_name": data['job_name'],
                            "task_list": data['task_list'],
                            "property": data['property']
                        }
        with open("job.json", "w") as json_file:
            json.dump(job_file, json_file, indent="\t")

        return job_file[id]


# 전달 받은 job_id를 job.json 파일에서 찾아 task들을 실행
@Job.route('/<string:id>/start')
class JobStart(Resource):
    def get(self, id):
        with open('job.json', 'r') as f:
            job_file = json.load(f)
        
        if id not in job_file.keys():
            return jsonify("실행하려는 데이터의 job_id가 존재하지 않습니다.") # 예외처리 해주기
        
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
                # return df.to_json()
            elif task == 'drop':
                if task_property["column_name"] not in list(df.columns):
                    print("삭제하려는 column이 존재하지 않습니다.") # 예외처리 필요
                else:
                    df = df.drop([task_property["column_name"]], axis='columns')
                    # return df.to_json()
            elif task == 'write':
                df.to_csv(task_property['filename'], sep=task_property['sep'], na_rep='NaN', index=False)
                return df.to_json()

        return job_file