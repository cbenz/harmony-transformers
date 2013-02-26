#!/usr/bin/env python
# -*- coding: utf-8 -*-


import argparse
import os
import sys
import urllib2

import imposm.app


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    parser = argparse.ArgumentParser(description=u'Import OSM data file into PostGIS database.')
    parser.add_argument('project_id')
    parser.add_argument('osm_data_filepath')
    parser.add_argument('cache_base_dirname')
    parser.add_argument('mapping_filepath')
    parser.add_argument('user'),
    parser.add_argument('password'),
    parser.add_argument('--callback-url')
    arguments = parser.parse_args(args)
    cache_dir = os.path.join(arguments.cache_base_dirname, arguments.project_id)
    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir)
    imposm.app.main([
        '--cache-dir={0}'.format(cache_dir),
        '--connection=postgis://{arguments.user}:{arguments.password}@localhost:5432/{arguments.project_id}'.format(
            arguments=arguments,
            ),
        '--deploy-production-tables',
        '--mapping-file={0}'.format(arguments.mapping_filepath),
        '--optimize',
        '--overwrite-cache',
        '--read',
        '--remove-backup-tables',
        '--write',
        arguments.osm_data_filepath,
        ])
    if arguments.callback_url:
        urllib2.urlopen(arguments.callback_url)


if __name__ == '__main__':
    sys.exit(main())
