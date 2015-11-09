# -*- coding: utf-8 -*-

from urllib2 import urlopen
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework import status

from common.http import install_wapiti_opener
from common.common import find_string_between
from grades.serializers import WapitiLoginSerializer
from grades.parsers import (SchoolGradesParser, SchoolJuriesParser,
                            SchoolCertificationsParser, SchoolYearsParser)


def get_years_urls(url):
    """
    From default school grades page you have a list of all your years spent in
    Telecom. This function list those years by reading available links via
    SchoolYearsParser and return a dictionnary with keys being ['grades',
    'juries', 'certifs'] and values a list of relative links.

    Ex: {'grades': ['/Commun/ens/adm/pf/pgs/etudiant/consulterResSco.aspx?' \\
                    'anSco=19&rangEtu=35 sur 83', link2, link3, ...],
         'juries': [link1, link2, ...],
         'certifs': [link1, link2, ...]}
    """

    list_years_html = urlopen(url)

    list_years_data = ""
    for line in list_years_html.readlines():
        line = line.strip()
        list_years_data += line

    parser = SchoolYearsParser()
    parser.feed(list_years_data)

    years_urls = {}
    years_urls['grades'] = parser.grades_years
    years_urls['juries'] = parser.juries_years
    years_urls['certifs'] = parser.certifications_years

    parser.close()

    return years_urls


def get_year_grades(year_grades_url):
    """
    Make use of SchoolGradesParser to parse all available data on your school
    year grades pages and compact it in one big JSON structure.

    Some data like the number of students and year id cannot be fetched on the
    page so the url to access the page is used instead.
    """

    year_grades_html = urlopen(year_grades_url)

    year_grades_data = ""
    for line in year_grades_html.readlines():
        year_grades_data += line

    parser = SchoolGradesParser()
    parser.feed(year_grades_data)
    year_grades = parser.grades
    parser.close()

    # Workaround to get number of students in your schoolyear as well as
    # year `id`. I don't know why it is not accessible on the page...
    # Url example : '/Commun/ens/adm/pf/pgs/etudiant/consulterResSco.aspx?' \
    # 'anSco=19&rangEtu=35 sur 83'
    # Note : I don't know exactly where does year id come from, but I suspect
    # it to be an incremented value since the year they released this grades
    # app. In this case, it would be school year 1995-1996 which could be
    # matching the first year of the first FIs.
    students = find_string_between(year_grades_url, 'sur ', None)
    year_id = find_string_between(year_grades_url, 'anSco=', '&rangEtu')

    year_grades['students'] = students
    year_grades['year_id'] = year_id

    return year_grades


def get_year_juries(year_juries_url):
    year_juries_html = urlopen(year_juries_url)

    year_juries_data = ""
    for line in year_juries_html.readlines():
        year_juries_data += line

    parser = SchoolJuriesParser()
    parser.feed(year_juries_data)
    year_juries = parser.juries
    parser.close()

    return year_juries


def get_year_certifications(year_certifications_url):
    year_certifications_html = urlopen(year_certifications_url)

    year_certifications_data = ""
    for line in year_certifications_html.readlines():
        year_certifications_data += line

    parser = SchoolCertificationsParser()
    parser.feed(year_certifications_data)
    year_certifications = parser.certifications
    parser.close()

    return year_certifications


@permission_classes((AllowAny,))
class MyGradesView(APIView):
    """
    === Access your school grades via webservice ! ===

    Anyone can access it since it does not provide anything else than what you
    can read on your wapiti pages. That's also why you need to provide your
    wapiti credentials each time your make a request here.
    """

    def get(self, request, *args, **kwargs):
        """
        === Return your school grades in JSON ===

        Since the amount of collected data can be huge depending on the number
        of years the student spent in Telecom Lille ;), and as swagger does not
        allow to format output with carriage return, an exemple of output can
        be found here : http://wiki.bdetl.org/doku.php?id=okapi_grades.

        You need to provide some JSON data in order to be able to access this
        endpoint. Indeed, Wapiti and Okapi credentials do not necessarly share
        the same login credentials. It will often be the same, but a student
        can gradute or can forget to synchronize his old password...

        Anyway, you need to provide wapiti_username and wapiti_password in
        application/form-data JSON. Keep always in mind that to access a
        resource on Wapiti you need to prefix your username by `elv/`. An error
        will remind you that if your loggin fails and your forget this prefix.
        It could be automaticaly added, but this kind of automation is more
        likely to be handled on user interface than on backend.

        Since you need to provide some application/form-data on a GET method,
        which is unorthodox, django rest framework tools do not provide
        built-in views to test the API... sorry for the inconvenience...
        """

        serializer = WapitiLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        wapiti_url = settings.WAPITI['url']
        user = serializer.validated_data['wapiti_username']
        passwd = serializer.validated_data['wapiti_password']
        install_wapiti_opener(wapiti_url, user, passwd)

        wapiti_login_url = '{}{}'.format(wapiti_url, settings.WAPITI['login'])
        urlopen(wapiti_login_url)

        years_overview_url = '{}{}'.format(
            wapiti_url, settings.WAPITI['years_overview'])
        grades_years_urls = get_years_urls(years_overview_url)['grades']

        grades = []
        for school_year_url in grades_years_urls:
            year_grades_url = '{}{}'.format(wapiti_url, school_year_url)
            year_grades = get_year_grades(year_grades_url)
            grades.append(year_grades)

        return Response(grades, status=status.HTTP_200_OK)


