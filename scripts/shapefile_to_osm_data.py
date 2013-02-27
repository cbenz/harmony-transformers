#!/usr/bin/python
# -*- coding: utf-8 -*-


u"""
Simple script wrapper updating lock file and calling callback URL.
"""


import argparse
import subprocess
import sys
import urllib2
import os


def main():
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument('project_id')
    parser.add_argument('process_infos_dir_name')
    parser.add_argument('ogr2osm_script_file_path')
    parser.add_argument('shapefile_file_path')
    parser.add_argument('osm_data_output_file_path')
    parser.add_argument('--callback-url')
    args = parser.parse_args()

    stderr_file = sys.stderr
    stdout_file = sys.stdout
    if args.callback_url is not None:
        stderr_file_path = os.path.join(args.process_infos_dir_name, u'{0}.stderr'.format(args.project_id))
        stderr_file = open(stderr_file_path, 'w')
        stdout_file_path = os.path.join(args.process_infos_dir_name, u'{0}.stdout'.format(args.project_id))
        stdout_file = open(stdout_file_path, 'w')
    process = subprocess.Popen(
        ['python', args.ogr2osm_script_file_path, args.shapefile_file_path, '--output', args.osm_data_output_file_path],
        stderr = stderr_file,
        stdin = subprocess.PIPE,
        stdout = stdout_file,
        )
    process.wait()
    if args.callback_url is not None:
        stderr_file.close()
        stdout_file.close()

    if args.callback_url is not None:
        return_code_file_path = os.path.join(args.process_infos_dir_name, u'{0}.returncode'.format(args.project_id))
        with open(return_code_file_path, 'w') as return_code_file:
            return_code_file.write(str(process.returncode))
        lock_file_path = os.path.join(args.process_infos_dir_name, u'{0}.lock'.format(args.project_id))
        os.unlink(lock_file_path)
        urllib2.urlopen(args.callback_url)
    return process.returncode


if __name__ == '__main__':
    sys.exit(main())
