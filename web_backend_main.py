from flask import Flask, abort
import collections
import random
from inference_pipeline import InferencePipeline as ip
from inference_pipeline import post_gaussian_blur3d, pre_gaussian_blur3d
from gaussian_blur3d import gaussian_blur3d

app = Flask(__name__)
JobEntry = collections.namedtuple('JobEntry', 'name config preprocess postprocess func')

file_directory = None
acceptable_jobs = ['3dblur']
current_jobs = {}

@app.route('/job', methods = ['POST'])
def job(job_name, in_dir):
    pipe = ip([])
    file_directory = in_dir
    if job_name in acceptable_jobs:
        pipe.register(JobEntry(name=job_name, config={'sigma': 1.0}, preprocess=pre_gaussian_blur3d,
                               postprocess=post_gaussian_blur3d, func=gaussian_blur3d))
        pipe.execute(job_name, in_dir, in_dir)
        job_id = random.randint(0,9999)
        current_jobs[str(job_id)] = pipe
        return job_id, 200
    else:
        abort(406)


@app.route('/query/{job_uid}', methods = ['GET'])
def query(job_uid):
    if job_uid in current_jobs:
        return 200
    else:
        abort(401)



if __name__ == '__main__':
    print()
