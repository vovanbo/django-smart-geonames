# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, print_function

from django.contrib.gis.geos import Point
from marshmallow import Schema, fields, pre_load, post_load
from marshmallow.validate import Length, Range
from unidecode import unidecode


class SmartGeoNamesBaseSchema(Schema):
    @pre_load
    def clean_up(self, in_data):
        in_data = {k: v or None for k, v in in_data.iteritems()}
        return in_data


class GeoNamesRecordSchema(SmartGeoNamesBaseSchema):
    """
    geonameid         : integer id of record in geonames database
    name              : name of geographical point (utf8) varchar(200)
    asciiname         : name of geographical point
                        in plain ascii characters, varchar(200)
    alternatenames    : alternatenames, comma separated, ascii names
                        automatically transliterated, convenience attribute
                        from alternatename table, varchar(10000)
    latitude          : latitude in decimal degrees (wgs84)
    longitude         : longitude in decimal degrees (wgs84)
    feature_class     : see http://www.geonames.org/export/codes.html, char(1)
    feature_code      : see http://www.geonames.org/export/codes.html,
                        varchar(10)
    country_code      : ISO-3166 2-letter country code, 2 characters
    cc2               : alternate country codes, comma separated,
                        ISO-3166 2-letter country code, 200 characters
    admin1_code       : fipscode (subject to change to iso code),
                        see exceptions below, see file admin1Codes.txt
                        for display names of this code; varchar(20)
    admin2_code       : code for the second administrative division,
                        a county in the US, see file admin2Codes.txt;
                        varchar(80)
    admin3_code       : code for third level administrative division,
                        varchar(20)
    admin4_code       : code for fourth level administrative division,
                        varchar(20)
    population        : bigint (8 byte int)
    elevation         : in meters, integer
    dem               : digital elevation model, srtm3 or gtopo30,
                        average elevation of 3''x3'' (ca 90mx90m)
                        or 30''x30'' (ca 900mx900m) area in meters,
                        integer. srtm processed by cgiar/ciat.
    timezone          : the timezone id (see file timeZone.txt) varchar(40)
    modification_date : date of last modification in yyyy-MM-dd format
    """
    geonameid = fields.Integer(required=True)
    name = fields.String(required=True, validate=Length(max=200))
    asciiname = fields.String(required=True, validate=Length(max=200))
    alternatenames = fields.String(validate=Length(max=10000), allow_none=True)
    latitude = fields.Float()
    longitude = fields.Float()
    feature_class = fields.String(required=True, validate=Length(min=1, max=1))
    feature_code = fields.String(validate=Length(max=10))
    country_code = fields.String(required=True, validate=Length(min=2, max=2))
    cc2 = fields.String(validate=Length(max=200), allow_none=True)
    admin1_code = fields.String(validate=Length(max=20), allow_none=True)
    admin2_code = fields.String(validate=Length(max=80), allow_none=True)
    admin3_code = fields.String(validate=Length(max=20), allow_none=True)
    admin4_code = fields.String(validate=Length(max=20), allow_none=True)
    population = fields.Integer()
    elevation = fields.Integer(allow_none=True)
    dem = fields.Integer()
    timezone = fields.String(validate=Length(max=40), allow_none=True)
    modification_date = fields.Date()

    class Meta:
        ordered = True

    @pre_load
    def convert_name_to_asciiname_if_not_exists(self, in_data):
        if not in_data['asciiname']:
            in_data['asciiname'] = unidecode(unicode(in_data['name'], "utf-8"))
            print(in_data['asciiname'], in_data['name'])
        return in_data

    @post_load
    def post_processing(self, data):
        self.setup_location_point(data)
        self.remove_unused_fields(data)
        return data

    def setup_location_point(self, data):
        data['location'] = None
        if data['latitude'] and data['longitude']:
            data['location'] = Point(data['latitude'], data['longitude'])
        return data

    def remove_unused_fields(self, data):
        data.pop('cc2')
        data.pop('latitude')
        data.pop('longitude')
        return data


class AlternateNameSchema(SmartGeoNamesBaseSchema):
    """
    alternateNameId   : the id of this alternate name, int
    geonameid         : geonameId referring to id in table 'geoname', int
    isolanguage       : iso 639 language code 2- or 3-characters;
                        4-characters 'post' for postal codes
                        and 'iata','icao' and faac for airport codes,
                        fr_1793 for French Revolution names,
                        abbr for abbreviation,
                        link for a website,
                        varchar(7)
    alternate name    : alternate name or name variant,
                        varchar(200)
    isPreferredName   : '1', if this alternate name is an official/preferred
                        name
    isShortName       : '1', if this is a short name
                        like 'California' for 'State of California'
    isColloquial      : '1', if this alternate name is a colloquial
                        or slang term
    isHistoric        : '1', if this alternate name is historic and was used
                        in the past
    """
    alternateNameId = fields.Integer(required=True)
    geonameid = fields.Integer(required=True)
    isolanguage = fields.String(validate=Length(max=7), allow_none=True)
    alternate_name = fields.String(validate=Length(max=200))
    isPreferredName = fields.Boolean(allow_none=True)
    isShortName = fields.Boolean(allow_none=True)
    isColloquial = fields.Boolean(allow_none=True)
    isHistoric = fields.Boolean(allow_none=True)

    class Meta:
        ordered = True


