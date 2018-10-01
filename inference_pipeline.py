import collections

# Create a namedtuple type as the entries in a job registry
JobEntry = collections.namedtuple('JobEntry',
                                  'name config preprocess postprocess func')


class InferencePipeline:
    '''Registers and executes inference jobs.

    A typical use case with the gaussian_blur3d function:

    >>> pipeline = InferencePipeline([])
    >>> job = JobEntry(name='3dblur', config={'sigma': 1.0},
    ....               preprocess=pre_gaussian_blur3d,
    ....               postprocess=post_gaussian_blur3d,
    ....               func=gaussian_blur3d)
    >>> pipeline.register(job)
    >>> pipeline.execute('3dblur', '/path/to/input/dicom/folder',
    ....                '/path/to/output/dicom/folder')
    '''

    def __init__(self, registry: list):
        '''Instantiate an InferencePipeline object with a list of jobs.

        Duplicated jobs (by name) will collide and only the last one will be
        kept. Others will be discarded without warning.

        :param registry: a list of JobEntry objects as the init job registry

        :return: a InferencePipeline object
        '''
        self.jobs = {}


    def register(self, job: JobEntry):
        '''Add a job into the registry.

        See __init__ for information of job name collision.

        :param job: A JobEntry object containing the job to be registered
        '''
        if job.name in self.jobs:
            del self.jobs[job.name]
        else:
            job_container = {}
            job_container['config'] = job.config
            job_container['preprocess'] = job.preprocess
            job_container['postprocess'] = job.postprocess
            job_container['func'] = job.func
            self.jobs[job.name] = job_container


    def unregister(self, job_name: str):
        '''Remove a job by name from the registry.

        An unfound job_name will raise a KeyError.

        :param job_name: the name of the job to be removed
        '''
        try:
            del self.jobs[job_name]
        except KeyError:
            return KeyError



    def is_job_registered(self, job_name: str) -> bool:
        '''Check if a job_name is registered with the pipeline

        :param job_name: str, the unique name of the job
        :return: bool, if the job is registered
        '''

        if job_name in self.jobs:
            return True
        else:
            return False

    def execute(self, job_name: str, in_dicom_dir: str, out_dicom_dir: str):
        '''Execute a job specified by job_name, with the in_dicom_dir
        (directory containing DICOM files) as input and out_dicom_dir as the
        output DICOM directory.

        :param job_name: a string, the job's unique name
        :param in_dicom_dir: a string, the path to the input DICOM folder
        :param out_dicom_dir: a string, the path to the output DICOM folder
        '''
        job = self.jobs[job_name]
        preprossing_out = job['preprocess'](in_dicom_dir)
        job_out = job['func'](preprossing_out, {'spacing', (3, 3, 1)}, job['config'])
        job['postprocess'](job_out, out_dicom_dir)
