#!/usr/bin/env python
# -*- coding: utf-8 -*-


u"""
Create imposm mapping file specifically for the OSM data file of each project.
"""

import json
import os
import urllib
import urllib2

from lxml import etree
from lxml.cssselect import CSSSelector


def extract_osm_data_tags(osm_data_input_file_path):
    osm_data_element_tree = etree.parse(osm_data_input_file_path)
    tags_selector = CSSSelector('tag')
    return set(tag_element.get('k') for tag_element in tags_selector(osm_data_element_tree))


def create_imposm_mapping(handler_conf, event_name, event_parameters):
    assert os.path.isfile(event_parameters['file_path'])
    osm_data_tags = extract_osm_data_tags(event_parameters['file_path'])
    with open(handler_conf['template_file_path'], 'r') as template_file:
        template = template_file.read()
    project_dir_path = os.path.join(handler_conf['projects_base_dir'], event_parameters['project_id'])
    imposm_mapping_output_file_path = os.path.join(project_dir_path, 'imposm_mapping.py')
    with open(imposm_mapping_output_file_path, 'w') as imposm_mapping_file:
        imposm_mapping_file.write(
            template.format(
                fields=u'\n'.join(u'(\'{0}\', String()),'.format(key) for key in osm_data_tags),
                unique_id_tag_key=handler_conf['gis_unique_id_tag_key'],
                )
            )
    emit_url_data = {
        'event_name': 'imposm_mapping:ready',
        'event_parameters': json.dumps({
            'file_path': imposm_mapping_output_file_path,
            'project_id': event_parameters['project_id'],
            }),
        }
    urllib2.urlopen(handler_conf['webrokeit.urls.emit'], urllib.urlencode(emit_url_data))
    return None


def register_handler(handler_conf):
    subscribe_url_data = {
        'event_name': 'osm_data:osm_id_tag:ready',
        'function_name': 'create_imposm_mapping',
        'script_name': handler_conf['handler_file'],
        }
    urllib2.urlopen(handler_conf['webrokeit.urls.subscribe'], urllib.urlencode(subscribe_url_data))
    return None
