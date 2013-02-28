#!/usr/bin/env python
# -*- coding: utf-8 -*-


u"""
Import OSM data file into PostGIS database.
"""


import argparse
import os
import sys
import urllib2

import imposm.app


job_name = os.path.splitext(os.path.basename(__file__))[0]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project_id')
    parser.add_argument('process_infos_dir_name')
    parser.add_argument('osm_data_input_file_path')
    parser.add_argument('imposm_cache_dir_name')
    parser.add_argument('imposm_mapping_input_file_path')
    parser.add_argument('db_user'),
    parser.add_argument('db_password'),
    parser.add_argument('--callback-url')
    args = parser.parse_args()

    assert os.path.isdir(args.process_infos_dir_name)
    assert os.path.isfile(args.osm_data_input_file_path)
    assert os.path.isdir(args.imposm_cache_dir_name)
    assert os.path.isfile(args.imposm_mapping_input_file_path)

    result = imposm.app.main([
        '--cache-dir={0}'.format(args.imposm_cache_dir_name),
        '--connection=postgis://{args.db_user}:{args.db_password}@localhost:5432/{args.project_id}'.format(args=args),
        '--deploy-production-tables',
        '--mapping-file={0}'.format(args.imposm_mapping_input_file_path),
        '--optimize',
        '--overwrite-cache',
        '--read',
        '--remove-backup-tables',
        '--write',
        args.osm_data_input_file_path,
        ])

    if args.callback_url is not None:
        return_code_file_path = os.path.join(args.process_infos_dir_name, u'{0}.returncode'.format(job_name))
        with open(return_code_file_path, 'w') as return_code_file:
            return_code_file.write(str(result or 0))
        lock_file_path = os.path.join(args.process_infos_dir_name, u'{0}.lock'.format(job_name))
        os.unlink(lock_file_path)
        urllib2.urlopen(args.callback_url)

    return 0


if __name__ == '__main__':
    sys.exit(main())
