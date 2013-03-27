#!/usr/bin/env python
# -*- coding: utf-8 -*-


u"""
Import OSM data file into PostGIS database.
"""


import json
import os
import urllib
import urllib2

import imposm.app


display_name = _(u'Import OSM data')


def check_all_events_received(handler_conf, state_document_list):
    expected_event_name_list = ['database:ready', 'imposm_mapping:ready', 'osm_data:osm_id_tag:ready']
    received_event_name_list = [
        state_document['data']['event_name']
        for state_document in state_document_list
        if state_document['data'].get('event_name') is not None
        ]
    if set(received_event_name_list) == set(expected_event_name_list):
        event_parameters_list = {
            state_document['data']['event_name']: state_document['data']['event_parameters']
            for state_document in state_document_list
            }
        emit_url_data = {
            'event_name': 'database:ready_to_import',
            'event_parameters': json.dumps(event_parameters_list),
            }
        urllib2.urlopen(handler_conf['webrokeit.urls.emit'], urllib.urlencode(emit_url_data))
    return None


def import_osm_data(handler_conf, event_name, event_parameters):
    assert os.path.isfile(event_parameters['imposm_mapping:ready']['file_path'])
    assert os.path.isfile(event_parameters['osm_data:osm_id_tag:ready']['file_path'])
    project_id = event_parameters['database:ready']['project_id']
    project_dir_path = os.path.join(handler_conf['projects_base_dir'], project_id)
    assert os.path.isdir(project_dir_path)
    imposm_cache_dir_path = os.path.abspath(os.path.join(project_dir_path, 'imposm_cache'))
    if not os.path.isdir(imposm_cache_dir_path):
        os.mkdir(imposm_cache_dir_path)
    imposm.app.main([
        '--cache-dir={0}'.format(imposm_cache_dir_path),
        '--connection=postgis://{db_user}:{db_password}@localhost:5432/{project_id}'.format(
            db_password=handler_conf['projects_databases.password'],
            db_user=handler_conf['projects_databases.user'],
            project_id=project_id,
            ),
        '--deploy-production-tables',
        '--mapping-file={0}'.format(event_parameters['imposm_mapping:ready']['file_path']),
        '--optimize',
        '--overwrite-cache',
        '--read',
        '--remove-backup-tables',
        '--write',
        event_parameters['osm_data:osm_id_tag:ready']['file_path'],
        ])
    emit_url_data = {
        'event_name': 'database:imported',
        'event_parameters': json.dumps({
            'project_id': project_id,
            }),
        }
    urllib2.urlopen(handler_conf['webrokeit.urls.emit'], urllib.urlencode(emit_url_data))
    return None


def on_database_ready(handler_conf, event_name, event_parameters):
    state_url_data = {
        'action': 'save',
        'data': json.dumps({
            'event_name': event_name,
            'event_parameters': event_parameters,
            }),
        'key': u'{0}.{1}'.format('import_osm_data', event_parameters['project_id']),
        }
    response = urllib2.urlopen(handler_conf['webrokeit.urls.state'], urllib.urlencode(state_url_data))
    state_document_list = json.loads(response.read())
    check_all_events_received(handler_conf, state_document_list)
    return None


def on_imposm_mapping_ready(handler_conf, event_name, event_parameters):
    state_url_data = {
        'action': 'save',
        'data': json.dumps({
            'event_name': event_name,
            'event_parameters': event_parameters,
            }),
        'key': u'{0}.{1}'.format('import_osm_data', event_parameters['project_id']),
        }
    response = urllib2.urlopen(handler_conf['webrokeit.urls.state'], urllib.urlencode(state_url_data))
    state_document_list = json.loads(response.read())
    check_all_events_received(handler_conf, state_document_list)
    return None


def on_osm_data_osm_id_tag_ready(handler_conf, event_name, event_parameters):
    state_url_data = {
        'action': 'save',
        'data': json.dumps({
            'event_name': event_name,
            'event_parameters': event_parameters,
            }),
        'key': u'{0}.{1}'.format('import_osm_data', event_parameters['project_id']),
        }
    response = urllib2.urlopen(handler_conf['webrokeit.urls.state'], urllib.urlencode(state_url_data))
    state_document_list = json.loads(response.read())
    check_all_events_received(handler_conf, state_document_list)
    return None


def register_handler(handler_conf):
    subscribe_url_data_list = [
        {
            'event_name': 'database:ready',
            'function_name': 'on_database_ready',
            'script_name': handler_conf['handler_file'],
            },
        {
            'event_name': 'database:ready_to_import',
            'function_name': 'import_osm_data',
            'script_name': handler_conf['handler_file'],
            },
        {
            'event_name': 'imposm_mapping:ready',
            'function_name': 'on_imposm_mapping_ready',
            'script_name': handler_conf['handler_file'],
            },
        {
            'event_name': 'osm_data:osm_id_tag:ready',
            'function_name': 'on_osm_data_osm_id_tag_ready',
            'script_name': handler_conf['handler_file'],
            },
        ]
    for subscribe_url_data in subscribe_url_data_list:
        urllib2.urlopen(handler_conf['webrokeit.urls.subscribe'], urllib.urlencode(subscribe_url_data))
    return None
