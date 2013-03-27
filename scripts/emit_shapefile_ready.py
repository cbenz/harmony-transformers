#!/usr/bin/env python
# -*- coding: utf-8 -*-


u"""
Emit the shapefile:ready event.
"""


import argparse
import ConfigParser
import json
import logging
import os
import sys
import urllib
import urllib2


log = logging.getLogger(os.path.basename(__file__))


def emit_shapefile_ready(handler_conf, project_id, shapefile_file_path):
    event_parameters = {
        'file_path': shapefile_file_path,
        'project_id': project_id,
        }
    emit_url_data = {
        'event_name': 'shapefile:ready',
        'event_parameters': json.dumps(event_parameters),
        }
    urllib2.urlopen(handler_conf['webrokeit.urls.emit'], urllib.urlencode(emit_url_data))
    log.debug(u'Event "shapefile:ready" emitted with parameters: {0}.'.format(event_parameters))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('handlers_ini')
    parser.add_argument('project_id')
    parser.add_argument('shapefile')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help=u'Display debug messages')
    args = parser.parse_args()
    assert os.path.isfile(args.handlers_ini)
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.WARNING)
    config_parser = ConfigParser.SafeConfigParser(defaults={
        'here': os.path.dirname(os.path.abspath(args.handlers_ini)),
        })
    config_parser.read(args.handlers_ini)
    handler_conf = dict(config_parser.items('shapefile_to_osm_data'))
    shapefile_file_path = os.path.abspath(args.shapefile)
    emit_shapefile_ready(handler_conf, args.project_id, shapefile_file_path)
    return 0


if __name__ == '__main__':
    sys.exit(main())
