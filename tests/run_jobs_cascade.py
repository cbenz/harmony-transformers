#!/usr/bin/env python
# -*- coding: utf-8 -*-


u"""
Run all converters, starting with a Shapefile and ending with a tile layer.
Callback URL targets a minimalist HTTP server.
"""


import argparse
import ConfigParser
import os
import shutil
import sys

from webob.dec import wsgify
from wsgiref.simple_server import make_server

from harmony_converters import jobs


# Loaded from INI file in main function.
config = None

job_name_order_list = [
    'shapefile_to_osm_data',
    'create_database',
    'add_osm_id_tag_to_osm_data',
    'create_imposm_mapping',
    'import_osm_data',
    'create_carto_project',
    ]

job_argument_config_keys_by_job_name = {
    'add_osm_id_tag_to_osm_data': [
        'osm_data_file_path',
        'osm_data_with_gis_unique_id_tag_file_path',
        ],
    'create_carto_project': [
        'carto_project_dir_name',
        'carto_script_file_path',
        'db_user',
        'db_password',
        ],
    'create_database': [
        'db_user',
        ],
    'create_imposm_mapping': [
        'osm_data_with_gis_unique_id_tag_file_path',
        'imposm_mapping_file_path',
        ],
    'import_osm_data': [
        'osm_data_with_gis_unique_id_tag_file_path',
        'imposm_cache_dir_name',
        'imposm_mapping_file_path',
        'db_user',
        'db_password',
        ],
    'shapefile_to_osm_data': [
        'ogr2osm_script_file_path',
        'shapefile_file_path',
        'osm_data_file_path',
        ]
    }


def create_project_structure():
    global config
    if os.path.isdir(config['project_dir_name']):
        shutil.rmtree(config['project_dir_name'])
    os.mkdir(config['project_dir_name'])
    os.mkdir(config['carto_project_dir_name'])
    os.mkdir(config['imposm_cache_dir_name'])
    os.mkdir(config['process_infos_dir_name'])


@wsgify
def job_completed(req):
    caller_job_name = req.params.get('caller_job_name')
    print u'caller_job_name = ', caller_job_name
    if caller_job_name is None:
        next_job_name = job_name_order_list[0]
    else:
        next_job_index = job_name_order_list.index(caller_job_name) + 1
        if next_job_index < len(job_name_order_list):
            next_job_name = job_name_order_list[next_job_index]
        else:
            next_job_name = None
            print u'End of jobs cascade reached.'
    if next_job_name is not None:
        print u'next_job_name = ', next_job_name
        job_default_params = [
            next_job_name,
            config['project_id'],
            'http://localhost:6666/?caller_job_name={0}'.format(next_job_name),
            config['process_infos_dir_name'],
            ]
        job_specific_params = [
            config[job_argument]
            for job_argument in job_argument_config_keys_by_job_name[next_job_name]
            ]
        job_params = job_default_params + job_specific_params
        print u'job_params', job_params
        jobs.start(*job_params)
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('config_ini')
    args = parser.parse_args()
    config_parser = ConfigParser.SafeConfigParser()
    config_parser.read(args.config_ini)
    global config
    config = dict(config_parser.items('harmony_project'))
    create_project_structure()
    httpd = make_server('', 6666, job_completed)
    print u'Open URL http://localhost:6666/ to start the jobs cascade.'
    httpd.serve_forever()
    return 0


if __name__ == '__main__':
    sys.exit(main())
