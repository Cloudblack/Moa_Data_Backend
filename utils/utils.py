import json
from flask import request
import pandas as pd

class JobsHandler:

    def __init__(self):
        self.JSON_FILE_PATH = 'job.json'

    def _get_all_jobs(self, id=None):
        with open(self.JSON_FILE_PATH, 'r') as file:
            jobs = json.load(file)
            return jobs

    def _indexing(self, job_id, jobs):
        for idx, job in enumerate(jobs):
            if job['job_id'] == job_id:
                return idx, job

    def _control_job(self, job):
        with open(self.JSON_FILE_PATH, 'w') as file:
            json.dump(job, file, indent=4)

    def get_response(self):
        response = request.data.decode('utf-8')
        data = json.loads(response)
        return data


class TaskHandler:

    def __init__(self):
        self.task = None
        self.filename = None

    def read(self, job):
        self.task = job['property']['read']
        self.filename, sep = self.task['filename'], self.task['sep']

        self.data = pd.read_csv(f'./{self.filename}', sep=sep)
        return self.data

    def drop(self, job):
        self.task = job['property']['drop']
        column_name = self.task['column_name']

        self.data.pop(column_name)
        return self.data

    def write(self, job):
        self.task = job['property']['write']
        self.filename, sep = self.task['filename'], self.task['sep']

        self.data.to_csv(f'./{self.filename}', sep=sep, index=False)
        return 200