# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function

import logging
import os
import shutil
import zipfile
import errno

import pandas
import requests
import time
import csv
from six import StringIO
from django.core.management import BaseCommand
from smartgeonames import settings

DATA_DIR = settings.DATA_DIR

COUNTRIES_FILE_PATH = settings.COUNTRIES_FILE_PATH
COUNTRIES_FILE_LOCAL_PATH = settings.COUNTRIES_FILE_LOCAL_PATH
COUNTRIES_FILTER = settings.COUNTRIES_FILTER
CountryInfoSchema = settings.COUNTRIES_SCHEMA

OBJECTS_FILE_PATH = settings.OBJECTS_FILE_PATH
OBJECTS_FILE_LOCAL_PATH = settings.OBJECTS_FILE_LOCAL_PATH
OBJECTS_FILTER = settings.OBJECTS_FILTER
GeoNameSchema = settings.OBJECTS_SCHEMA

TRANSLATIONS_FILE_PATH = settings.TRANSLATIONS_FILE_PATH
TRANSLATIONS_FILE_LOCAL_PATH = settings.TRANSLATIONS_FILE_LOCAL_PATH
TRANSLATIONS_FILTER = settings.TRANSLATIONS_FILTER
AlternateNameSchema = settings.TRANSLATIONS_SCHEMA

POSTAL_CODES_FILE_PATH = settings.POSTAL_CODES_FILE_PATH
POSTAL_CODES_FILE_LOCAL_PATH = settings.POSTAL_CODES_FILE_LOCAL_PATH
POSTAL_CODES_FILTER = settings.POSTAL_CODES_FILTER
PostalCodeSchema = settings.POSTAL_CODES_SCHEMA

logger = logging.getLogger("smartgeonames")


class GeoNamesDialect(csv.Dialect):
    delimiter = str('\t')
    escapechar = None
    strict = True
    quoting = csv.QUOTE_NONE
    lineterminator = str('\r\n')


def comment_stripper(iterator):
    for line in iterator:
        if line[:1] == '#':
            continue
        if not line.strip():
            continue
        yield line


