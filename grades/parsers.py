# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from HTMLParser import HTMLParser


class SchoolGradesParser(HTMLParser):
    """
    Parser implementation to extract all possible data (meta and core) from a
    year grades recap page like `https://wapiti.telecom-lille.fr/Commun/ens/-
    adm/pf/pgs/etudiant/consulterResSco.aspx?anSco=22&rangEtu= sur 120`.

    This implementation is very ugly, like the html page themselves.
    """

    def __init__(self):
        HTMLParser.__init__(self)

        # handle_data is triggered even outside of tags. current_tag records
        # the most recent opened tags, and is set to None when a tag is closed.
        self.current_tag = None

        # grades is the structure when all parsed data will be stored
        self.grades = {}
        self.grades['UVs'] = []

        # In html pages, there are 2 interesting sections : meta data and
        # grades data. When those sections are detected, parsing_meta and
        # parsing_grades will be set to True, and at the end of the section
        # it'll be back to False.
        self.parsing_meta = False
        self.parsing_grades = False

        # Meta datas are in the 3rd table
        # Grades datas are in the 5th table after the 2dn tr tag
        self.table_counter = 0
        self.tr_counter = 0

        # When parsing grades, you can either be in an UV or in an exam section
        self.in_UV = False
        self.in_exam = False

        # Track which meta information is being parsed
        self.meta_tr = -1
        self.meta_td = -1
        # Depending on meta_tr and meta_td, those states will be the keys of
        # the self.grades final dict strucre
        self.meta_states = [
            (u'name', u'credits_so_far'),
            (u'firstname', u'observed_absences'),
            (u'birth_date', u'unexplained_absences'),
            (u'year_label', None),
            (u'rank', None),
        ]
        # Each information is announced in html by the following sentences that
        # will be replaced by an empty string.
        self.meta_str_rm = [
            (u'Nom :', u'Nb crédits validés à ce jour :'),
            (u'Prénom :', u'Nb absences constatées :'),
            (u'Date de naissance :', u'Nb absences non justifées :'),
            (u'Libellé de la promotion :', None),
            (u'Rang :', None),
        ]

        # This is basicaly the same principle as for meta datas
        self.UV_step = -1
        self.UV_states = [
            u'name',
            u'ECTS_total',
            u'ECTS_validated',
            u'average',
            u'ECTS_grade',
        ]
        self.UV_str_rm = [
            u'',
            u'credits:',
            u'obtenus:',
            u'Moy:',
            u'Note ECTS:',
        ]

        # Same principle as for meta datas and UV datas
        self.exam_step = -1
        self.exam_states = [
            u'nickname', u'fulname',
            u'init', u'retake', u'final',
            u'average', u'min', u'max',
        ]

        # Sometimes when parsing grades data, there are less or more td tags.
        # *_step_max constants are here to help detecting when some useless /
        # junk values are encountered.
        self.exam_step_max = len(self.exam_states) - 1
        # +1 because there is always a useless column at the end of each UV tr
        # tag (containing &nbsp;).
        self.UV_step_max = len(self.UV_states) - 1 + 1

    def yet_parsing_what(self, tag, attrs):
        """
        Keep track of progress in html document. Depending on what is detected
        self.parsing_meta and self.parsing_grades might be set to True.

        Meta datas start after the 3rd table tag and grades datas start after
        the 5th table tag and after the 2dn tr tag.
        """

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
        """
        Increment self.meta_tr and self.meta_td when detecting such start tags.
        """

        if tag == 'tr':
            if ('class', 'tdb') in attrs:
                self.meta_tr += 1

        elif tag == 'td':
            self.meta_td += 1

    def handle_startUV(self, tag, attrs):
        """
        Update self.in_UV, self.UV_step and self.current_{UV,exam} depending
        on which tag is detected (tr or td). It does not add data but prepares
        values and structures for the next call to handle_data.
        """

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
        """
        Update self.in_exam, self.exam_step and self.current_exam depending
        on which tag is detected (tr or td). It does not add data but prepares
        values and structures for the next call to handle_data.
        """

        if tag == 'tr':
            if not attrs:
                self.in_exam = True
                self.current_exam = {}

        elif tag == 'td':
            if self.in_exam is True:
                self.exam_step += 1

    def handle_starttag(self, tag, attrs):
        """
        HTMLParser method when a starting tag is encountered. First check if
        parser is in a particular section (meta or grades). If it is not, check
        if this is the right time to active such sections. Else, handle
        operations depending on the section with help of handle_start* methods.
        """

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
        """
        Keep track of progress in html document. Depending on what is detected
        self.parsing_meta and self.parsing_grades might be set to False.

        Meta datas end after the 3rd table tag and grades datas end after the
        5th table.
        """

        if tag == 'table':
            if self.table_counter == 3:
                self.parsing_meta = False

            elif self.table_counter == 5:
                self.parsing_grades = False

    def handle_endmeta(self, tag):
        """
        The only operation handled here is if a tr tag end while
        parsing meta data. If it's the case self.meta_td counter is reset
        to -1.
        """

        if tag == 'tr':
            self.meta_td = -1

    def handle_endUV(self, tag):
        """
        When detecting the end of an exam (ending tr while self.in_exam is
        True), self.current_UV is appended in self.grades, which allows
        to reuse self.current_UV.
        """

        if self.in_UV is True:
            if tag == 'tr':
                # Testing that we got all values we need in case of a
                # junk tr
                if self.UV_step == self.UV_step_max:
                    self.grades['UVs'].append(self.current_UV)

                self.UV_step = -1
                self.in_UV = False

    def handle_endexam(self, tag):
        """
        When detecting the end of an exam (ending tr while self.in_exam is
        True), self.current_exam is appended in self.current_UV, which allows
        to reuse self.current_exam.
        """

        if self.in_exam is True:
            if tag == 'tr':
                # Testing that we got all values we need in case of a
                # junk tr
                if self.exam_step == self.exam_step_max:
                    self.current_UV['exams'].append(self.current_exam)

                self.exam_step = -1
                self.in_exam = False

    def handle_endtag(self, tag):
        """
        HTMLParser method when an ending tag is encountered. First check if
        parser is still parsing a section (meta or grades). If it is check
        if this is not the end of that section and then handle operations
        depending on the section with help of handle_end* methods.
        """

        if self.parsing_meta is True or self.parsing_grades is True:
            self.still_parsing_something(tag)

            self.current_tag = None

            if self.parsing_meta is True:
                self.handle_endmeta(tag)

            elif self.parsing_grades is True:
                self.handle_endUV(tag)
                self.handle_endexam(tag)

    def handle_metadata(self, data):
        """
        Epurate meta parsed data and store it in self.grades big JSON
        structure.
        """

        if self.current_tag == 'td':
            # We don't want to keep label information in our data
            to_remove = self.meta_str_rm[self.meta_tr][self.meta_td]
            data = data.replace(to_remove, '')

            # Make sure we don't have any junk substring (which is at least the
            # case for firstnames
            data = data.replace('&nbsp;', '')

            # Last epuration
            data = data.strip()

            self.grades[self.meta_states[self.meta_tr][self.meta_td]] = data

    def handle_UVdata(self, data):
        """
        Make sure the parser is parsing some good data before epurating and
        storing it in self.current_UV.
        """

        if self.in_UV is True:
            # Make sure what is being parsed is not some junk
            if self.UV_step >= 0 and self.UV_step < self.UV_step_max:
                # Again
                if data != '&nbsp;':
                    to_replace = self.UV_str_rm[self.UV_step]
                    data = data.replace(to_replace, '').strip()
                    self.current_UV[self.UV_states[self.UV_step]] = data

    def handle_examdata(self, data):
        """
        Make sure the parser is parsing some good data before storing it in
        self.current_exam.
        """

        if self.in_exam is True:
            # Make sure what is being parsed is not some junk
            if self.exam_step >= 0 and self.exam_step < self.exam_step_max:
                # Again
                if data != '&nbsp;':
                    self.current_exam[self.exam_states[self.exam_step]] = data

    def handle_data(self, data):
        """
        HTMLParser method when data is encountered. First check if parser is in
        a particular section (meta or grades). If it is, it makes sure that
        data is contained in a tag (not outside, because outside datas are
        ignored), before handling operations depending on the section with help
        of handle_*data methods.
        """

        if self.parsing_meta is True or self.parsing_grades is True:
            if self.current_tag is not None:
                # Make sure we work with unicode
                data = unicode(data, 'utf8')

                if self.parsing_meta is True:
                    self.handle_metadata(data)

                elif self.parsing_grades is True:
                    self.handle_UVdata(data)
                    self.handle_examdata(data)


