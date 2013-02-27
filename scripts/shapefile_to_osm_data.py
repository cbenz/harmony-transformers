#! /usr/bin/python
# -*- coding: utf-8 -*-


"""
Simple script wrapper updating lock file and calling callback URL.
"""


import argparse
import logging
import subprocess
import sys
import urllib2
import os


log = logging.getLogger('harmonyconverters.wrapper')


def main():
    parser = argparse.ArgumentParser(description = __doc__)
    parser.add_argument('project_id', help = "Project ID sequence")
    parser.add_argument('--callback-url', help = "Callback URL")
    parser.add_argument('cache_dirname', help = "Path to cache directory")
    parser.add_argument('ogr2osm_script', help = "Path to shapefile file")
    parser.add_argument('shapefile', help = "Path to shapefile file")
    parser.add_argument('-v', '--verbose', action = 'store_true', help = 'increase output verbosity')

    args = parser.parse_args()
    logging.basicConfig(level = logging.DEBUG if args.verbose else logging.WARNING, stream = sys.stdout)

    output_file = open(os.path.join(args.cache_dirname, 'stdout', args.project_id), 'w')
    error_file = open(os.path.join(args.cache_dirname, 'stderr', args.project_id), 'w')

    job_process = subprocess.Popen(
        ['python', args.ogr2osm_script, args.shapefile],
        stdin = subprocess.PIPE,
        stdout = output_file,
        stderr = error_file,
        )

    output_file.close()
    error_file.close()

    lock_file_path = os.path.join(args.cache_dirname, 'locks', args.project_id)
    with open(lock_file_path, 'w') as lock_file:
        lock_file.write(str(job_process.pid))

    job_process.wait()

    status_file_path = os.path.join(args.cache_dirname, 'statuses', args.project_id)
    with open(status_file_path, 'w') as status_file:
        status_file.write(str(job_process.returncode))

    try:
        response = urllib2.urlopen(args.callback_url)
    except urllib2.HTTPError, response:
        log.error('Erreur {0} : Request: {1}'.format(
            response.code,
            args.callback_url,
            ))
        raise
    log.info('Callback URL returned {0} code'.format(response.code))

    if os.path.isfile(lock_file_path):
        os.unlink(lock_file_path)
        log.info('Lock file {0} removed'.format(lock_file_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
