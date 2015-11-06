# -*- coding: utf-8 -*-

from HTMLParser import HTMLParser
from datetime import date


class PressReviewPDFParser(HTMLParser):
    """
    HTMLParser implementation to extract press reviews pdf link from a press
    review month page.
    """

    def __init__(self):
        HTMLParser.__init__(self)

        # Structure receiving urls. At the end it should look like :
        # {"MonthA": {"pdf_name": "pdf_url", ...}, "MonthB": ...}
        self.pdf_urls = {}

        # Toggle True/False when data are interesting, which is on the first
        # table tag
        self.parsing_pdf_urls = False
        self.table_counter = 0

    def handle_starttag(self, tag, attrs):
        if self.parsing_pdf_urls is False:
            if tag == 'table':
                self.table_counter += 1
                if self.table_counter == 1:
                    self.parsing_pdf_urls = True

            return

        if tag == 'a':
            for attr, value in attrs:
                if attr == 'href':
                    # splitting to get only the last part of the url, aka
                    # the filename
                    splited_url = value.split('/')
                    pdf_name = splited_url[-1]
                    self.pdf_urls[pdf_name] = value

    def handle_endtag(self, tag):
        if self.parsing_pdf_urls is True:

            if tag == 'table':
                if self.table_counter == 1:
                    self.parsing_pdf_urls = False
                    return

    def handle_data(self, data):
        pass


class PressReviewMonthsParser(HTMLParser):
    """
    HTMLParser implementation to extract whippet url links giving access to
    each press review month page.
    """

    def __init__(self):
        HTMLParser.__init__(self)

        # Handle_data is triggered even outside of tags. current_tag records
        # the most opened tags, and is set to None when a tag is closed.
        self.current_tag = None

        # Structure receiving urls. At the end it should look like :
        # {"Year": {"MonthA", "MonthB", ...}, "Year2": ...}
        self.urls = {}
        self.current_year = None

        # Toggle True/False when data are interesting, which is on the first
        # div tag with a class attribute with value `book_toc_bullets clearfix`
        self.parsing_toc = False

        self.in_year = False
        self.in_month = False

        self.years = self.generate_years_range(2014)

    def generate_years_range(self, earliest_year):
        """
        Generate a list of years in strings from earliest_year to current_year.
        """

        this_year = date.today().year

        years = []
        for year in range(earliest_year, this_year + 1):
            years.append(str(year))

        return years

    def handle_starttag(self, tag, attrs):
        if self.parsing_toc is False:
            if tag == 'div':
                if ('class', 'book_toc_bullets clearfix') in attrs:
                    self.parsing_toc = True

            return

        self.current_tag = tag

        if self.in_year is True:
            # Each a tag in a year section is a month
            if tag == 'a':
                month = None
                url = None
                for attr, value in attrs:
                    if attr == 'title':
                        month = value

                    elif attr == 'href':
                        url = value

                if month and url:
                    self.current_year[month] = url

    def handle_endtag(self, tag):
        if self.parsing_toc is True:
            if tag == 'div':
                self.parsing_toc = False
                return

            self.current_tag = None

            if self.in_year is True:
                if tag == 'ul':
                    self.in_year = False

    def handle_data(self, data):
        if self.parsing_toc is True:
            if self.in_year is False:
                self.in_year = True

                for year in self.years:
                    if year in data:
                        self.current_year = {}
                        self.urls[year] = self.current_year
