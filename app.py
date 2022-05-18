import json
import re
from flask import Flask, request, jsonify
from flask_api import status
from flask_restx import Api, Resource, Namespace
import pandas as pd
from job import Job

app = Flask(__name__)
api = Api(  app,
            version='1.0',
            title='API문서',
            description='Swagger문서',
            doc="/api-docs")

    
api.add_namespace(Job, '/jobs')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)