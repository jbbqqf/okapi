# -*- coding: utf-8 -*-

from library.parsers import PressReviewMonthsParser, PressReviewPDFParser


def get_months_urls(s, url):
    """
    From press reviews home page there is a table of contents listing all
    years and months on which press reviews have been recorded. This function
    list those months and associate them with links to whippet pages.

    Ex: {"2015": {"Avril": link, "Août": link, ...}, "2014": {...}, ...}
    """

    request = s.get(url)
    list_months_html = request.text

    parser = PressReviewMonthsParser()
    parser.feed(list_months_html)
    parser.close()

    return parser.urls


def get_pdfs_urls(s, url):
    """
    On a given press review page there is in general a three-columns list where
    you can find all dates on which a press review has been made (working
    days). This function uses PressReviewPDFParser to extract all those dates
    and associate them with a direct link to the pdf resource.

    Ex: {"2015": {"Avril": {"10_04_15.pdf": link, ...}, ...}, ...}
    """

    request = s.get(url)
    list_pdfs_html = request.text

    parser = PressReviewPDFParser()
    parser.feed(list_pdfs_html)
    parser.close()

    return parser.pdf_urls


def pdf_name_to_date(pdf_name):
    """
    Alexia Simon's convention to name her pdfs with the current date is
    dd_mm_YY and sometimes dd_mm_YYYY. Django's convention is YYYY-mm-dd. This
    function handles the conversion.

    This way of doing things is very precarious since it relies on the fact
    that tomorrow's press reviews will be named with the same convention.
    """

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
