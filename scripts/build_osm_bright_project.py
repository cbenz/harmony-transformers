#!/usr/bin/env python
# -*- coding: utf-8 -*-


import argparse
import json
import os
import shutil
import sys
import urllib2


def build_osm_bright_project(project_id, template_project_dirname, projects_base_dirname, data_dirname, user, password):
    project_dirname = os.path.join(projects_base_dirname, project_id)
    shutil.copytree(template_project_dirname, project_dirname)
    os.unlink(os.path.join(project_dirname, 'osm-bright.imposm.mml'))
    os.unlink(os.path.join(project_dirname, 'osm-bright.osm2pgsql.mml'))
    with open(os.path.join(template_project_dirname, 'osm-bright.imposm.mml')) as template_file:
        template = json.loads(template_file.read())
    for layer in template["Layer"]:
        if layer["id"] == "shoreline_300":
            layer["Datasource"]["file"] = os.path.join(data_dirname, 'shoreline_300.zip')
        elif layer["id"] in ("processed_p", "processed_p_outline"):
            layer["Datasource"]["file"] = os.path.join(data_dirname, 'coastline-good.zip')
        else:
            layer['Datasource'].update({
                'dbname': project_id,
                # World extent.
                'extent': '-20037508.34 -20037508.34 20037508.34 20037508.34',
                'host': 'localhost',
                'port': '5432',
                'user': user,
                'password': password,
                })
    template['name'] = project_id
    with open(os.path.join(project_dirname, 'project.mml'), 'w') as output_file:
        output_file.write(json.dumps(template, sort_keys=True, indent=2))
    return None


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    parser = argparse.ArgumentParser(description=u'Build an OSM bright project.')
    parser.add_argument('project_id')
    parser.add_argument('template_project_dirname')
    parser.add_argument('projects_base_dirname')
    parser.add_argument('data_dirname')
    parser.add_argument('user')
    parser.add_argument('password')
    parser.add_argument('--callback-url')
    arguments = parser.parse_args(args)
    build_osm_bright_project(
        arguments.project_id, arguments.template_project_dirname, arguments.projects_base_dirname,
        arguments.data_dirname, arguments.user, arguments.password,
        )
    if arguments.callback_url:
        urllib2.urlopen(arguments.callback_url)


if __name__ == '__main__':
    sys.exit(main())
