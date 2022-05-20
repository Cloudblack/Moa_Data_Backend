import sys
sys.path.append(".")
import pytest
import json
import app
from job import JobHandler

"""
    류성훈
"""

class TestJob:

    FILE_PATH = './job.json'

    job_handler = JobHandler()

    test_data = {
                    "job_id": "test", 
                    "job_name": "Test",
                    "task_list": {"read": ["drop"], "drop":["write"], "write":[]},
                    "property": {
                                "read": {"task_name": "read", "filename" : "path/to/a.csv", "sep" :","}, 
                                "drop" : {"task_name": "drop", "column_name": "date"}, 
                                "write" : {"task_name": "write", "filename" : "path/to/b.csv", "sep": ","}}
                }   

    put_data = {
                    "job_id": "test", 
                    "job_name": "Test_put",
                    "task_list": {"read": ["drop"], "drop":["write"], "write":[]},
                    "property": {
                                "read": {"task_name": "read", "filename" : "path/to/a.csv", "sep" :","}, 
                                "drop" : {"task_name": "drop", "column_name": "date"}, 
                                "write" : {"task_name": "write", "filename" : "path/to/b.csv", "sep": ","}}
                }   

    put_data_1 = {
                    "job_id": "test1", 
                    "job_name": "Test_put",
                    "task_list": {"read": ["drop"], "drop":["write"], "write":[]},
                    "property": {
                                "read": {"task_name": "read", "filename" : "path/to/a.csv", "sep" :","}, 
                                "drop" : {"task_name": "drop", "column_name": "date"}, 
                                "write" : {"task_name": "write", "filename" : "path/to/b.csv", "sep": ","}}
                }  

    @pytest.fixture
    def api(self):
        test_api = app.app
        api = test_api.test_client()
        return api


    @pytest.fixture
    def generate_data(self, api):
        # 테스트 데이터를 생성
        resp = api.post(
            '/jobs',
            data=json.dumps(self.test_data),
            content_type='application/json'
        )
        return True
    

    def reset_data(self, api):
        # 생성했던 테스트케이스를 삭제해서 데이터 원상복구
        job_file = self.job_handler.read_json()
        if not job_file.get(str("test"), None) is None:
            del(job_file["test"])
            self.job_handler.write_json(job_file)
        return True


    def test_job_post(self, api):
        # Job data test
        resp = api.post(
            '/jobs',
            data=json.dumps(self.test_data),
            content_type='application/json'
        )
        self.reset_data(api)

        assert resp.status_code == 201


    def test_job_post_duplitated(self, api, generate_data):
        # 같은 job_id를 중복으로 POST 했을 경우
        resp = api.post(
            '/jobs',
            data=json.dumps(self.test_data),
            content_type='application/json'
        )
        self.reset_data(api)

        assert resp.status_code == 409
        

    def test_job_get_list(self, api):
        # job.json에서 job list를 조회
        resp = api.get(
            '/jobs'
            )

        assert resp.status_code == 200


    def test_job_get_detail(self, api, generate_data):
        # 특정 job_id의 data 조회
        resp = api.get(
            '/jobs/test'
        )
        self.reset_data(api)
        assert resp.status_code == 200


    def test_job_delete(self, api, generate_data):
        # 해당 job_id의 data 삭제
        resp = api.delete(
            '/jobs/test'
        )
        assert resp.status_code == 204


    def test_job_delete_not_exist(self, api):
        # 존재하지 않는 job_id의 data를 삭제하려 했을 경우
        resp = api.delete(
            '/jobs/test_invalid'
        )
        assert resp.status_code == 404


    def test_job_put(self, api, generate_data):
        # 해당 job_id의 job_name 수정
        resp = api.put(
            '/jobs/test',
            data=json.dumps(self.put_data),
            content_type='application/json'
        )

        with open(self.FILE_PATH, 'r') as f:
            job_file = json.load(f)

        self.reset_data(api)
        assert job_file['test']['job_name'] == self.put_data['job_name']
        assert resp.status_code == 200
        
    
    def test_job_put_not_exist(self, api):
        # 수정하려는 데이터의 job_id가 존재하지 않은 경우
        resp = api.put(
            '/jobs/test_not_exist',
            data=json.dumps(self.put_data),
            content_type='application/json'
        )
        assert resp.status_code == 404


    def test_job_put_dismatch(self, api, generate_data):
        # parameter job_id와 request body 의 job_id가 일치하지 않은 경우
        resp = api.put(
            '/jobs/test',
            data=json.dumps(self.put_data_1),
            content_type='application/json'
        )
        self.reset_data(api)
        assert resp.status_code == 400

