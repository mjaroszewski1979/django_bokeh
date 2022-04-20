import json
import itertools
from django.core.management.base import BaseCommand
from django.conf import settings
from gdp.models import GDP

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        if not GDP.objects.count():
            data_file = settings.BASE_DIR / 'data' / 'gdp.json'
            with open(data_file, 'r') as f:
                data = json.load(f)
            data = itertools.dropwhile(lambda x: x['Country Name'] != 'Afghanistan', data)
            gdps = []
            for d in data:
                gdps.append(GDP(
                    country=d['Country Name'],
                    country_code = d['Country Code'],
                    year = d['Year'],
                    gdp = d['Value']
                ))
            GDP.objects.bulk_create(gdps)