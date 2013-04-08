# -*- coding: utf-8 -*-


u"""
Create project tree
"""


import json
import shutil
import os
import urllib
import urllib2
import zipfile

N_ = lambda msg: msg

display_name = N_(u'Create project tree')


# unzip archive and returns shapefile path
def unzip(path, dest_dir_path):
    shapefile = None
    zfile = zipfile.ZipFile(path)
    for name in zfile.namelist():
        (dirname, filename) = os.path.split(name)
        if filename == '':
            # dir
            pass
        else:
            # file
            file_path = os.path.join(dest_dir_path, filename)
            fd = open(file_path, 'w')
            fd.write(zfile.read(name))
            fd.close()
            if file_path.endswith('.shp'):
                shapefile = file_path
    zfile.close()
    return shapefile


def register_handler(handler_conf):
    subscribe_url_data = {
        'event_name': 'shapefile:archive:ready',
        'function_name': 'create_project_tree',
        'script_name': handler_conf['handler_file'],
        }
    urllib2.urlopen(handler_conf['webrokeit.urls.subscribe'], urllib.urlencode(subscribe_url_data))
    return None


def create_project_tree(handler_conf, event_name, event_parameters):
    assert os.path.isdir(handler_conf['projects_base_dir'])
    assert os.path.isfile(event_parameters['file_path'])

    # create project dir
    project_dir_path = os.path.join(handler_conf['projects_base_dir'], event_parameters['project_id'])
    os.mkdir(project_dir_path)

    # create source folder: contains ZIP archive + decompress archives files 
    src_dir_path = os.path.join(project_dir_path, 'src')
    os.mkdir(src_dir_path)

    # cp archive file in src
    shutil.copy(event_parameters['file_path'], src_dir_path)

    # create src/files folder
    src_files_dir_path = os.path.join(src_dir_path, 'files')
    os.mkdir(src_files_dir_path)

    # decompress archive
    archive_path = os.path.join(src_dir_path, event_parameters['file_path'])
    shapefile_path = unzip(archive_path, src_files_dir_path)

    emit_url_data = {
        'event_name': 'shapefile:ready',
        'event_parameters': json.dumps({
            'file_path': shapefile_path,
            'project_id': event_parameters['project_id'],
            }),
        }
    urllib2.urlopen(handler_conf['webrokeit.urls.emit'], urllib.urlencode(emit_url_data))

    return None