class Command(BaseCommand):
    help = 'Smart GeoNames manager'
    progress_width = 50
    status_file = os.path.join(DATA_DIR, 'status.csv')
    status_fields = [
        'remote',
        'local',
        'etag',
        'content_length',
        'last_modified',
        'date',
    ]
    memory_mode = None
    without_pandas_mode = None

    def add_arguments(self, parser):
        parser.add_argument(
            '-i', '--import', action='store_true', dest='import',
            default=True,
            help='Import GeoNames data (default: true)'
        )
        parser.add_argument(
            '-d', '--download', action='store_true', dest='download',
            default=False,
            help='Download GeoNames data (default: false)'
        )
        parser.add_argument(
            '--clean-up', action='store_true', dest='clean_up',
            default=False,
            help='Clean-up downloaded files and '
                 'reset status file (default: false)'
        )
        parser.add_argument(
            '--memory-mode', dest='memory_mode',
            choices=['low', 'normal', 'max'],
            default='normal',
            help='Memory mode (default: normal)'
        )
        parser.add_argument(
            '--without-pandas', action='store_true', dest='without_pandas_mode',
            default=False,
            help='Don\'t use Pandas package for CSV parsing (default: false)'
        )

    def handle(self, *args, **options):
        if options.get('clean_up'):
            logger.info('CLEAN-UP')
            try:
                shutil.rmtree(DATA_DIR)
            except os.error:
                logger.error('Nothing to delete! No such directory %s',
                             DATA_DIR)
            else:
                logger.warn('%s is removed.', DATA_DIR)

            try:
                os.remove(self.status_file)
            except os.error:
                logger.error('Nothing to delete! No such file %s',
                             self.status_file)
            else:
                logger.warn('%s is removed.', self.status_file)

        if options.get('download'):
            logger.info('DOWNLOAD')
            self.download(COUNTRIES_FILE_PATH, COUNTRIES_FILE_LOCAL_PATH)
            self.download(OBJECTS_FILE_PATH, OBJECTS_FILE_LOCAL_PATH)
            self.download(TRANSLATIONS_FILE_PATH, TRANSLATIONS_FILE_LOCAL_PATH)
            self.download(POSTAL_CODES_FILE_PATH, POSTAL_CODES_FILE_LOCAL_PATH)

        if options.get('import'):
            self.memory_mode = options.get('memory_mode')
            self.without_pandas_mode = options.get('without_pandas_mode')
            logger.info('IMPORT (memory mode: %s, use Pandas: %s)',
                        self.memory_mode, not self.without_pandas_mode)
            # self.parse(COUNTRIES_FILE_LOCAL_PATH, CountryInfoSchema)
            # self.parse(OBJECTS_FILE_LOCAL_PATH, GeoNameSchema)
            # self.parse(TRANSLATIONS_FILE_LOCAL_PATH, AlternateNameSchema)
            data = self.parse(POSTAL_CODES_FILE_LOCAL_PATH, PostalCodeSchema)
            counter = 0
            errors = 0
            for row in data:
                counter += 1
                if row.errors:
                    errors += 1
                    print(counter)
                # TODO: Make handlers for each file type
                self.postal_code_handler(row)
            print('Total records:', counter)
            print('Records with errors:', errors)

    def postal_code_handler(self, postal_code):
        # print('{0}'.format(counter), end='\r')
        if postal_code.errors:
            # print(row)
            # print(counter, 'ERROR', row_result.errors)
            # print(counter, ', '.join(
            #     [f for f, m in row.errors.iteritems()]))
            print(postal_code)

    def mkdir(self, path):
        path, _ = os.path.split(path)  # get only path to file
        if os.path.exists(path):
            return
        try:
            os.makedirs(path)
        except os.error as e:
            if e.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                logger.error('Folder %s can\'t be created.', path)
                raise
        logger.info('Created folder %s', path)

    def download(self, remote, local):
        self.mkdir(local)

        r = requests.get(remote, stream=True)
        downloaded = 0
        total_length = int(r.headers.get('content-length'))

        if os.path.exists(local):
            etag = r.headers.get('etag')
            is_updated = self.is_file_updated(remote, local, etag)
            if is_updated:
                logger.info(
                    'File %s is up-to-date (Etag: %s).', local, etag)
                return
            else:
                logger.info(
                    'File %s is outdated. Needs to update now.', local)

            backup = local + '.bak'
            logger.info(
                'Create backup of existing local file to %s', backup)
            shutil.copy2(local, backup)

        logger.info('Download of %s in progress\n'
                    'Size: %s bytes\n',
                    remote, total_length)

        with open(local, 'wb') as f:
            start = time.clock()
            for chunk in r.iter_content(chunk_size=4096):
                if chunk:
                    downloaded += len(chunk)
                    f.write(chunk)
                    f.flush()
                    done = int(self.progress_width * downloaded / total_length)
                    percent = float(downloaded) / float(total_length)
                    bps = int(downloaded // (time.clock() - start) / 1024)
                    done_bar = '=' * done
                    remain_bar = ' ' * (self.progress_width - done)
                    print(
                        "[{0}{1}] done: {2:.0%} | speed: {3} kbps".format(
                            done_bar, remain_bar, percent, bps
                        ),
                        end='\r'
                    )
        self.update_status(remote, local, r.headers)
        print('\n')
        return local

    def update_status(self, remote, local, headers):
        status = self.get_status()
        update = {
            'remote': remote,
            'local': local,
            'etag': headers.get('etag'),
            'content_length': headers.get('content-length'),
            'last_modified': headers.get('last-modified'),
            'date': headers.get('date'),
        }
        with open(self.status_file, 'wb') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.status_fields)
            writer.writeheader()
            if not status:
                status = [update, ]
            else:
                status = [f for f in status if f['remote'] != update['remote']]
                status.append(update)
            for row in status:
                writer.writerow(row)

    def get_status(self):
        result = []
        if os.path.exists(self.status_file):
            with open(self.status_file) as csvfile:
                reader = csv.DictReader(csvfile, fieldnames=self.status_fields)
                result = [r for r in reader][1:]  # ignore first row (header)
        return result

    def is_file_updated(self, remote, local, etag):
        status = self.get_status()
        is_updated = False
        for row in status:
            if row['remote'] == remote and \
               row['local'] == local and \
               row['etag'] == etag:
                is_updated = True
        return is_updated

    def parse(self, filepath, schema_class):
        if os.path.exists(filepath):
            filename, ext = os.path.splitext(os.path.basename(filepath))
            data = filepath
            if ext.lower() == '.zip':
                with open(filepath) as csvfile:
                    zfile = zipfile.ZipFile(csvfile)
                    file_in_zip = '.'.join([filename, 'txt'])
                    data = StringIO(zfile.read(file_in_zip))
            schema = schema_class()

            if self.without_pandas_mode:
                reader = csv.DictReader(comment_stripper(data),
                                        dialect=GeoNamesDialect(),
                                        fieldnames=schema.fields.keys())
                for row in reader:
                    yield schema.load(row)
            else:
                # dtype = {}
                # num_types_to_dtype = {
                #     int: np.int32,
                #     float: np.float64,
                #     decimal.Decimal: np.float64,
                # }
                # for name in schema.fields.keys():
                #     field_type = 'str'
                #     field = schema.fields[name]
                #     if hasattr(field, 'num_type'):
                #         if field.num_type in num_types_to_dtype.keys():
                #             field_type = num_types_to_dtype[field.num_type]
                #     dtype[name] = field_type
                # pprint(dtype)

                options = {}
                if self.memory_mode == 'low':
                    options['iterator'] = True
                    options['chunksize'] = 4096

                reader = pandas.read_csv(data,
                                         engine='c',
                                         sep=str('\t'),
                                         escapechar=None,
                                         quoting=csv.QUOTE_NONE,
                                         lineterminator=str('\n'),
                                         header=None,
                                         names=schema.fields.keys(),
                                         na_values=None,
                                         na_filter=False,
                                         keep_default_na=False,
                                         # dtype=dtype)
                                         dtype='str',
                                         **options)
                # Low memory usage mode
                # ./manage.py smartgeonames --memory-mode low  265,09s user 1,11s system 99% cpu 4:27,65 total
                if self.memory_mode == 'low':
                    for records in reader:
                        for row in records.itertuples():
                            yield schema.load(row._asdict())
                # Normal memory usage mode
                # ./manage.py smartgeonames --memory-mode normal  256,56s user 1,08s system 99% cpu 4:18,95 total
                elif self.memory_mode == 'normal':
                    for row in reader.itertuples():
                        yield schema.load(row._asdict())
                # Maximum memory usage mode
                # ./manage.py smartgeonames --memory-mode max  230,07s user 1,90s system 99% cpu 3:53,09 total
                else:
                    for row in reader.to_dict(orient='records'):
                        yield schema.load(row)
