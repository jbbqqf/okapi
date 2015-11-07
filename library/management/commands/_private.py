# -*- coding: utf-8 -*-

from library.parsers import PressReviewMonthsParser, PressReviewPDFParser


def get_months_urls(s, url):
    request = s.get(url)
    list_months_html = request.text

    parser = PressReviewMonthsParser()
    parser.feed(list_months_html)
    parser.close()

    return parser.urls


def get_pdfs_urls(s, url):
    request = s.get(url)
    list_pdfs_html = request.text

    parser = PressReviewPDFParser()
    parser.feed(list_pdfs_html)
    parser.close()

    return parser.pdf_urls


def pdf_name_to_date(pdf_name):
    name_and_extension = pdf_name.split('.')
    short_name = name_and_extension[0]

    splited_name = short_name.split('_')
    day = splited_name[0]
    month = splited_name[1]
    year = splited_name[2]
    # Workaround to avoid some misnamed pdfs since the majority of pdfs are
    # named dd_mm_YY, a pdf named dd_mm_YYYY is considered misnamed
    if len(year) == 2:
        year = '20{}'.format(year)

    date = '{}-{}-{}'.format(year, month, day)
    return date
