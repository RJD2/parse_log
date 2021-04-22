import re
import logging
from datetime import datetime

import requests
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
        res = {'total': 0, 'error': 0, 'success': 0}
        logger.info(f"Start parsing {url}")
        data = self.read_file(url)
        for line in data:
            if line.isspace() or not line:
                logger.error('Empty line')
                continue
            try:
                data = re.match(REGEX, line).groups()
            except Exception as e:
                logger.error(f'Error {e} on line: {line}')
                continue
            if self.save_log(data):
                res['success'] += 1
            else:
                res['error'] += 1
            res['total'] += 1
        logger.info(
            f"Finish parsing {url}. Total: {res['total']}, success: {res['success']}, errors: {res['error']}")

    @staticmethod
    def read_file(url: str) -> str:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            for line in r.iter_lines():
                yield line.decode()

    @staticmethod
    def save_log(data: tuple) -> bool:
        try:
            log = Log()
            log.ip = data[0]
            log.date = datetime.strptime(data[1], "%d/%b/%Y:%H:%M:%S %z")
            log.method = data[2].split()[0]
            log.uri = data[2].split()[1]
            log.status_code = int(data[3]) if data[3].isdigit() else None
            log.size = int(data[4]) if data[4].isdigit() else None
            log.save()
        except Exception as e:
            logger.error(f"Error {e} on saving: {''.join(data)}")
            return False
        return True
