import json


class JobTask():
    
    FATH_JOB = './json/job.json'

    def read_json(self):
        with open(self.FATH_JOB) as json_file:
            return json.load(json_file)

    def read_job(self, job_id):
        with open(self.FATH_JOB, 'r'):
            for job in self.read_json():
                if int(job['job_id']) == int(job_id):
                    return job

    def write_json(self, new_job):
        with open(self.FATH_JOB, 'w') as json_file:
            json.dump(new_job, json_file)


class IndexTask():

    FATH_INDEX = './json/index.json'

    def read_index(self, job_id=None):
        with open(self.FATH_INDEX, 'r') as json_file:
            job_index = json.load(json_file)

            if job_id:
                return job_index[str(job_id)]

            return job_index

    def _write_index(self, new_idex):
        with open(self.FATH_INDEX, 'w') as json_file:
            json.dump(new_idex, json_file)
