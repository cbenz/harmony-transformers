# -*- coding: utf-8 -*-


from imposm.mapping import LineStrings, Options, Points, String


db_conf = Options(
    sslmode='allow',
    prefix='osm_new_',
    proj='epsg:900913',
    )


nodes = Points(
    fields=(
        {fields}
        ),
    mapping={{
        '{unique_id_tag_key}': (
            '__any__',
            ),
        }},
    name='nodes',
    with_type_field=False,
    )


ways = LineStrings(
    fields=(
        {fields}
        ),
    mapping={{
        '{unique_id_tag_key}': (
            '__any__',
            ),
        }},
    name='ways',
    with_type_field=False,
    )
