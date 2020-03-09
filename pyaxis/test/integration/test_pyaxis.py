"""Integration tests for pyaxis module."""

from csv import QUOTE_NONNUMERIC

from pkg_resources import resource_filename

from pyaxis import pyaxis

import pytest

import requests


data_path = resource_filename('pyaxis', 'test/data/')


def test_to_csv():
    """Returned data should be able to be converted to CSV format."""
    parsed_pcaxis = pyaxis.parse(
        'http://www.ine.es/jaxiT3/files/es/2184.px',
        encoding='windows-1252')
    parsed_pcaxis['DATA'].to_csv(
        path_or_buf=data_path + '2184.csv',
        sep=',',
        header=True,
        index=False,
        doublequote=True,
        quoting=QUOTE_NONNUMERIC,
        encoding='utf-8')
    test_file = open(data_path + '2184.csv', 'r')
    line = ''
    for line in test_file:
        pass
    last = line
    test_file.close()
    assert last == \
    '"19 Melilla","Vivienda segunda mano","Variación en lo que va de año","2007T1",""\n'

    parsed_pcaxis = pyaxis.parse(
        'http://www.ine.es/jaxiT3/files/es/1443.px',
        encoding='windows-1252')
    parsed_pcaxis['DATA'].to_csv(
        path_or_buf=data_path + '1443.csv',
        sep=',',
        header=True,
        index=False,
        doublequote=True,
        quoting=QUOTE_NONNUMERIC,
        encoding='utf-8')
    test_file = open(data_path + '1443.csv', 'r')
    for line in test_file:
        pass
    last = line
    test_file.close()
    assert last == '"19 Melilla","Extranjera","1975",""\n'


def test_http_error():
    """Using parse() with a non-existent URL should return a 404."""
    url = 'http://www.ine.es/jaxi'
    with pytest.raises(requests.exceptions.HTTPError):
        pyaxis.parse(url, encoding='windows-1252')


def test_connection_error():
    """Using parse() with a wrong URL should return a 404."""
    url = 'http://www.ine.net/jaxiT3/files/t/es/px/1001.px'

    with pytest.raises(requests.exceptions.HTTPError):
        pyaxis.parse(url, encoding='windows-1252')


if __name__ == '__main__':
    unittest.main()
