# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from HTMLParser import HTMLParser

class SchoolGradesParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)

        self.current_tag = None

        self.grades = {}
        self.grades['UVs'] = []

        # interesting value begins in the 4th table after the 2dn tr
        self.parsing_meta = False
        self.parsing_grades = False
        self.table_counter = 0
        self.tr_counter = 0

        self.in_UV = False
        self.in_exam = False

        self.meta_tr = -1
        self.meta_td = -1
        self.meta_states = [
            (u'name', u'credits_so_far'),
            (u'firstname', u'observed_absences'),
            (u'birth_date', u'unexplained_absences'),
            (u'year_label', None),
            (u'rank', None),
        ]
        self.meta_str_rm = [
            (u'Nom :', u'Nb crédits validés à ce jour :'),
            (u'Prénom :', u'Nb absences constatées :'),
            (u'Date de naissance :', u'Nb absences non justifées :'),
            (u'Libellé de la promotion :', None),
            (u'Rang :', None),
        ]

        # States : name, ECTS_total, ECTS_validated, average, ECTS_grade
        self.UV_step = -1
        self.UV_states = [
            u'name',
            u'ECTS_total',
            u'ECTS_validated',
            u'average',
            u'ECTS_grade',
        ]
        # +1 because there is a useless column containing &nbsp;
        self.UV_step_max = len(self.UV_states) - 1 + 1
        self.UV_str_rm = [
            u'',
            u'credits:',
            u'obtenus:',
            u'Moy:',
            u'Note ECTS:',
        ]

        # States : nickname, fulname, init, retake, final, avg, min, max
        self.exam_step = -1
        self.exam_states = [
            u'nickname', u'fulname',
            u'init', u'retake', u'final',
            u'average', u'min', u'max',
        ]
        self.exam_step_max = len(self.exam_states) - 1

    def yet_parsing_what(self, tag, attrs):
        if tag == 'table':
            self.table_counter += 1

            if self.table_counter == 3:
                self.parsing_meta = True
    
        if self.table_counter == 5:
            if tag == 'tr':
                self.tr_counter += 1

                if self.tr_counter == 2:
                    self.parsing_grades = True

    def handle_startmeta(self, tag, attrs):
        if tag == 'tr':
            if ('class', 'tdb') in attrs:
                self.meta_tr += 1

        elif tag == 'td':
            self.meta_td += 1

    def handle_startUV(self, tag, attrs):
        if tag == 'tr':
            if ('class', 'uvLine') in attrs:
                self.in_UV = True
                self.current_UV = {}
                self.current_UV['exams'] = []
                self.current_exam = {}

        elif tag == 'td':
            if self.in_UV is True:
                self.UV_step += 1

    def handle_startexam(self, tag, attrs):
        if tag == 'tr':
            if not attrs:
                self.in_exam = True
                self.current_exam = {}

        elif tag == 'td':
            if self.in_exam is True:
                self.exam_step += 1

    def handle_starttag(self, tag, attrs):
        if self.parsing_meta is False and self.parsing_grades is False:
            self.yet_parsing_what(tag, attrs)
            return

        self.current_tag = tag

        if self.parsing_meta is True:
            self.handle_startmeta(tag, attrs)

        if self.parsing_grades is True:
            self.handle_startUV(tag, attrs)
            self.handle_startexam(tag, attrs)

    def still_parsing_something(self, tag):
        if tag == 'table':
            if self.table_counter == 3:
                self.parsing_meta = False

            elif self.table_counter == 5:
                self.parsing_grades = False

    def handle_endmeta(self, tag):
        if tag == 'tr':
            self.meta_td = -1

    def handle_endUV(self, tag):
        if self.in_UV is True:
            if tag == 'tr':
                # testing that we got all values we need in case of a
                # junk tr
                if self.UV_step == self.UV_step_max:
                    self.grades['UVs'].append(self.current_UV)

                self.UV_step = -1
                self.in_UV = False

    def handle_endexam(self, tag):
        if self.in_exam is True:
            if tag == 'tr':
                # testing that we got all values we need in case of a
                # junk tr
                if self.exam_step == self.exam_step_max:
                    self.current_UV['exams'].append(self.current_exam)

                self.exam_step = -1
                self.in_exam = False

    def handle_endtag(self, tag):
        if self.parsing_meta is True or self.parsing_grades is True:
            self.still_parsing_something(tag)

            self.current_tag = None

            if self.parsing_meta is True:
                self.handle_endmeta(tag)

            elif self.parsing_grades is True:
                self.handle_endUV(tag)
                self.handle_endexam(tag)

    def handle_metadata(self, data):
        if self.current_tag == 'td':
            to_remove = self.meta_str_rm[self.meta_tr][self.meta_td]
            data = data.replace(to_remove, '')
            data = data.replace('&nbsp;', '')
            data = data.strip()

            self.grades[self.meta_states[self.meta_tr][self.meta_td]] = data

    def handle_UVdata(self, data):
        if self.in_UV is True:
            if self.UV_step >= 0 and self.UV_step < self.UV_step_max:
                if data != '&nbsp;':
                    data = data.replace(self.UV_str_rm[self.UV_step], '').strip()
                    self.current_UV[self.UV_states[self.UV_step]] = data

    def handle_examdata(self, data):
        if self.in_exam is True:
            if self.exam_step >= 0 and self.exam_step < self.exam_step_max:
                if data != '&nbsp;':
                    self.current_exam[self.exam_states[self.exam_step]] = data

    def handle_data(self, data):
        if self.parsing_meta is True or self.parsing_grades is True:
            if self.current_tag is not None:
                data = unicode(data, 'utf8')
                if self.parsing_meta is True:
                    self.handle_metadata(data)

                elif self.parsing_grades is True:
                    self.handle_UVdata(data)
                    self.handle_examdata(data)

class SchoolYearsParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.years = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr, value in attrs:
                if attr == 'href':
                    if 'consulterResSco.aspx' in value:
                         self.years.append(value)
