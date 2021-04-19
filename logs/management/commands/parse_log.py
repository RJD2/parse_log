import re
import logging
from datetime import datetime

import requests
from django.conf import settings
from django.core.management import BaseCommand

from logs.models import Log

logger = logging.getLogger(__name__)

REGEX = "([(\d\.)]+.*) - .* \[(.*?)\] \"(.*?)\" (\d+) (\d+|-)"


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('url', nargs='+', type=str)

    def handle(self, *args, **options):
        url = options['url'][0]
        logger.info(f"Start downloading {url}")
        filename = self.download_file(url)
        res = {'total': 0, 'error': 0, 'success': 0}
        logger.info(f"Start parsing {filename}")
        with open(f'{settings.MEDIA_ROOT}logs/{filename}') as f:
            for line in f:
                if line == '\n':
                    logger.error('Empty line')
                    continue
                if self.save_log(line):
                    res['success'] += 1
                else:
                    res['error'] += 1
                res['total'] += 1
        logger.info(
            f"Finish parsing {filename}. Total: {res['total']}, success: {res['success']}, errors: {res['error']}")

    @staticmethod
    def download_file(url: str) -> str:
        filename = f'{int(datetime.timestamp(datetime.now()))}_{url.split("/")[-1]}'
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(f'{settings.MEDIA_ROOT}logs/{filename}', 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return filename

    @staticmethod
    def save_log(line: str) -> bool:
        try:
            data = re.match(REGEX, line).groups()
            log = Log()
            log.ip = data[0]
            log.date = datetime.strptime(data[1], "%d/%b/%Y:%H:%M:%S %z")
            log.method = data[2].split()[0]
            log.uri = data[2].split()[1]
            log.status_code = int(data[3]) if data[3].isdigit() else None
            log.size = int(data[4]) if data[4].isdigit() else None
            log.save()
        except Exception as e:
            logger.error(f'Error {e} on line: {line}')
            return False
        return True
