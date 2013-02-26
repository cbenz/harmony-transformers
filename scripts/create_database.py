#!/usr/bin/env python
# -*- coding: utf-8 -*-


import argparse
import string
import subprocess
import sys
import urllib2


def generate_createdb_script(project_id, user):
    db_create_template = u"""
set -xe
createdb -E UTF8 -O ${user} -U ${user} -h localhost ${database}
psql -U ${user} -h localhost -d ${database} -f ${postgis_sql}
psql -U ${user} -h localhost -d ${database} -f ${spatial_ref_sys_sql}
echo "ALTER TABLE geometry_columns OWNER TO ${user}; ALTER TABLE spatial_ref_sys OWNER TO ${user};" | \
    psql -U ${user} -h localhost -d ${database}
set +x
""".strip()
    template = string.Template(db_create_template)
    mapping = {
        'database': project_id,
        'pg_hba': '/etc/postgresql/9.1/main/pg_hba.conf',
        'postgis_sql': '/usr/share/postgresql/9.1/contrib/postgis-1.5/postgis.sql',
        'spatial_ref_sys_sql': '/usr/share/postgresql/9.1/contrib/postgis-1.5/spatial_ref_sys.sql',
        'user': user,
        }
    return template.substitute(mapping)


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    parser = argparse.ArgumentParser(description=u'Create a new database for an Harmony project.')
    parser.add_argument('project_id')
    parser.add_argument('user')
    parser.add_argument('--callback-url')
    arguments = parser.parse_args(args)
    bash_process = subprocess.Popen(['bash'], stdin=subprocess.PIPE)
    createdb_script = generate_createdb_script(
        project_id=arguments.project_id,
        user=arguments.user,
        )
    stdoutdata, stderrdata = bash_process.communicate(input=createdb_script)
    print stdoutdata, stderrdata
    if arguments.callback_url:
        urllib2.urlopen(arguments.callback_url)


if __name__ == '__main__':
    sys.exit(main())
