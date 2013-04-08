# -*- coding: utf-8 -*-


u"""
Convert Shapefile to OSM data XML file, using ogr2osm script.
"""


import json
import subprocess
import os
import urllib
import urllib2

N_ = lambda msg: msg

display_name = N_(u'Convert shapefile to OSM data')


def register_handler(handler_conf):
    subscribe_url_data = {
        'event_name': 'shapefile:ready',
        'function_name': 'shapefile_to_osm_data',
        'script_name': handler_conf['handler_file'],
        }
    urllib2.urlopen(handler_conf['webrokeit.urls.subscribe'], urllib.urlencode(subscribe_url_data))
    return None


def shapefile_to_osm_data(handler_conf, event_name, event_parameters):
    assert os.path.isfile(handler_conf['ogr2osm_script_file'])
    assert os.path.isfile(event_parameters['file_path'])
    project_dir_path = os.path.join(handler_conf['projects_base_dir'], event_parameters['project_id'])
    osm_data_output_file_path = os.path.join(project_dir_path, 'data.osm')
    process = subprocess.Popen(
        [
            'python',
            handler_conf['ogr2osm_script_file'],
            event_parameters['file_path'],
            '--output', osm_data_output_file_path,
            ],
        )
    process.wait()
    emit_url_data = {
        'event_name': 'osm_data:ready',
        'event_parameters': json.dumps({
            'file_path': osm_data_output_file_path,
            'project_id': event_parameters['project_id'],
            }),
        }
    urllib2.urlopen(handler_conf['webrokeit.urls.emit'], urllib.urlencode(emit_url_data))
    return None
