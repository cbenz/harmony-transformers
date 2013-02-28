#!/usr/bin/env python
# -*- coding: utf-8 -*-


u"""
Create imposm mapping file specifically for the OSM data file of each project.
"""

import argparse
import os
import sys
import urllib2

from lxml import etree
from lxml.cssselect import CSSSelector

import harmony_converters


job_name = os.path.splitext(os.path.basename(__file__))[0]


def extract_osm_data_tags(osm_data_input_file_path):
    osm_data_element_tree = etree.parse(osm_data_input_file_path)
    tags_selector = CSSSelector('tag')
    return set(tag_element.get('k') for tag_element in tags_selector(osm_data_element_tree))


def create_imposm_mapping_file(imposm_mapping_output_file_path, osm_data_tags):
    template_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'imposm_mapping_template.py')
    with open(template_file_path, 'r') as template_file:
        template = template_file.read()
    with open(imposm_mapping_output_file_path, 'w') as imposm_mapping_file:
        imposm_mapping_file.write(
            template.format(
                fields=u'\n'.join(u'(\'{0}\', String()),'.format(key) for key in osm_data_tags),
                unique_id_tag_key=harmony_converters.gis_unique_id_tag_key,
                )
            )
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project_id')
    parser.add_argument('process_infos_dir_name')
    parser.add_argument('osm_data_input_file_path')
    parser.add_argument('imposm_mapping_output_file_path')
    parser.add_argument('--callback-url')
    args = parser.parse_args()

    assert os.path.isdir(args.process_infos_dir_name)
    assert os.path.isfile(args.osm_data_input_file_path)

    osm_data_tags = extract_osm_data_tags(args.osm_data_input_file_path)
    result = create_imposm_mapping_file(args.imposm_mapping_output_file_path, osm_data_tags)

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
