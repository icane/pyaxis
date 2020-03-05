"""Integration tests for pyaxis class."""

import csv

import numpy as np

from pkg_resources import resource_filename

import requests

from pyaxis import pyaxis

import unittest


class TestPyaxis(unittest.TestCase):
    """Unit tests for pyaxis."""

    def setUp(self):
        """Set initialization variables."""
        self.data_path = resource_filename('pyaxis', 'test/data/')

    def test_uri_type(self):
        """uri_type() should be capable of discriminating files and URLs."""
        self.assertEqual(pyaxis.uri_type(
            'http://www.ine.es/jaxiT3/files/t/es/px/2184.px'),
            'URL',
            'Uri type differs!')

    def test_to_csv(self):
        """Returned data should be able to be converted to CSV format."""
        parsed_pcaxis = pyaxis.parse('http://www.ine.es/jaxiT3/'
                                     'files/es/2184.px',
                                     encoding='windows-1252')
        parsed_pcaxis['DATA'].to_csv(
            path_or_buf=self.data_path + '2184.csv',
            sep=',',
            header=True,
            index=False,
            doublequote=True,
            quoting=csv.QUOTE_NONNUMERIC,
            encoding='utf-8')
        test_file = open(self.data_path + '2184.csv', 'r')
        line = ''
        for line in test_file:
            pass
        last = line
        test_file.close()
        self.assertEqual(last, '"19 Melilla","Vivienda segunda mano",'
                         '"Variación en lo que va de año","2007T1",""\n')

        parsed_pcaxis = pyaxis.parse('http://www.ine.es/jaxiT3/'
                                     'files/es/1443.px',
                                     encoding='windows-1252')
        parsed_pcaxis['DATA'].to_csv(
            path_or_buf=self.data_path + '1443.csv',
            sep=',',
            header=True,
            index=False,
            doublequote=True,
            quoting=csv.QUOTE_NONNUMERIC,
            encoding='utf-8')
        test_file = open(self.data_path + '1443.csv', 'r')
        for line in test_file:
            pass
        last = line
        test_file.close()
        self.assertEqual(last, '"19 Melilla","Extranjera","1975",""\n')

    def test_http_error(self):
        """Using parse() with a non-existent URL should return a 404."""
        # returns status code 404
        url = 'http://www.ine.es/jaxi'
        with self.assertRaises(requests.exceptions.HTTPError):
            pyaxis.parse(url, encoding='windows-1252')

    def test_connection_error(self):
        """Using parse() with a wrong URL should return a 404."""
        url = 'http://www.ine.net/jaxiT3/files/t/es/px/1001.px'

        with self.assertRaises(requests.exceptions.HTTPError):
            pyaxis.parse(url, encoding='windows-1252')


if __name__ == '__main__':
    unittest.main()
