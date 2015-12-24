# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
from smartgeonames import settings

OBJECTS_IGNORE = settings.OBJECTS_IGNORE
HIERARCHY_TREE_ROOT = settings.HIERARCHY_TREE_ROOT


def dummy_handler(schema, data):
    result = schema.load(data)
    if result.errors:
        # print(result)
        # print(counter, 'ERROR', row_result.errors)
        # print(counter, ', '.join(
        #     [f for f, m in result.errors.iteritems()]))
        print(result)
    return result, result.errors


def object_handler(schema, data, tree):
    result = schema.load(data)
    object = result.data
    if result.errors:
        print(data)
        print(result)
    else:
        object.full_clean()
    return object, result.errors


def hierarchy_builder_handler(schema, data, tree):
    parent = int(data['parent'])
    child = int(data['child'])

    def desc(x):
        return {'desc': x}

    if parent not in OBJECTS_IGNORE and child not in OBJECTS_IGNORE:
        try:
            if not tree.contains(parent):
                tree.create_node(parent, parent, HIERARCHY_TREE_ROOT,
                                 data=desc(parent))
            if child != 0 and not tree.contains(child):
                tree.create_node(child, child, parent,
                                 data=desc(child))
        except:
            print(parent, child)
            raise
    else:
        print(parent, child)
    return tree, {}