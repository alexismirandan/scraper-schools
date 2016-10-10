# -*- coding: utf-8 -*-
from lxml import html
import requests
from scrapping_school_base import ScrappingSchoolsBase


class ScrappingSchoolsMineduc(ScrappingSchoolsBase):
    name_file = 'mineduc2'
    base_url = 'http://www.mime.mineduc.cl/mime-web/mvc/mime/busqueda_avanzada'

    def get_list_first_row_of_file(self):
        return ['region_id', 'region', 'commune_id', 'commune', 'name_school', 'mensualidad', 'dependencia']

    def get_schools(self, link, commune_id, num_region):
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
            'reg': num_region,
            'region': num_region,
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

    def get_regions(self):
        return {
            1: 'tarapacá',
            2: 'antofagasta',
            3: 'atacama',
            4: 'coquimbo',
            5: 'valparaíso',
            6: 'libertador bernardo ohiggins',
            7: 'maule',
            8: 'biobío',
            9: 'la araucanía',
            10: 'los lagos',
            11: 'aysén del general carlos ibañez del campo',
            12: 'magallanes y de la antártica chilena',
            13: 'metropolitana de santiago',
            14: 'los ríos',
            15: 'arica y parinacota'
        }


if __name__ == '__main__':
    s = ScrappingSchoolsMineduc()
    s.run()
