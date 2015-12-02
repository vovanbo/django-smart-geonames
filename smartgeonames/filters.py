# -*- coding: utf-8 -*-
import shutil
import tempfile

from smartgeonames import settings

OBJECTS_FILTER = settings.OBJECTS_FILTER


def comment_stripper(iterator):
    for line in iterator:
        if line[:1] == '#':
            continue
        if not line.strip():
            continue
        yield line


def remove_comments(filepath):
    tmp = tempfile.NamedTemporaryFile(mode='wb', delete=True)
    source = open(filepath, 'rb')
    try:
        for line in comment_stripper(source):
            tmp.write(line)
            tmp.flush()
    finally:
        source.close()
        shutil.copy2(tmp.name, filepath)
        tmp.close()


def objects_filter(data):
    result = []
    for filter_key, filter_values in OBJECTS_FILTER.iteritems():
        result.append(data[filter_key] in filter_values)
    return all(result)