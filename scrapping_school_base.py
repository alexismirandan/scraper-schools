# -*- coding: utf-8 -*-
import abc
import xlsxwriter


class ScrapingSchoolBase(metaclass=abc.ABCMeta):
    """ Base scrapping for schools """

    def __init__(self):
        """ Initialize ScrappingSchools """
        self.encoding = None
        self.requests_obj = None
        self.workbook = xlsxwriter.Workbook('{0}.xlsx'.format(self.name_file))
        self.worksheet = self.workbook.add_worksheet('Colegios')

    def run(self):
        self.build_file_first_row()
        communes_by_region = self.get_communes_by_regions()
        dict_regions = self.get_regions()
        cnt_row = 1
        for region_id, dict_communes in communes_by_region.items():
            for commune_id, commune_name in dict_communes:
                schools = self.get_schools(
                    link=self.base_url,
                    commune_id=commune_id,
                    region_id=region_id
                )
                for school in schools:
                    list_data_school = self.get_list_data_school(
                        school=school,
                        region_id=region_id,
                        region_name=dict_regions[region_id],
                        commune_id=commune_id,
                        commune_name=commune_name
                    )
                    cnt_row += 1
                    for col, data in enumerate(list_data_school):
                        self.worksheet.write(cnt_row, col, data)
        self.close_file()

    @abc.abstractproperty
    def base_url(self):
        pass

    @abc.abstractproperty
    def name_file(self):
        pass

    @abc.abstractproperty
    def list_first_row_of_file(self):
        pass

    @abc.abstractmethod
    def get_schools(self):
        """ Return list of HtmlElement """
        pass

    @abc.abstractmethod
    def get_communes_by_regions(self):
        """
        Return dictionary of regions
        Excample:
            {1: [{'commune_value': 15101, 'commune_name': "Arica"}}, ...] ...}
        """
        pass

    @abc.abstractmethod
    def get_list_data_school(self, school, region_id, region_name, commune_id, commune_name):
        """
        Return list of data of the school:
            [region_id, name_region, commune_id, commune_name, name_school, monthly_payment, dependence]
        """
        pass

    def get_file_format_first_row(self):
        return self.workbook.add_format({'bold': True, 'font_size': 12})

    def build_file_first_row(self):
        for col, value in enumerate(self.list_first_row_of_file):
            self.worksheet.write(0, col, value, self.get_file_format_first_row())
            self.worksheet.set_column(col, col, 10)

    def close_file(self):
        self.workbook.close()

    def get_regions(self):
        """ Return regions """
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
            12: 'magallanes y la antártica chilena',
            13: 'metropolitana de santiago',
            14: 'los ríos',
            15: 'arica y parinacota'
        }
