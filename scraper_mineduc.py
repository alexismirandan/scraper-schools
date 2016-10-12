# -*- coding: utf-8 -*-
from lxml import html
import requests
from base import AbstractWebScrapingSchool


class ScraperMineduc(AbstractWebScrapingSchool):
    """ Scrapping class of schools from mineduc.cl"""

    name_file = 'mineduc2'
    base_url = 'http://www.mime.mineduc.cl/mime-web/mvc/mime/busqueda_avanzada'
    list_first_row_of_file = [
        'region_id', 'region', 'commune_id', 'commune',
        'name_school', 'mensualidad', 'dependencia'
    ]

    def get_schools(self, link, commune_id, region_id):
        """ Return schools of mineduc for an commune_id and region_id """
        data = {
            'com': commune_id,
            'comuna': commune_id,
            'dep': 0,
            'dependencia': 0,
            'esp': 0,
            'espec': 0,
            'especialidad': 0,
            'idMedia': 1,
            'nEspecial': 0,
            'nbas': 0,
            'nmed': 0,
            'npar': 0,
            'rbd1': None,
            'reg': region_id,
            'region': region_id,
            'sec': 0,
            'sectorEco': 0,
            'sep': 0,
            'tens': 0,
            'tipoEns': 0
        }
        page_schools = requests.post(link, data=data)
        tree_schools = html.fromstring(page_schools.content)
        schools = tree_schools.cssselect("#busqueda_avanzada tbody tr")
        return schools

    def get_list_data_school(self, school, region_id, region_name, commune_id, commune_name):
        """ Return data of school as list of mineduc """
        row_school = school.cssselect("td")
        name_school = row_school[1].cssselect("a")[0].text
        monthly_payment = row_school[2].text
        dependence = row_school[3].text
        return [
            region_id,
            region_name,
            commune_id,
            commune_name,
            name_school,
            monthly_payment,
            dependence
        ]

    def get_communes_by_regions(self):
        """ Return communes by regions of mineduc """
        return {
            1: [
                (1101, 'IQUIQUE'),
                (1107, 'ALTO HOSPICIO'),
                (1401, 'POZO ALMONTE'),
                (1402, 'CAMIÑA'),
                (1403, 'COLCHANE'),
                (1404, 'HUARA'),
                (1405, 'PICA'),
            ],
        }


if __name__ == '__main__':
    scraper_mineduc = ScraperMineduc()
    scraper_mineduc.run()
