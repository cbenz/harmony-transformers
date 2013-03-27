#!/usr/bin/env python
# -*- coding: utf-8 -*-


u"""
Create a new database for an Harmony project.
"""


import json
import subprocess
import urllib
import urllib2


display_name = _(u'Create database')


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


def create_database(handler_conf, event_name, event_parameters):
    process = subprocess.Popen(['bash'], stdin=subprocess.PIPE)
    createdb_script = generate_createdb_script(
        project_id=event_parameters['project_id'],
        user=handler_conf['projects_databases.user'],
        )
    process.communicate(input=createdb_script)
    assert process.returncode == 0
    emit_url_data = {
        'event_name': 'database:ready',
        'event_parameters': json.dumps({
            'project_id': event_parameters['project_id'],
            }),
        }
    urllib2.urlopen(handler_conf['webrokeit.urls.emit'], urllib.urlencode(emit_url_data))
    return None


def register_handler(handler_conf):
    subscribe_url_data = {
        'event_name': 'shapefile:ready',
        'function_name': 'create_database',
        'script_name': handler_conf['handler_file'],
        }
    urllib2.urlopen(handler_conf['webrokeit.urls.subscribe'], urllib.urlencode(subscribe_url_data))
    return None
