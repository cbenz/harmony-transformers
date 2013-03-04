# -*- coding: utf-8 -*-


import os
import signal
import subprocess


scripts_base_dir_name = os.path.join(os.path.dirname(__file__), '..', 'scripts')


def get_status(job_name, process_infos_dir_name):
    lock_file_path = os.path.join(process_infos_dir_name, u'{0}.lock'.format(job_name))
    if os.path.isfile(lock_file_path):
        return 'RUNNING'
    else:
        return_code_file_path = os.path.join(process_infos_dir_name, u'{0}.returncode'.format(job_name))
        if not os.path.isfile(return_code_file_path):
            return 'NOT_FOUND'
        with open(return_code_file_path, 'r') as return_code_file:
            return_code = int(return_code_file.read().strip())
        return 'COMPLETED' if return_code == 0 else 'ERROR'


def kill(job_name, process_infos_dir_name):
    lock_file_path = os.path.join(process_infos_dir_name, u'{0}.lock'.format(job_name))
    if not os.path.isfile(lock_file_path):
        return None
    with open(lock_file_path, 'r') as lock_file:
        pid = int(lock_file.read().strip())
    os.kill(pid, signal.SIGTERM)
    # Check if the process that we killed is alive.
    try:
        os.kill(pid, 0)
        return False
    except OSError:
        os.unlink(lock_file_path)
        return True
    return None


def start(job_name, project_id, callback_url, process_infos_dir_name, *args):
    job_script_file_path = os.path.join(scripts_base_dir_name, '{0}.py'.format(job_name))
    arguments = [
        'python',
        job_script_file_path,
        '--callback-url', callback_url,
        project_id,
        process_infos_dir_name
        ]
    arguments.extend(args)
    stderr_file_path = os.path.join(process_infos_dir_name, u'{0}.stderr'.format(job_name))
    stdout_file_path = os.path.join(process_infos_dir_name, u'{0}.stdout'.format(job_name))
    with open(stderr_file_path, 'w') as stderr_file, open(stdout_file_path, 'w') as stdout_file:
        job_process = subprocess.Popen(arguments, stderr=stderr_file, stdout=stdout_file)
    lock_file_path = os.path.join(process_infos_dir_name, u'{0}.lock'.format(job_name))
    with open(lock_file_path, 'w') as lock_file:
        lock_file.write(unicode(job_process.pid))
    return job_process.pid