class SchoolJuriesParser(HTMLParser):
    """
    HTMLParser implementation to extract wapiti published informations about
    juries which can be found at an url like `https://wapiti.telecom-lille.fr/-
    Commun/ens/adm/pf/pgs/etudiant/consulterJury.aspx?anSco=22`.

    You should find one jury per page for most of those pages, but sometimes
    it's not the case... This could be investigated...
    """

    def __init__(self):
        HTMLParser.__init__(self)

        # structure storing recorded juries
        self.juries = []
        # append this dictionnary to juries after each jury's end
        self.current_jury = {}

        # handle_data is triggered even outside of tags. current_tag records
        # the most recent opened tags, and is set to None when a tag is closed.
        self.current_tag = None

        # Those categories will be the keys of the final structure self.juries
        self.categories = [
            'date',
            'decision',
            'comment',
        ]
        # Keep track which category is the next one :
        # += 1 after a td
        # = -1 after a tr
        self.current_category = -1

        # There is only one section that is interesting : the third table,
        # after the first tr. In this section, self.parsing_juries is set to
        # True and is False the rest of the time.
        self.parsing_juries = False
        self.table_counter = 0
        self.in_juries_table = False

    def handle_starttag(self, tag, attrs):
        if self.parsing_juries is False:
            if tag == 'table':
                self.table_counter += 1
                if self.table_counter == 3:
                    self.in_juries_table = True

                return

            # Make sure the first tr used to display titles is not parsed
            if self.in_juries_table is True:
                if tag == 'tr':
                    self.parsing_juries = True

            return

        self.current_tag = tag

        if tag == 'td':
            self.current_category += 1

    def handle_endtag(self, tag):
        if self.parsing_juries is True:
            self.current_tag = None

            if tag == 'table':
                if self.table_counter == 3:
                    self.parsing_juries = False

            elif tag == 'tr':
                if self.current_jury:  # True if not empty
                    self.juries.append(self.current_jury)
                    self.current_jury = {}
                    self.current_category = -1

    def handle_data(self, data):
        if self.parsing_juries is True:
            if self.current_tag == 'td':
                data = unicode(data, 'utf-8')
                data = data.strip()

                if data != '':
                    category = self.categories[self.current_category]
                    self.current_jury[category] = data


