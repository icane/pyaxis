"""Integration tests for pyaxis module."""

from csv import QUOTE_NONNUMERIC

from pandas import Series

from pkg_resources import resource_filename

from pyaxis import pyaxis

import pytest

import requests


data_path = resource_filename('pyaxis', 'test/data/')


def test_uri_type():
    """uri_type() should be capable of discriminating files and URLs."""
    assert pyaxis.uri_type(
        'http://www.ine.es/jaxiT3/files/es/2184.px') == 'URL'


def test_read():
    """Check if a URL is loaded into a string variable."""
    pc_axis = pyaxis.read(
        'http://www.ine.es/jaxiT3/files/es/1001.px',
        'iso-8859-15')
    #assert len(pc_axis) >= 3445
    assert pc_axis.startswith('AXIS-VERSION="2006";')
    assert pc_axis.endswith('6.21 5.95;')


def test_metadata_extract():
    """Should extract pcaxis metadata into a list."""
    pc_axis = pyaxis.read(
        'https://www.ine.es/jaxi/files/_px/es/px/t20/e301/matri/a2000/l0/'
        '14001.px?nocab=1',
        'iso-8859-15')
    metadata_elements, raw_data = pyaxis.metadata_extract(pc_axis)
    assert type(metadata_elements) == list
    assert len(metadata_elements) == 23
    assert type(raw_data) == str
    assert len(raw_data) >= 40282


def test_metadata_split_to_dict():
    """Should split metadata into a dictionary."""
    pc_axis = pyaxis.read(
        'https://www.ine.es/jaxi/files/_px/es/px/t20/e301/matri/a2000/l0/'
        '14001.px?nocab=1',
        'iso-8859-15')
    metadata_elements, raw_data = pyaxis.metadata_extract(pc_axis)
    metadata = pyaxis.metadata_split_to_dict(metadata_elements)
    assert type(metadata) == dict
    assert len(metadata) == 23


def test_get_dimensions():
    """Should return two lists (dimension names and members)."""
    pc_axis = pyaxis.read(
        'https://www.ine.es/jaxi/files/_px/es/px/t20/e301/matri/a2000/l0/'
        '14001.px?nocab=1',
        'iso-8859-15')
    metadata_elements, raw_data = pyaxis.metadata_extract(pc_axis)
    metadata = pyaxis.metadata_split_to_dict(metadata_elements)
    dimension_names, dimension_members = pyaxis.get_dimensions(metadata)
    assert len(dimension_names) == 4
    assert dimension_names[0] == 'Comunidad Autónoma de residencia de los cónyuges'
    assert dimension_names[3] == 'Estado civil anterior de los cónyuges'
    assert len(dimension_members) == 4
    assert dimension_members[0][0] == 'Todas las comunidades'
    assert dimension_members[3][3] == 'Divorciados/as'


def test_build_dataframe():
    """Should return a dataframe with n+1 columns (dimensions + data)."""
    null_values=r'^"\."$'
    sd_values=r'"\.\."'
    pc_axis = pyaxis.read(
        'https://www.ine.es/jaxi/files/_px/es/px/t20/e301/matri/a2000/l0/'
        '14001.px?nocab=1',
        'iso-8859-15')
    metadata_elements, raw_data = pyaxis.metadata_extract(pc_axis)
    metadata = pyaxis.metadata_split_to_dict(metadata_elements)
    dimension_names, dimension_members = pyaxis.get_dimensions(metadata)
    data_values = Series(raw_data.split())
    df = pyaxis.build_dataframe(
        dimension_names,
        dimension_members,
        data_values,
        null_values=null_values,
        sd_values=sd_values)
    assert df.shape == (8064, 5)
    assert df['DATA'][7] == '10624.0'
    assert df['DATA'][159] == '534.0'


def test_parse():
    """Should parse a pc-axis into a dataframe and a metadata dictionary"""
    parsed_pcaxis = pyaxis.parse(
        'https://www.ine.es/jaxi/files/_px/es/px/t20/e301/matri/a2000/l0/'
        '14001.px?nocab=1',
        encoding='ISO-8859-15')
    assert parsed_pcaxis['DATA'].dtypes['DATA'] == 'object'
    assert len(parsed_pcaxis['DATA']) == 8064
    assert parsed_pcaxis['METADATA']
    ['VALUES(Comunidad Autónoma de residencia de los cónyuges)'][0][0] == \
        'Total'
    assert parsed_pcaxis['METADATA']
    ['VALUES(Comunidad Autónoma de residencia de los cónyuges)'][0][20] == \
        'Extranjero'


def test_http_error():
    """Using parse() with a non-existent URL should return a 404."""
    url = 'http://www.ine.es/jaxi'
    with pytest.raises(requests.exceptions.HTTPError):
        pyaxis.parse(url, encoding='windows-1252')


def test_connection_error():
    """Using parse() with a wrong URL should return a 404."""
    url = 'http://www.ine.es/jaxiT3/files/t/es/px/22284.px'

    with pytest.raises(requests.exceptions.HTTPError):
        pyaxis.parse(url, encoding='windows-1252')


if __name__ == '__main__':
    pytest.main()
