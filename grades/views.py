# -*- coding: utf-8 -*-

from urllib2 import (HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler,
                     build_opener, install_opener, urlopen,
                     HTTPCookieProcessor)
from cookielib import CookieJar

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework import status

from grades.serializers import MyGradesSerializer
from grades.parsers import SchoolGradesParser, SchoolYearsParser


def install_wapiti_opener(domain, user, passwd):
    """
    urllib2 can open pages with a default opener : no user, no password, just a
    query on an http resource. But creating a custom opener allows to give auto
    credentials and handle cookies, which we need due to the asp awful
    application implementation.
    """

    cookiejar = CookieJar()

    password_manager = HTTPPasswordMgrWithDefaultRealm()
    password_manager.add_password(None, domain, user, passwd)
    handler = HTTPBasicAuthHandler(password_manager)

    opener = build_opener(handler, HTTPCookieProcessor(cookiejar))
    install_opener(opener)


def get_school_years_urls(url):
    """
    From default school grades page you have a list of all your years spent in
    Telecom. This function list those years by reading available links via
    SchoolYearsParser and return a list of relative links.
    Ex: ['/Commun/ens/adm/pf/pgs/etudiant/consulterResSco.aspx?anSco=19&' \\
         'rangEtu=35 sur 83', link2, link3, ...]
    """

    list_school_years_html = urlopen(url)

    list_school_years_data = ""
    for line in list_school_years_html.readlines():
        line = line.strip()
        list_school_years_data += line

    parser = SchoolYearsParser()
    parser.feed(list_school_years_data)
    school_years_urls = parser.years
    parser.close()

    return school_years_urls


def find_string_between(string, sub_first, sub_last):
    """
    Common function to find a substring surrounded by sub_first and sub_last.
    sub_last can be set to None if for example you expect to isolate something
    at the end of the string. In this case, the whole string after sub_first is
    returned.

    In case submitted data raises a ValueError, an empty string will be
    returned instead.
    """

    try:
        start = string.index(sub_first) + len(sub_first)
        if sub_last is not None:
            end = string.index(sub_last, start)
            return string[start:end]

        else:
            return string[start:]

    except ValueError:
        return ''


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

        serializer = MyGradesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        domain = 'https://wapiti.telecom-lille.fr'
        user = serializer.validated_data['wapiti_username']
        passwd = serializer.validated_data['wapiti_password']
        install_wapiti_opener(domain, user, passwd)

        authelv = '{}/authelv.php'.format(domain)
        urlopen(authelv)

        years_overview_url = '{}/Commun/ens/adm/pf/pgs/login.aspx'.format(
            domain)
        school_years_urls = get_school_years_urls(years_overview_url)

        grades = []
        for school_year_url in school_years_urls:
            year_grades_url = '{}{}'.format(domain, school_year_url)
            year_grades = get_year_grades(year_grades_url)
            grades.append(year_grades)

        return Response(grades, status=status.HTTP_200_OK)
