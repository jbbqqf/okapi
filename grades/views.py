from django.shortcuts import render

from urllib2 import HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler, build_opener, install_opener, urlopen, HTTPCookieProcessor
from cookielib import CookieJar

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework import status

from grades.serializers import MyGradesSerializer
from grades.parsers import SchoolGradesParser, SchoolYearsParser

def install_wapiti_opener(domain, user, passwd):
    cookiejar = CookieJar()

    password_manager = HTTPPasswordMgrWithDefaultRealm()
    password_manager.add_password(None, domain, user, passwd)
    handler = HTTPBasicAuthHandler(password_manager)

    opener = build_opener(handler, HTTPCookieProcessor(cookiejar))
    install_opener(opener)

def get_school_years_urls(url):
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
    year_grades_html = urlopen(year_grades_url)

    year_grades_data = ""
    for line in year_grades_html.readlines():
        year_grades_data += line

    parser = SchoolGradesParser()
    parser.feed(year_grades_data)
    year_grades = parser.grades
    parser.close()

    # workaround to get number of students in your schoolyear as well as
    # year `number`
    # /Commun/ens/adm/pf/pgs/etudiant/consulterResSco.aspx?anSco=19&rangEtu=35 sur 83
    students = find_string_between(year_grades_url, 'sur ', None)
    year_id = find_string_between(year_grades_url, 'anSco=', '&rangEtu') 

    year_grades['students'] = students
    year_grades['year_id'] = year_id

    return year_grades

@permission_classes((AllowAny,))
class MyGradesView(APIView):
    def get(self, request, *args, **kwargs):
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
