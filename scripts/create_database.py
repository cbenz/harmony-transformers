#!/usr/bin/env python
# -*- coding: utf-8 -*-


import argparse
import subprocess
import sys
import urllib2


u"""
Create a new database for an Harmony project.
"""


def generate_createdb_script(project_id, user):
    db_create_template = u"""
set -xe
createdb -E UTF8 -O {user} -U {user} -h localhost {database}
psql -U {user} -h localhost -d {database} -f {postgis_sql}
psql -U {user} -h localhost -d {database} -f {spatial_ref_sys_sql}
echo "ALTER TABLE geometry_columns OWNER TO {user}; ALTER TABLE spatial_ref_sys OWNER TO {user};" | \
    psql -U {user} -h localhost -d {database}
set +x
""".strip()
    return db_create_template.format(
        database=project_id,
        pg_hba='/etc/postgresql/9.1/main/pg_hba.conf',
        postgis_sql='/usr/share/postgresql/9.1/contrib/postgis-1.5/postgis.sql',
        spatial_ref_sys_sql='/usr/share/postgresql/9.1/contrib/postgis-1.5/spatial_ref_sys.sql',
        user=user,
        )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project_id')
    parser.add_argument('process_infos_dir_name')
    parser.add_argument('db_user')
    parser.add_argument('--callback-url')
    args = parser.parse_args()

    process = subprocess.Popen(['bash'], stdin=subprocess.PIPE)
    createdb_script = generate_createdb_script(
        project_id=args.project_id,
        user=args.db_user,
        )
    stdoutdata, stderrdata = process.communicate(input=createdb_script)

    if args.callback_url:
        urllib2.urlopen(args.callback_url)
    return process.returncode


if __name__ == '__main__':
    sys.exit(main())
