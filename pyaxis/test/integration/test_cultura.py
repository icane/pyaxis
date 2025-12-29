"""Integration tests for remote site estadisticas.cultura.gob.es."""


from pkg_resources import resource_filename

from pyaxis import pyaxis

data_path = resource_filename('pyaxis', 'test/data/')


def test_parse_to_csv():
    """Should parse a pc-axis into a dataframe and save data to CSV format."""
    file_list = [
        '2004',
        '2003',
        '2005',
        '2037',
        '2020',
        '2006',
        '2007',
        '2016',
        '2017',
        '2018',
        '2019',
        '2021',
        '2022',
        '2023',
        '2024',
        '2025',
        '2027',
        '2009',
        '2008',
        '2012',
        '2010',
        '2011',
        '2013',
        '2014',
        '2015',
        '2029',
        '2030',
        '2038'
    ]

    for file in file_list:
        uri = 'https://estadisticas.cultura.gob.es/CulturaJaxiPx/files/_px/es/px/' + \
              't14/p14b/a2020/l0/T14B' + file + '.px?nocab=1'
        parsed_pcaxis = pyaxis.parse(uri, encoding='ISO-8859-1', timeout=10, verify=False)
        parsed_pcaxis['DATA'].to_csv(
            data_path + '0' + file + '.txt', sep='\t', encoding='utf-8', index=False)
