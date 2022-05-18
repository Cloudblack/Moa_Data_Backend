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
            title='Moa-Data-API',
            description='Moa-Data 과제 swagger',
            terms_of_service="https://github.com/wanted-pre-onboarding-2nd-BE-Team-D/004_Moa_Data",
            doc="/api-docs")

    
api.add_namespace(Job, '/jobs')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)