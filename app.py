import json
import re
from flask import Flask, request, jsonify
from flask_api import status
from flask_restx import Api, resource

app = Flask(__name__)

"""
류성훈
"""

# 전달 받은 job 정보를 job.json 파일에 저장
@app.route('/job', methods=['GET','POST'])
def post_job():
    # Job file 조회
    if request.method == 'GET':
        with open('job.json','r') as f:
            json_data = json.load(f)
        return json_data

    # Job file 저장
    elif request.method == 'POST':
        data = json.loads(request.data)
        
        with open('job.json', 'r') as f:
            job_file = json.load(f)
    
        job_file[data['job_id']] = {
                                "job_name": data['job_name'],
                                "task_list": data['task_list'],
                                "property": data['property']
                                 }                

        with open("job.json", "w") as json_file:
            json.dump(job_file, json_file, indent="\t")

        return job_file
    
# 전달 받은 job_id를 job.json 파일에 찾아 삭제/수정
@app.route('/job/<string:id>', methods=['DELETE','PUT'])
def update_delete_job(id):

    # 해당 job_id 데이터 삭제
    if request.method == 'DELETE':
        with open('job.json', 'r') as f:
            job_file = json.load(f)
            
        if id not in job_file.keys():
            return jsonify("삭제하려는 데이터의 job_id가 존재하지 않습니다.") # 예외처리 해주기
        
        del(job_file[id])

        with open("job.json", "w") as json_file:
            json.dump(job_file, json_file, indent="\t")

        return job_file
    
    # 해당 job_id 데이터 수정
    elif request.method == 'PUT':
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
@app.route('/job/<string:id>/start', methods=['GET'])
def start_job(id):
    with open('job.json', 'r') as f:
        job_file = json.load(f)
    
    if id not in job_file.keys():
        return jsonify("실행하려는 데이터의 job_id가 존재하지 않습니다.") # 예외처리 해주기

    
    print(job_file)
    return job_file
    

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)