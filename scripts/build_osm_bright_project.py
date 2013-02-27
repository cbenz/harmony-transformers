#!/usr/bin/env python
# -*- coding: utf-8 -*-


import argparse
import json
import os
import shutil
import sys
import urllib2


u"""
Build an OSM bright project.
"""


def build_osm_bright_project(project_id, template_project_dir_name, projects_base_dir_name, data_dir_name,
        user, password):
    project_dir_name = os.path.join(projects_base_dir_name, project_id)
    shutil.copytree(template_project_dir_name, project_dir_name)
    os.unlink(os.path.join(project_dir_name, 'osm-bright.imposm.mml'))
    os.unlink(os.path.join(project_dir_name, 'osm-bright.osm2pgsql.mml'))
    with open(os.path.join(template_project_dir_name, 'osm-bright.imposm.mml')) as template_file:
        template = json.loads(template_file.read())
    for layer in template["Layer"]:
        if layer["id"] == "shoreline_300":
            layer["Datasource"]["file"] = os.path.join(data_dir_name, 'shoreline_300.zip')
        elif layer["id"] in ("processed_p", "processed_p_outline"):
            layer["Datasource"]["file"] = os.path.join(data_dir_name, 'coastline-good.zip')
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
    with open(os.path.join(project_dir_name, 'project.mml'), 'w') as output_file:
        output_file.write(json.dumps(template, sort_keys=True, indent=2))
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project_id')
    parser.add_argument('template_project_dir_name')
    parser.add_argument('projects_base_dir_name')
    parser.add_argument('data_dir_name')
    parser.add_argument('user')
    parser.add_argument('password')
    parser.add_argument('--callback-url')
    args = parser.parse_args()

    result = build_osm_bright_project(
        args.project_id, args.template_project_dir_name, args.projects_base_dir_name, args.data_dir_name,
        args.user, args.password,
        )

    if args.callback_url:
        urllib2.urlopen(args.callback_url)
    return result


if __name__ == '__main__':
    sys.exit(main())
