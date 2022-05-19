import json


class JobTask():

    FATH_JOB = './json/job.json'

    def read_json(self):
        with open(self.FATH_JOB) as json_file:
            return json.load(json_file)

    def read_job(self, job_id):
        with open(self.FATH_JOB, 'r') as json_file:
            return json_file[str(job_id)]

    def write_json(self, new_job):
        with open(self.FATH_JOB, 'w') as json_file:
            json.dump(new_job, json_file)
