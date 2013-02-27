# -*- coding: utf-8 -*-


import os
import signal
import subprocess


scripts_base_dirname = os.path.join(os.path.dirname(__file__), '..', 'scripts')


def get_status(project_id, cache_dirname):
    lock_file_path = os.path.join(cache_dirname, 'locks', project_id)
    if os.path.isfile(lock_file_path):
        return 'RUNNING'
    else:
        status_file_path = os.path.join(cache_dirname, 'statuses', project_id)
        if not os.path.isfile(status_file_path):
            return 'Job not found'
        status_file = open(status_file_path, 'r')
        status = int(status_file.read().strip())
        status_file.close()
        if status == 0:
            return 'COMPLETED'
        return 'STOPPED'


def kill(project_id, cache_dirname):
    lock_file_path = os.path.join(cache_dirname, 'locks', project_id)
    if not os.path.isfile(lock_file_path):
        return 'Job not found'
    with open(lock_file_path, 'r') as lock_file:
        pid = int(lock_file.read().strip())
    os.kill(pid, signal.SIGTERM)
    # Check if the process that we killed is alive.
    try:
        os.kill(int(pid), 0)
        raise Exception("wasn't able to kill the process {0} HINT:use signal.SIGKILL or signal.SIGABORT".format(pid))
    except OSError as ex:
        return 0
    return 1


def start(job_name, project_id, callback_url, cache_dirname, *args):
    job_script_filepath = os.path.join(scripts_base_dirname, '{0}.py'.format(job_name))
    lock_file_path = os.path.join(cache_dirname, 'locks', project_id)
    arguments = [
        'python',
        job_script_filepath,
        '--callback-url', callback_url,
        project_id,
        cache_dirname
        ]
    arguments.extend(args)
    job_process = subprocess.Popen(arguments)
    with open(lock_file_path, 'w') as lock_file:
        lock_file.write(unicode(job_process.pid))
    return job_process.pid
