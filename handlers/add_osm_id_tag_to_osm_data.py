#!/usr/bin/env python
# -*- coding: utf-8 -*-


u"""
Add an osm_id tag to each element.
"""


import json
import os
import urllib
import urllib2

from lxml import etree
from lxml.cssselect import CSSSelector

N_ = lambda msg: msg

display_name = N_(u'Post-process OSM data')


def add_osm_id_tag_to_osm_data(handler_conf, event_name, event_parameters):
    input_osm_data_element_tree = etree.parse(event_parameters['file_path'])
    element_selector = CSSSelector('node, relation, way')
    for element in element_selector(input_osm_data_element_tree):
        etree.SubElement(element, 'tag', k=handler_conf['gis_unique_id_tag_key'], v=element.get('id'))
    output_osm_data_file_path = u'{0}_with_osm_id_tag{1}'.format(*os.path.splitext(event_parameters['file_path']))
    with open(output_osm_data_file_path, 'w') as output_osm_data_file:
        output_osm_data_file.write(etree.tostring(input_osm_data_element_tree))
    emit_url_data = {
        'event_name': 'osm_data:osm_id_tag:ready',
        'event_parameters': json.dumps({
            'file_path': output_osm_data_file_path,
            'project_id': event_parameters['project_id'],
            }),
        }
    urllib2.urlopen(handler_conf['webrokeit.urls.emit'], urllib.urlencode(emit_url_data))
    return None


def register_handler(handler_conf):
    subscribe_url_data = {
        'event_name': 'osm_data:ready',
        'function_name': 'add_osm_id_tag_to_osm_data',
        'script_name': handler_conf['handler_file'],
        }
    urllib2.urlopen(handler_conf['webrokeit.urls.subscribe'], urllib.urlencode(subscribe_url_data))
    return None
