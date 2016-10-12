# -*- coding: utf-8 -*-
from lxml import html
import requests
from base import AbstractWebScrapingSchool


def get_region_number(region_href):
    text_without_html = region_href.replace('.html', '')
    pos_last = text_without_html.rfind('-')
    return int(text_without_html[pos_last+1::])


class ScrapingSchoolZonacolegios(AbstractWebScrapingSchool):
    """ Scrapping class of schools from zonacolegios.ipower.com """

    name_file = 'zonacolegios'
    base_url = 'http://zonacolegios.ipower.com/colegios-de-chile/'
    list_first_row_of_file = [
        'region_id', 'region', 'commune_id', 'commune',
        'name_school', 'mensualidad', 'dependencia'
    ]

    def get_schools(self, link, commune_id, region_id):
        """ Return schools of zonacolegios for an commune_id and region_id """
        print("get_schools: commune_id={0} region_id={1}".format(commune_id, region_id))
        url = self.base_url + commune_id
        requests_school = requests.get(url)
        if requests_school.ok:
            tree_schools = html.fromstring(requests_school.content)
            schools = tree_schools.cssselect('table')[2].cssselect('td[height="17"]')[1::]
            return schools
        print('Requests School is not ok status_code:{0} url:{1}'.format(
            requests_school.status_code, url
        ))
        return []

    def get_list_data_school(self, school, region_id, region_name, commune_id, commune_name):
        """ Return data of school as list of zonacolegios """
        name_school = school.text
        commune_key = commune_id.replace('.html', '').replace('comunas/colegios-de-', '')
        print(name_school)
        return [
            region_id,
            region_name,
            commune_key,
            commune_name,
            name_school,
            '',
            ''
        ]

    def get_communes_by_regions(self):
        """ Return communes by regions of zonacolegios """
        page_regions = requests.get(self.base_url + 'colegios-zona.html')
        tree_regions = html.fromstring(page_regions.content)
        regions = tree_regions.cssselect('table td tr a')
        dict_regions = map(
            lambda region: (
                get_region_number(region.get('href', None)),
                self.get_list_communes_by_region(region)
            ),
            regions
        )
        return dict(dict_regions)

    def get_list_communes_by_region(self, region):
        """ Return list of communes by region """
        region_href = region.get('href', None)
        region_number = get_region_number(region_href)
        # get communes
        page_communes = requests.get(self.base_url + region_href)
        tree_communes = html.fromstring(page_communes.content)
        communes = tree_communes.cssselect('table td tr a')
        list_communes = [
            (commune.get('href', None), commune.text)
            for commune in communes
        ]
        return list_communes


if __name__ == '__main__':
    scraping_zonacolegios = ScrapingSchoolZonacolegios()
    scraping_zonacolegios.run()
