# -*- coding: utf-8 -*-

from os import makedirs
from os.path import join, isdir
from getpass import getpass

from django.conf import settings
from django.core.management.base import BaseCommand
from library.models import PressReview

from _private import (
    init_whippet_session, get_months_urls, get_pdfs_urls, pdf_name_to_date)


class Command(BaseCommand):
    help = """Fetch all press reviews links and download pdfs in
    media/library/pressreviews/ if they are not present"""

    def add_arguments(self, parser):
        # TODO: handle today fetch behaviour for better efficiency
        parser.add_argument('--today', help='Only fetch today\'s press review',
                            action='store_true')
        parser.add_argument(
            '--yes',
            help='Answers y for each new review import prompt',
            action='store_true'
        )
        parser.add_argument(
            '--user',
            help='Whippet user to perform requests'
        )
        parser.add_argument(
            '--password',
            help='Whippet password to perform requests'
        )

    def handle(self, *args, **options):
        if options['today']:
            self.stdout.write('Fetching today...')

        else:
            self.stdout.write('Fetching...')

        if options['yes']:
            yes = True

        else:
            yes = False

        whippet_url = settings.WHIPPET['url']
        login_url = '{}{}'.format(whippet_url, settings.WHIPPET['login'])
        data_url = '{}{}'.format(
            whippet_url, settings.WHIPPET['press_review_home'])

        if options['user']:
            user = options['user']

        else:
            user = raw_input('user: ')

        if options['password']:
            password = options['password']

        else:
            password = getpass('pass: ')

        pressreviews_dir = join(settings.MEDIA_ROOT, 'pressreviews')
        if isdir(pressreviews_dir) is False:
            makedirs(pressreviews_dir)

        s = init_whippet_session(login_url, user, password)
        periods_urls = get_months_urls(s, data_url)

        for year, months in periods_urls.items():
            for month, month_url in months.items():
                month_pdfs = get_pdfs_urls(
                    s,
                    '{}/mod/book/{}'.format(whippet_url, month_url)
                )
                for pdf, pdf_url in month_pdfs.items():
                    if 'brokenfile' not in pdf_url:
                        # dd_mm_YY -> YYYY-mm-dd
                        pdf_date = pdf_name_to_date(pdf)
                        self.download_review(
                            s, pdf, pdf_url, pdf_date, yes=yes)

    def download_review(self, s, pdf, pdf_url, date, yes=False):
        review = PressReview.objects.filter(date=date)
        if not review.exists():
            if yes is False:
                prompt = '{} press review not detected. Download {} ? '.format(
                    pdf, pdf_url)

                answer = raw_input(prompt)
                if answer not in ['y', 'Y']:
                    self.stdout.write('Did not download {}'.format(pdf))
                    return

            pdf_name = '{}.pdf'.format(date)
            pdf_location = join(
                settings.MEDIA_ROOT, 'pressreviews', pdf_name)

            self.stdout.write('Downloading {} pdf in {}...'.format(
                pdf, pdf_location))
            with open(pdf_location, 'wb') as pdf_handle:
                response = s.get(pdf_url, stream=True)

                if response.ok:
                    for block in response.iter_content(1024):
                        pdf_handle.write(block)

                    self.stdout.write('Importing {}...'.format(pdf))
                    local_url = '{}{}{}'.format(
                        settings.MEDIA_URL,
                        'pressreviews/',
                        pdf_name
                    )
                    PressReview.objects.create(date=date, link=local_url)

                else:  # is something went wrong
                    self.stdout.write('Could not download {}'.format(
                        pdf_url))