class SchoolCertificationsParser(HTMLParser):
    """
    HTMLParser implementation to extract wapiti published informations about
    your english, german and spanish (and whatsoever) which can be found at an
    url like `https://wapiti.telecom-lille.fr/Commun/ens/adm/pf/pgs/etudiant/-
    consulterExamen.aspx?anSco=22`.

    For a given student, you can query different pages (one for each anSco).
    However, you should always find the same informations on each of those
    pages regarding certifications.
    """

    def __init__(self):
        HTMLParser.__init__(self)

        # structure storing recorded certifications
        self.certifications = []
        # append this dictionnary to certifications after each certif's end
        self.current_certification = {}

        # handle_data is triggered even outside of tags. current_tag records
        # the most recent opened tags, and is set to None when a tag is closed.
        self.current_tag = None

        # Keys of the final structure self.certifications
        self.categories = [
            'date',
            'exam',
            'grade',
        ]
        # Keep track which category is the next one :
        # += 1 after a td
        # = -1 after a tr
        self.current_category = -1

        # There is only one section that is interesting : the third table,
        # after the first tr. In this section, self.parsing_certifications is
        # set to True and is False the rest of the time.
        self.parsing_certifications = False
        self.table_counter = 0
        self.in_certifications_table = False

    def handle_starttag(self, tag, attrs):
        if self.parsing_certifications is False:
            if tag == 'table':
                self.table_counter += 1
                if self.table_counter == 3:
                    self.in_certifications_table = True

                return

            # Make sure the first tr used to display titles is not parsed
            if self.in_certifications_table is True:
                if tag == 'tr':
                    self.parsing_certifications = True

            return

        self.current_tag = tag

        if tag == 'td':
            self.current_category += 1

    def handle_endtag(self, tag):
        if self.parsing_certifications is True:
            self.current_tag = None

            if tag == 'table':
                if self.table_counter == 3:
                    self.parsing_certifications = False

            elif tag == 'tr':
                if self.current_certification:  # True if not empty
                    self.certifications.append(self.current_certification)
                    self.current_certification = {}
                    self.current_category = -1

    def handle_data(self, data):
        if self.parsing_certifications is True:
            if self.current_tag == 'td':
                data = unicode(data, 'utf-8')
                data = data.strip()

                if data != '':
                    category = self.categories[self.current_category]
                    self.current_certification[category] = data


class SchoolYearsParser(HTMLParser):
    """
    This parser has been implemented to extract school years URL links listed
    on https://wapiti.telecom-lille.fr/Commun/ens/adm/pf/pgs/login.aspx.
    """

    def __init__(self):
        HTMLParser.__init__(self)

        # Structures to read from the outside to get parsed data.
        self.grades_years = []
        self.juries_years = []
        self.certifications_years = []

    def handle_starttag(self, tag, attrs):
        """
        Check if current tag is an hyperlink tag (<a>) having an href attribute
        in which `consulterResSco.aspx` is present.

        It is ugly, but it works !
        """

        if tag == 'a':
            for attr, value in attrs:
                if attr == 'href':
                    if 'consulterResSco.aspx' in value:
                        self.grades_years.append(value)

                    elif 'consulterJury.aspx' in value:
                        self.juries_years.append(value)

                    elif 'consulterExamen.aspx' in value:
                        self.certifications_years.append(value)
