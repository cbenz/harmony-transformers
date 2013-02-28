#!/usr/bin/env python
# -*- coding: utf-8 -*-


u"""
Create a new database for an Harmony project.
"""


import argparse
import os
import subprocess
import sys
import urllib2


job_name = os.path.splitext(os.path.basename(__file__))[0]


def generate_createdb_script(project_id, user):
    db_create_template = u"""
set -xe
createdb -E UTF8 -O {user} -U {user} -h localhost {database}
psql -U {user} -h localhost -d {database} -f {postgis_sql} > /dev/null
psql -U {user} -h localhost -d {database} -f {spatial_ref_sys_sql} > /dev/null
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

    assert os.path.isdir(args.process_infos_dir_name)

    process = subprocess.Popen(['bash'], stdin=subprocess.PIPE)
    createdb_script = generate_createdb_script(
        project_id=args.project_id,
        user=args.db_user,
        )
    process.communicate(input=createdb_script)

    if args.callback_url is not None:
        return_code_file_path = os.path.join(args.process_infos_dir_name, u'{0}.returncode'.format(job_name))
        with open(return_code_file_path, 'w') as return_code_file:
            return_code_file.write(str(process.returncode))
        lock_file_path = os.path.join(args.process_infos_dir_name, u'{0}.lock'.format(job_name))
        os.unlink(lock_file_path)
        urllib2.urlopen(args.callback_url)

    return 0


if __name__ == '__main__':
    sys.exit(main())
