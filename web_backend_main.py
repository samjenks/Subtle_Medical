from flask import Flask, abort
app = Flask(__name__)
from .inference_pipeline import InferencePipeline as ip

file_directory = None
acceptable_jobs = ['3dblur']
current_jobs = {}

@app.route('/job', methods = ['POST'])
def job(job_name, in_dir):
    pipe = ip()
    file_directory = in_dir
    if job_name in acceptable_jobs:
        pipe.register()

    else:
        abort(406)


@app.route('/query/{job_uid}', methods = ['GET'])
def query():
    print()


if __name__ == '__main__':
    print()
