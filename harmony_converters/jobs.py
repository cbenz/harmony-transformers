# -*- coding: utf-8 -*-


import os
import subprocess


scripts_base_dirname = os.path.join(os.dirname(__file__), '..', 'scripts')


def start_build_osm_bright_project(project_id, template_project_dirname, projects_base_dirname, data_dirname,
        user, password, callback_url):
    job_script_filepath = os.path.join(scripts_base_dirname, 'build_osm_bright_project.py')
    subprocess.Popen([
        'python', job_script_filepath, project_id, template_project_dirname, projects_base_dirname, data_dirname,
        user, password, '--callback-url', callback_url,
        ])


def start_create_database(project_id, user, password, callback_url):
    job_script_filepath = os.path.join(scripts_base_dirname, 'create_database.py')
    subprocess.Popen(['python', job_script_filepath, project_id, user, '--callback-url', callback_url])


def start_import_osm_data(project_id, osm_data_filepath, cache_dir, connection_url, mapping_filepath, callback_url):
    job_script_filepath = os.path.join(scripts_base_dirname, 'import_osm_data.py')
    subprocess.Popen([
        'python', job_script_filepath, project_id, osm_data_filepath, cache_dir, connection_url, mapping_filepath,
        '--callback_url', callback_url,
        ])
