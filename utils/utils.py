from collections import deque

import os.path
import pandas as pd

import json


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
    앞서 구한 순서를 바탕으로 task들을 실행 한다
    이미 실행한 태스크로 결과값이 나와있다면 결과값을 제공
    (현재는 중복되어있다는 말만 뜸)
    """

    def __init__(self, job_data):
        self.job_data = job_data
        self.in_path = f'./csv_data/{self.job_data["property"]["read"]["filename"]}'
        self.out_path = f'./csv_data/{self.job_data["property"]["write"]["filename"]}'
        self.exist = None
        if os.path.isfile(self.out_path):
            self.exist = "RESULT_ALREADY_EXIST"

    def read(self):
        self.df = pd.read_csv(self.in_path)

    def drop(self):
        self.df = self.df.drop("date", axis=1)

    def write(self):
        self.df.to_csv(self.out_path)


class JsonExcutor:
    """
    json file을 불러온다
    값을 입력(미구현)하지않으면 미리등록한 path로 불러온다
    """

    def __init__(self, json_file="job_change.json"):
        with open(json_file, "r") as f:
            self.job_data = json.load(f)

    def get_data(self):
        return self.job_data

    def save_data(self):
        with open("job_change.json", "w", encoding="utf-8") as f:
            json.dump(self.job_data, f, indent="\t")
        return "Success Delete"


class CheckData:
    def data(self, create_data, job_data):
        if create_data in list(job_data.values()):
            return {"MESSAGE": "DUPLICATE_VALUE"}
        data_key = job_data[list(job_data.keys())[0]]
        if create_data.keys() != data_key.keys():
            return {"MESSAGE": "MISSING_VALUE"}
        # property의 key가 제대로있는지 확인하는 코드인데 고정값이 아니기때문에 제거
        # if create_data["property"].keys() != data_key["property"].keys():
        #     return {"MESSAGE": "MISSING_VALUE"}

    def id(self, job_data, id):
        try:
            job_data[str(id)]
        except:
            return "NOT_EXIST"
