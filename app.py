from ensurepip import version
from pydoc import describe
from flask import Flask, request
from flask_restx import Resource, Api
import json
from utils.utils import *

app = Flask(__name__)
api = Api(app,
          version='beta 1.0',
          title = 'Moa Data API',
          describe= 'API document',)
          #doc="/api-docs")



check = CheckData()


@api.route("/api/jobs")
class JobDataC(Resource):
    """
        json 형식의 data를 추가한다
        data_check를 통해 중복과 입력할때 key가 없으면 추가할 수 없다
    """

    def __init__(self, nothing):
        self.json_excutor = JsonExcutor()
        self.job_data = self.json_excutor.get_data()
        self.keys = list(self.job_data.keys())

    def post(self):
        """
            데이터를 받아 저장
            입력 데이터 형식
            {
            "job_name" : "Job6",
            "task_list" : {
                "read" : ["drop"],
                "drop" : ["write"],
                "write" : []
            },
            "property" :
                {
                    "read": {
                        "task_name": "read",
                        "filename" : "path/to/a6.csv",
                        "sep" :","
                    },
                    "drop" : {
                        "task_name": "drop",
                        "column_name": "date"
                    },
                    "write" : {
                        "task_name": "write",
                        "filename" : "path/to/b6.csv",
                        "sep": ","
                    }
                }

        }

        """
        create_data = request.json
        result = check.data(create_data, self.job_data)
        if result:
            return result
        # 마지막 id +1 아니면 빈칸 채워야할까?
        job_id = int(self.keys.pop()) + 1

        self.job_data[job_id] = create_data

        self.json_excutor.save_data()

        return self.job_data[job_id]


@api.route("/api/jobs/<int:id>")
class JobDataRUD(Resource):
    """
        id를 입력받아 자세히보기 , 수정 , 삭제를 수행한다
    """

    def __init__(self, nothing):
        self.json_excutor = JsonExcutor()
        self.job_data = self.json_excutor.get_data()

    def get(self, id):
        check_id = check.id(self.job_data, id)
        if check_id:
            return check_id
        return self.job_data[str(id)]

    def put(self, id):
        check_id = check.id(self.job_data, id)
        if check_id:
            return check_id

        id = str(id)
        create_data = request.json
        result = check.data(create_data, self.job_data)

        if result:
            return result

        self.job_data[id] = create_data
        self.json_excutor.save_data()
        return self.job_data[id]

    def delete(self, id):
        check_id = check.id(self.job_data, id)
        if check_id:
            return check_id
        self.job_data.pop(str(id))
        return self.json_excutor.save_data()


@api.route("/api/jobs/<int:id>/run")
class JobDataRun(Resource):
    def __init__(self, nothing):
        with open("job_change.json", "r") as f:
            self.job_data = json.load(f)

    def _get_order(self, id):
        finder = FindOrder(self.job_data[str(id)]["task_list"])
        return finder()

    def get(self, id):
        check_id = check.id(self.job_data, id)
        if check_id:
            return check_id

        task_excutor = TaskExcutor(self.job_data[str(id)])
        if task_excutor.exist:
            return task_excutor.exist

        for task in self._get_order(id):
            getattr(task_excutor, task)()
        return "FINISH_WORK"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
