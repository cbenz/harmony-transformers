# -*- coding: utf-8 -*-


import os
import signal
import subprocess


def get_status(project_id, base_dirname):
    lock_file_path = os.path.join(base_dirname, 'cache', 'locks', project_id)
    if os.path.isfile(lock_file_path):
        return 'RUNNING'
    else:
        status_file_path = os.path.join(base_dirname, 'cache', 'statuses', project_id)
        if not os.path.isfile(status_file_path):
            return 'Job not found'
        status_file = open(status_file_path, 'r')
        status = int(status_file.read().strip())
        status_file.close()
        if status == 0:
            return 'COMPLETED'
        return 'STOPPED'


def kill(project_id, base_dirname):
    lock_file_path = os.path.join(base_dirname, 'cache', 'locks', project_id)
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


def start(job_name, project_id, callback_url, base_dirname, *args):
    job_script_filepath = os.path.join(base_dirname, 'scripts', '{0}.py'.format(job_name))
    lock_file_path = os.path.join(base_dirname, 'cache', 'locks', project_id)
    arguments = [
        'python',
        job_script_filepath,
        '--callback-url', callback_url,
        project_id,
        base_dirname
        ]
    arguments.extend(args)
    job_process = subprocess.Popen(arguments)
    with open(lock_file_path, 'w') as lock_file:
        lock_file.write(unicode(job_process.pid))
    return job_process.pid