class CountryInfoSchema(SmartGeoNamesBaseSchema):
    iso_3166_1_a2 = fields.String(required=True, validate=Length(min=2, max=2))
    iso_3166_1_a3 = fields.String(required=True, validate=Length(min=3, max=3))
    iso_3166_1_numeric = fields.String(required=True,
                                       validate=Length(min=1, max=3))
    fips = fields.String(allow_none=True)
    country = fields.String(required=True, validate=Length(max=200))
    capital = fields.String(validate=Length(max=200), allow_none=True)
    area = fields.Decimal()
    population = fields.Integer()
    continent = fields.String(required=True, validate=Length(min=2, max=2))
    tld = fields.String(validate=Length(min=3, max=3), allow_none=True)
    currency_code = fields.String(validate=Length(min=3, max=3),
                                  allow_none=True)
    currency_name = fields.String(allow_none=True)
    phone = fields.String(allow_none=True)
    postal_code_format = fields.String(allow_none=True)
    postal_code_regex = fields.String(allow_none=True)
    languages = fields.String(allow_none=True)
    geonameid = fields.Integer()
    neighbours = fields.String(allow_none=True)
    equivalent_fips_code = fields.String(allow_none=True)

    class Meta:
        ordered = True


class PostalCodeSchema(SmartGeoNamesBaseSchema):
    """
    country code      : iso country code, 2 characters
    postal code       : varchar(20)
    place name        : varchar(180)
    admin name1       : 1. order subdivision (state) varchar(100)
    admin code1       : 1. order subdivision (state) varchar(20)
    admin name2       : 2. order subdivision (county/province) varchar(100)
    admin code2       : 2. order subdivision (county/province) varchar(20)
    admin name3       : 3. order subdivision (community) varchar(100)
    admin code3       : 3. order subdivision (community) varchar(20)
    latitude          : estimated latitude (wgs84)
    longitude         : estimated longitude (wgs84)
    accuracy          : accuracy of lat/lng from 1=estimated to 6=centroid
    """
    country_code = fields.String(required=True, validate=Length(min=2, max=2))
    postal_code = fields.String(required=True, validate=Length(max=20))
    place_name = fields.String(required=True, validate=Length(max=180))
    admin_name1 = fields.String(validate=Length(max=100), allow_none=True)
    admin_code1 = fields.String(validate=Length(max=20), allow_none=True)
    admin_name2 = fields.String(validate=Length(max=100), allow_none=True)
    admin_code2 = fields.String(validate=Length(max=20), allow_none=True)
    admin_name3 = fields.String(validate=Length(max=100), allow_none=True)
    admin_code3 = fields.String(validate=Length(max=20), allow_none=True)
    latitude = fields.Decimal()
    longitude = fields.Decimal()
    accuracy = fields.Integer(validate=Range(min=1, max=6), allow_none=True)

    class Meta:
        ordered = True


class Admin1CodesSchema(SmartGeoNamesBaseSchema):
    """
    ASCII names of admin divisions.
    http://download.geonames.org/export/dump/admin1CodesASCII.txt

    concatenated code   : country_code<dot>admin1_code
    name                : name of geographical point (utf8) varchar(200)
    asciiname           : name of geographical point
                          in plain ascii characters, varchar(200)
    geonameId           : integer id of record in geonames database
    """
    concatenated_code = fields.String(required=True)
    name = fields.String(required=True, validate=Length(max=200))
    asciiname = fields.String(required=True, validate=Length(max=200))
    geonameid = fields.Integer(required=True)

    class Meta:
        ordered = True

    @post_load
    def divide_concatenated_code(self, data):
        data['country_code'], data['admin1_code'] = \
            data['concatenated_code'].split('.')
        return data


class Admin2CodesSchema(SmartGeoNamesBaseSchema):
    """
    Names for administrative subdivision 'admin2 code'
    http://download.geonames.org/export/dump/admin2Codes.txt

    concatenated code   : country_code<dot>admin1_code<dot>admin2_code
    name                : name of geographical point (utf8) varchar(200)
    asciiname           : name of geographical point
                          in plain ascii characters, varchar(200)
    geonameId           : integer id of record in geonames database
    """
    concatenated_code = fields.String(required=True)
    name = fields.String(required=True, validate=Length(max=200))
    asciiname = fields.String(required=True, validate=Length(max=200))
    geonameid = fields.Integer(required=True)

    class Meta:
        ordered = True

    @post_load
    def divide_concatenated_code(self, data):
        data['country_code'], data['admin1_code'], data['admin2_code'] = \
            data['concatenated_code'].split('.')
        return data
