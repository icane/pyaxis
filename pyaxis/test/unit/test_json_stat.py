"""Unit tests for json_stat module."""

from pkg_resources import resource_filename

from pyaxis import pyaxis, json_stat

import pytest


data_path = resource_filename('pyaxis', 'test/data/')

def test_to_json_stat():
    """Should generate a JSON-Stat object."""
    px = pyaxis.parse(
        data_path + '14001.px',
        encoding='ISO-8859-15')
    json_obj = json_stat.to_json_stat(px)
    assert json_obj['id'] == \
        ['Comunidad Autónoma de residencia del matrimonio',
         'edad de los cónyuges', 'sexo',
         'estado civil anterior de los cónyuges', 'Variables']
    assert json_obj['source'] == ['Instituto Nacional de Estadística']
    assert json_obj['value'][9] == '1'
    assert json_obj['value'][len(json_obj['value']) - 1] == '1600'
