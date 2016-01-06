# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function

from pprint import pprint

from django.core.exceptions import ObjectDoesNotExist
from treelib.tree import NodeIDAbsentError

from smartgeonames import settings
from smartgeonames.models import GeoNamesRecord

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
    obj = None

    def create_children(node, geoname_object):
        created = set()
        children_to_create = node.data['children_to_create']
        for child_id in children_to_create:
            child_node = tree[child_id]
            child_data = child_node.data.get('object')
            if child_data:
                geoname_object.add_child(**child_data)
                created.add(child_id)
        node.data['children_to_create'] = children_to_create - created

    if not result.errors:
        geonameid = result.data['geonameid']
        tree_node = tree.get_node(geonameid)
        try:
            parent_node = tree.parent(geonameid)
        except NodeIDAbsentError:
            parent_node = None

        if tree_node and parent_node:
            if parent_node.identifier == HIERARCHY_TREE_ROOT:
                node_is_created = tree_node.data.get('created', False)
                if not node_is_created:
                    obj = GeoNamesRecord.add_root(**result.data)
                    tree_node.data['created'] = True
                    create_children(tree_node, obj)
            else:
                parent_is_created = parent_node.data.get('created', False)
                if parent_is_created:
                    parent_geo_record = GeoNamesRecord.objects.get(
                            geonameid=geonameid)
                    obj = parent_geo_record.add_child(**result.data)
                    tree_node.data['created'] = True
                    create_children(tree_node, obj)
                else:
                    parent_node.data['children_to_create'].add(geonameid)
                    tree_node.data['object'] = result.data
        else:
            print(result.data)
    else:
        print(data)
        print(result)
    return obj, result.errors


def hierarchy_builder_handler(schema, data, tree):
    parent = int(data['parent'])
    child = int(data['child'])
    default_data = {
        'created': False,
        'children_to_create': set(),
        'object': {},
    }

    if parent not in OBJECTS_IGNORE and child not in OBJECTS_IGNORE:
        try:
            if not tree.contains(parent):
                tree.create_node(parent, parent, HIERARCHY_TREE_ROOT,
                                 data=default_data)
            if child != 0 and not tree.contains(child):
                tree.create_node(child, child, parent, data=default_data)
        except:
            print(parent, child)
            raise
    else:
        print(parent, child)
    return tree, {}