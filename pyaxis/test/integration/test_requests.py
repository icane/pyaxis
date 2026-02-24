"""Integration tests for certificate verification and use of headers."""

import os.path

from pkg_resources import resource_filename

from pyaxis import pyaxis


data_path = resource_filename('pyaxis', 'test/data/')


def test_parse_not_verify():
    """Should parse a pc-axis without verifying the certificate."""

    headers = {'User-agent':'Pyaxis 0.4.3'}
    uri = 'https://estadisticas.cultura.gob.es/CulturaJaxiPx/files/_px/es/px/' + \
            't14/p14b/a2020/l0/T14B2004.px?nocab=1'
    parsed_pcaxis = pyaxis.parse(
        uri, encoding='ISO-8859-1', timeout=10, verify=False, headers=headers)
    parsed_pcaxis['DATA'].to_csv(
        data_path + '2004.txt', sep='\t', encoding='utf-8', index=False)
    assert os.path.isfile(data_path + '2004.txt')


def test_parse_verify_1():
    """Should parse a pc-axis verifying the certificate."""

    headers = {'User-agent':'Pyaxis 0.4.3'}
    cert_file = data_path + "cert/_.cultura.gob.es.crt"

    uri = 'https://estadisticas.cultura.gob.es/CulturaJaxiPx/files/_px/es/px/' + \
            't14/p14b/a2020/l0/T14B2005.px?nocab=1'
    parsed_pcaxis = pyaxis.parse(
        uri, encoding='ISO-8859-1', timeout=10, verify=cert_file, headers=headers)
    parsed_pcaxis['DATA'].to_csv(
        data_path + '2005.txt', sep='\t', encoding='utf-8', index=False)
    assert os.path.isfile(data_path + '2005.txt')

def test_parse_verify_2():
    """Should parse a pc-axis verifying the certificate."""

    headers = {'User-agent':'Pyaxis 0.4.3'}
    cert_file = data_path + "cert/_.inclusion.gob.es.crt"

    uri = 'https://expinterweb.inclusion.gob.es/jaxiPx/files/_px/es/px/' + \
            'Stock/l0/AT_NA_SX_GE_TIP_MOT.px?nocab=1'
    parsed_pcaxis = pyaxis.parse(
        uri, encoding='ISO-8859-1', timeout=10, verify=cert_file, headers=headers)
    parsed_pcaxis['DATA'].to_csv(
        data_path + 'AT_NA_SX_GE_TIP_MOT.txt', sep='\t', encoding='utf-8', index=False)
    assert os.path.isfile(data_path + 'AT_NA_SX_GE_TIP_MOT.txt')
