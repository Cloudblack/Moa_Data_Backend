from flask import Flask, request
from flask_restx import Resource, Api
import json

app = Flask(__name__)
api = Api(app)


def check(create_data, job_data):
    if create_data in list(job_data.values()):
        return {"MESSAGE": "DUPLICATE_VALUE"}
    data_key = job_data[list(job_data.keys())[0]]
    if create_data.keys() != data_key.keys():
        return {"MESSAGE": "MISSING_VALUE"}
    if create_data["property"].keys() != data_key["property"].keys():
        return {"MESSAGE": "MISSING_VALUE"}


@api.route("/api/data")
class DataCR(Resource):
    def __init__(self, nothing):
        with open("job_change.json", "r") as f:
            self.job_data = json.load(f)
        self.keys = list(self.job_data.keys())

    def get(self):
        return self.job_data

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
        print(create_data)
        result = check(create_data, self.job_data)
        if result:
            return result
        # 마지막 id +1 아니면 빈칸 채워야할까?
        job_id = int(self.keys.pop()) + 1

        self.job_data[job_id] = create_data

        with open("job_change.json", "w", encoding="utf-8") as f:
            json.dump(self.job_data, f, indent="\t")

        return self.job_data[job_id]


@api.route("/api/data/<int:id>")
class DataRUD(Resource):
    def __init__(self, nothing):
        with open("job_change.json", "r") as f:
            self.job_data = json.load(f)

    def get(self, id):
        return self.job_data[str(id)]

    def put(self, id):
        id = str(id)      
        create_data = request.json       
        result = check(create_data, self.job_data)
        if result:
            return result

        self.job_data[id] = create_data
        with open("job_change.json", "w", encoding="utf-8") as f:
            json.dump(self.job_data, f, indent="\t")
        return self.job_data[id]

    def delete(self, id):
        self.job_data.pop(str(id))
        with open("job_change.json", "w", encoding="utf-8") as f:
            json.dump(self.job_data, f, indent="\t")

        return "Success Delete"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
