#!/usr/bin/env python
# -*- coding: utf-8 -*-


u"""
Build a carto project to generate tiles with.
"""


import json
import os
import shutil
import subprocess
import urllib
import urllib2

N_ = lambda msg: msg

display_name = N_(u'Create tile layer')


def create_carto_project(handler_conf, event_name, event_parameters):
    project_dir_path = os.path.join(handler_conf['projects_base_dir'], event_parameters['project_id'])
    assert os.path.isdir(project_dir_path)
    assert os.path.isfile(handler_conf['carto_script_file'])
    assert os.path.isdir(handler_conf['carto_project_template_dir'])
    carto_project_dir_path = os.path.abspath(os.path.join(project_dir_path, 'carto_project'))
    os.mkdir(carto_project_dir_path)
    style_file_path = os.path.join(handler_conf['carto_project_template_dir'], 'style.mss')
    shutil.copyfile(style_file_path, os.path.join(carto_project_dir_path, 'style.mss'))
    project_template_file_path = os.path.join(handler_conf['carto_project_template_dir'], 'project.mml')
    with open(project_template_file_path, 'r') as project_template_file:
        project_template = project_template_file.read()
    project_mml_file_path = os.path.join(carto_project_dir_path, 'project.mml')
    with open(project_mml_file_path, 'w') as project_mml_file:
        project_mml_file.write(project_template.format(
            db_password=handler_conf['projects_databases.password'],
            db_user=handler_conf['projects_databases.user'],
            project_id=event_parameters['project_id'],
            ))
    project_xml_file_path = os.path.join(carto_project_dir_path, 'project.xml')
    with open(project_xml_file_path, 'w') as project_xml_file:
        process = subprocess.Popen(
            [handler_conf['carto_script_file'], project_mml_file_path],
            stdout=project_xml_file,
            )
        process.wait()
    assert process.returncode == 0
    emit_url_data = {
        'event_name': 'carto_project:ready',
        'event_parameters': json.dumps({
            'dir_path': carto_project_dir_path,
            'project_id': event_parameters['project_id'],
            }),
        }
    urllib2.urlopen(handler_conf['webrokeit.urls.emit'], urllib.urlencode(emit_url_data))
    return None


def register_handler(handler_conf):
    subscribe_url_data = {
        'event_name': 'shapefile:ready',
        'function_name': 'create_carto_project',
        'script_name': handler_conf['handler_file'],
        }
    urllib2.urlopen(handler_conf['webrokeit.urls.subscribe'], urllib.urlencode(subscribe_url_data))
    return None
