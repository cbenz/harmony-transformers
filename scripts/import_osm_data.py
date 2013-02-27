#!/usr/bin/env python
# -*- coding: utf-8 -*-


import argparse
import os
import sys
import urllib2

import imposm.app


u"""
Import OSM data file into PostGIS database.
"""


def generate_imposm_mapping():
    pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project_id')
    parser.add_argument('osm_data_file_path')
    parser.add_argument('imposm_cache_dir_name')
    parser.add_argument('mapping_file_path')
    parser.add_argument('db_user'),
    parser.add_argument('db_password'),
    parser.add_argument('--callback-url')
    args = parser.parse_args()

    generate_imposm_mapping()
    if not os.path.exists(args.imposm_cache_dir_name):
        os.mkdir(args.imposm_cache_dir_name)
    imposm_result = imposm.app.main([
        '--cache-dir={0}'.format(args.imposm_cache_dir_name),
        '--connection=postgis://{args.db_user}:{args.db_password}@localhost:5432/{args.project_id}'.format(args=args),
        '--deploy-production-tables',
        '--mapping-file={0}'.format(args.mapping_file_path),
        '--optimize',
        '--overwrite-cache',
        '--read',
        '--remove-backup-tables',
        '--write',
        args.osm_data_file_path,
        ])

    if args.callback_url:
        urllib2.urlopen(args.callback_url)
    return imposm_result


if __name__ == '__main__':
    sys.exit(main())
