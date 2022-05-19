from flask import Flask
from flask_restx import Api

from job import Job

app = Flask(__name__)
api = Api(app,
          version='1.0',
          title='Moa_Data API',
          description='모아데이타 과제 API구현',
          contact='rsh1994@naver.com',
          doc="/api-docs",
          )


api.add_namespace(Job, '/jobs')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
