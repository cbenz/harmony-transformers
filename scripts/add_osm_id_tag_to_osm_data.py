#!/usr/bin/env python
# -*- coding: utf-8 -*-


u"""
Add an artificial osm_id tag to each element.
"""


import argparse
import os
import sys
import urllib2

from lxml import etree
from lxml.cssselect import CSSSelector

import harmony_converters


job_name = os.path.splitext(os.path.basename(__file__))[0]


def add_osm_id_tag_to_osm_data(osm_data_input_file_path, osm_data_output_file_path):
    input_osm_data_element_tree = etree.parse(osm_data_input_file_path)
    element_selector = CSSSelector('node, relation, way')
    for element in element_selector(input_osm_data_element_tree):
        etree.SubElement(element, 'tag', k=harmony_converters.gis_unique_id_tag_key, v=element.get('id'))
    with open(osm_data_output_file_path, 'w') as output_osm_data_file:
        output_osm_data_file.write(etree.tostring(input_osm_data_element_tree))
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project_id')
    parser.add_argument('process_infos_dir_name')
    parser.add_argument('osm_data_input_file_path')
    parser.add_argument('osm_data_output_file_path')
    parser.add_argument('--callback-url')
    args = parser.parse_args()

    assert os.path.isdir(args.process_infos_dir_name)
    assert os.path.isfile(args.osm_data_input_file_path)

    result = add_osm_id_tag_to_osm_data(args.osm_data_input_file_path, args.osm_data_output_file_path)

    if args.callback_url is not None:
        return_code_file_path = os.path.join(args.process_infos_dir_name, u'{0}.returncode'.format(job_name))
        with open(return_code_file_path, 'w') as return_code_file:
            return_code_file.write(str(result or 0))
        lock_file_path = os.path.join(args.process_infos_dir_name, u'{0}.lock'.format(job_name))
        os.unlink(lock_file_path)
        urllib2.urlopen(args.callback_url)
    return 0 if result is None else 1


if __name__ == '__main__':
    sys.exit(main())
