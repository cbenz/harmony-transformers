#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""Data converters for the OSM-GIS-Harmony project."""


from setuptools import setup, find_packages


doc_lines = __doc__.split('\n')


setup(
    author=u'Christophe Benz',
    author_email=u'cbenz@easter-eggs.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        ],
    description=doc_lines[0],
    include_package_data=True,
    install_requires=[
        'imposm >= 2.4.0',
        'lxml >= 2.2.8',
        ],
    keywords='harmony osm gis data converters tile layer',
#    license=u'http://www.fsf.org/licensing/licenses/agpl-3.0.html',
    long_description='\n'.join(doc_lines[2:]),
    name=u'harmony_converters',
    packages=find_packages(),
    url=u'',
    version='0.1',
    zip_safe=False,
    )
