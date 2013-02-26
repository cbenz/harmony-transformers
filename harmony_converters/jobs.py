# -*- coding: utf-8 -*-


import os
import subprocess


scripts_base_dirname = os.path.join(os.dirname(__file__), '..', 'scripts')


def start(job_name, project_id, callback_url, *args):
    job_script_filepath = os.path.join(scripts_base_dirname, '{0}.py'.format(job_name))
    return subprocess.Popen(['python', job_script_filepath, '--callback-url', callback_url, project_id, *args])