@permission_classes((AllowAny,))
class MyJuriesView(APIView):
    """
    === Access your school juries via webservice ! ===

    Anyone can access it since it does not provide anything else than what you
    can read on your wapiti pages. That's also why you need to provide your
    wapiti credentials each time your make a request here.
    """

    def get(self, request, *args, **kwargs):
        """
        === Return your school juries in JSON ===

        You need to provide some JSON data in order to be able to access this
        endpoint. Indeed, Wapiti and Okapi credentials do not necessarly share
        the same login credentials. It will often be the same, but a student
        can gradute or can forget to synchronize his old password...

        Anyway, you need to provide wapiti_username and wapiti_password in
        application/form-data JSON. Keep always in mind that to access a
        resource on Wapiti you need to prefix your username by `elv/`. An error
        will remind you that if your loggin fails and your forget this prefix.
        It could be automaticaly added, but this kind of automation is more
        likely to be handled on user interface than on backend.

        Since you need to provide some application/form-data on a GET method,
        which is unorthodox, django rest framework tools do not provide
        built-in views to test the API... sorry for the inconvenience...
        """

        serializer = WapitiLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        wapiti_url = settings.WAPITI['url']
        user = serializer.validated_data['wapiti_username']
        passwd = serializer.validated_data['wapiti_password']
        install_wapiti_opener(wapiti_url, user, passwd)

        wapiti_login_url = '{}{}'.format(wapiti_url, settings.WAPITI['login'])
        urlopen(wapiti_login_url)

        years_overview_url = '{}{}'.format(
            wapiti_url, settings.WAPITI['years_overview'])
        juries_years_urls = get_years_urls(years_overview_url)['juries']

        juries = []
        for school_year_url in juries_years_urls:
            year_juries_url = '{}{}'.format(wapiti_url, school_year_url)
            year_juries = get_year_juries(year_juries_url)
            juries.append(year_juries)

        return Response(juries, status=status.HTTP_200_OK)


@permission_classes((AllowAny,))
class MyCertificationsView(APIView):
    """
    === Access your school certifications via webservice ! ===

    Anyone can access it since it does not provide anything else than what you
    can read on your wapiti pages. That's also why you need to provide your
    wapiti credentials each time your make a request here.
    """

    def get(self, request, *args, **kwargs):
        """
        === Return your school certifications in JSON ===

        School certifications are english, german, spanish and whatsoever
        language exams that you can take in Telecom Lille. Results are
        supposed to be identical for each year. Despite that, a list item per
        year is returned in case one day there are different values.

        You need to provide some JSON data in order to be able to access this
        endpoint. Indeed, Wapiti and Okapi credentials do not necessarly share
        the same login credentials. It will often be the same, but a student
        can gradute or can forget to synchronize his old password...

        Anyway, you need to provide wapiti_username and wapiti_password in
        application/form-data JSON. Keep always in mind that to access a
        resource on Wapiti you need to prefix your username by `elv/`. An error
        will remind you that if your loggin fails and your forget this prefix.
        It could be automaticaly added, but this kind of automation is more
        likely to be handled on user interface than on backend.

        Since you need to provide some application/form-data on a GET method,
        which is unorthodox, django rest framework tools do not provide
        built-in views to test the API... sorry for the inconvenience...
        """

        serializer = WapitiLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        wapiti_url = settings.WAPITI['url']
        user = serializer.validated_data['wapiti_username']
        passwd = serializer.validated_data['wapiti_password']
        install_wapiti_opener(wapiti_url, user, passwd)

        wapiti_login_url = '{}{}'.format(wapiti_url, settings.WAPITI['login'])
        urlopen(wapiti_login_url)

        years_overview_url = '{}{}'.format(
            wapiti_url, settings.WAPITI['years_overview'])
        certifs_years_urls = get_years_urls(years_overview_url)['certifs']

        certifs = []
        for school_year_url in certifs_years_urls:
            year_certifs_url = '{}{}'.format(wapiti_url, school_year_url)
            year_certifs = get_year_certifications(year_certifs_url)
            certifs.append(year_certifs)

        return Response(certifs, status=status.HTTP_200_OK)
