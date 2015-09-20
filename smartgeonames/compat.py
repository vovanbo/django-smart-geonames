# -*- coding: utf-8 -*-
import csv
import sys

from django.utils import six
from django.core.exceptions import ImproperlyConfigured


# Python3 compatibility layer

"""
Unicode compatible wrapper for CSV reader and writer that abstracts away
differences between Python 2 and 3. A package like unicodecsv would be
preferable, but it's not Python 3 compatible yet.

Code from http://python3porting.com/problems.html
Changes:
- Classes renamed to include CSV.
- Unused 'codecs' import is dropped.
- Added possibility to specify an open file to the writer to send as response
  of a view
"""


PY3 = sys.version > '3'


class UnicodeCSVReader:
    def __init__(self, filename, dialect=csv.excel,
                 encoding="utf-8", **kw):
        self.filename = filename
        self.dialect = dialect
        self.encoding = encoding
        self.kw = kw

    def __enter__(self):
        if PY3:
            self.f = open(self.filename, 'rt',
                          encoding=self.encoding, newline='')
        else:
            self.f = open(self.filename, 'rbU')
        self.reader = csv.reader(self.f, dialect=self.dialect,
                                 **self.kw)
        return self

    def __exit__(self, type, value, traceback):
        self.f.close()

    def next(self):
        row = next(self.reader)
        if PY3:
            return row
        return [s.decode("utf-8") for s in row]

    __next__ = next

    def __iter__(self):
        return self


class UnicodeCSVWriter:
    """
    Python 2 and 3 compatible CSV writer. Supports two modes:
    * Writing to an open file or file-like object:
      writer = UnicodeCSVWriter(open_file=your_file)
      ...
      your_file.close()
    * Writing to a new file:
      with UnicodeCSVWriter(filename=filename) as writer:
          ...
    """
    def __init__(self, filename=None, open_file=None, dialect=csv.excel,
                 encoding="utf-8", **kw):
        if filename is open_file is None:
            raise ImproperlyConfigured(
                "You need to specify either a filename or an open file")
        self.filename = filename
        self.f = open_file
        self.dialect = dialect
        self.encoding = encoding
        self.kw = kw
        self.writer = None

    def __enter__(self):
        assert self.filename is not None
        if PY3:
            self.f = open(self.filename, 'wt',
                          encoding=self.encoding, newline='')
        else:
            self.f = open(self.filename, 'wb')

    def __exit__(self, type, value, traceback):
        assert self.filename is not None
        if self.filename is not None:
            self.f.close()

    def writerow(self, row):
        if self.writer is None:
            self.writer = csv.writer(self.f, dialect=self.dialect, **self.kw)
        if not PY3:
            row = [six.text_type(s).encode(self.encoding) for s in row]
        self.writer.writerow(list(row))

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)