# -*- coding: utf-8 -*-
from lxml import html
import requests
from base import AbstractWebScrapingSchool


class ScraperSchool(AbstractWebScrapingSchool):
    """ Base Webscraping for schools {name_page}"""

    name_file = ''
    base_url = ''
    list_first_row_of_file = [
        'region_id', 'region', 'commune_id', 'commune', 'name_school'
    ]

    def get_schools(self, link, commune_id, region_id):
        pass

    def get_list_data_school(self, school, region_id, region_name, commune_id, commune_name):
        pass

    def get_communes_by_regions(self):
        pass


if __name__ == '__main__':
    scraper = ScraperSchool()
    scraper.run()
