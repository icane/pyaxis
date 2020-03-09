"""Unit tests for pyaxis module."""

from csv import QUOTE_NONNUMERIC

from numpy import isnan

from pkg_resources import resource_filename

from pyaxis import pyaxis

import pytest


data_path = resource_filename('pyaxis', 'test/data/')


def test_uri_type():
    """uri_type() should be capable of discriminating files and URLs."""
    assert pyaxis.uri_type('2184.px') == 'FILE'
    assert pyaxis.uri_type(data_path + '2184.px') == 'FILE'
    assert pyaxis.uri_type(
        'http://www.ine.es/jaxiT3/files/es/2184.px') == 'URL'


def test_read():
    """Check if a file or URL is loaded into a string variable."""
    pc_axis = pyaxis.read(
        data_path + '01001.px',
        'iso-8859-15')
    assert len(pc_axis) == 1073
    assert pc_axis.startswith('AXIS-VERSION="2006";')
    assert pc_axis.endswith(' 16203.0;')


def test_metadata_extract():
    """Should extract pcaxis metadata into a list."""
    pc_axis = pyaxis.read(
        data_path + '27067.px',
        'iso-8859-15')
    metadata_elements, data = pyaxis.metadata_extract(pc_axis)
    assert type(metadata_elements) == list
    assert len(metadata_elements) == 25
    assert type(data) == str
    assert len(data) == 3890


def test_metadata_split_to_dict():
    """Should split metadata into a dictionary."""
    pc_axis = pyaxis.read(
        data_path + '27067.px',
        'iso-8859-15')
    metadata_elements, data = pyaxis.metadata_extract(pc_axis)
    metadata = pyaxis.metadata_split_to_dict(metadata_elements)
    assert type(metadata) == dict
    assert len(metadata) == 25


def test_get_dimensions():
    """Should return two lists (dimension names and members)."""
    pc_axis = """AXIS-VERSION="2006";
    CREATION-DATE="20170526";
    CHARSET="ANSI";
    SUBJECT-AREA="Encuesta de financiación y gastos de la enseñanza
    privada.
    Curso 2004-2005";
    SUBJECT-CODE="null";
    MATRIX="01001";
    TITLE="Principales resultados estructurales por Tipo de indicador y
    Nivel educativo (agregado)";
    CONTENTS="Principales resultados estructurales";
    CODEPAGE="iso-8859-15";
    DESCRIPTION="";
    COPYRIGHT=YES;
    DECIMALS=0;
    SHOWDECIMALS=0;
    STUB="Tipo de indicador";
    HEADING="Nivel educativo (agregado)";
    VALUES("Tipo de indicador")="Número de Centros","Número de Alumnos",
    "Personal remunerado con tareas docentes",
    "Personal remunerado con tareas no docentes",
    "Total de Personal Remunerado",
    "Total de Personal no Remunerado","Total de Personal";
    VALUES("Nivel educativo (agregado)")="TOTAL",
    "Educación no Universitaria","Educación Universitaria";
    UNITS="valores absolutos";
    SOURCE="Instituto Nacional de Estadística";
    DATA=
    6621.0 6477.0 144.0 2478366.0 2288630.0 189736.0 181347.0 170919.0
    10428.0 44702.0 39962.0 4740.0 225724.0 210556.0
    15168.0 6790.0 5949.0 841.0 232708.0 216505.0 16203.0;
    """
    metadata_elements = pyaxis.metadata_extract(pc_axis)[0]
    metadata = pyaxis.metadata_split_to_dict(metadata_elements)
    dimension_names, dimension_members = pyaxis.get_dimensions(metadata)
    assert dimension_names[0] == 'Tipo de indicador'
    assert dimension_names[1] == 'Nivel educativo (agregado)'
    assert dimension_members[0][0] == 'Número de Centros'
    assert dimension_members[0][1] == 'Número de Alumnos'


def test_parse():
    """Should parse a pc-axis into a dataframe and a metadata dict."""
    parsed_pcaxis = pyaxis.parse(
        data_path + '2184.px',
        encoding='ISO-8859-2')
    assert parsed_pcaxis['DATA'].dtypes['DATA'] == 'object'
    assert parsed_pcaxis['METADATA']['VALUES(Índices y tasas)'][0] == 'Índice'
    assert len(parsed_pcaxis['DATA']) == 9600

    parsed_pcaxis = pyaxis.parse(
        data_path + '14001.px',
        encoding='ISO-8859-2')
    assert parsed_pcaxis['DATA'].dtypes['DATA'] == 'object'
    assert parsed_pcaxis['METADATA']['VALUES(sexo)'][0] == 'Esposos'
    assert len(parsed_pcaxis['DATA']) == 8064

    parsed_pcaxis = pyaxis.parse(
        data_path + '01004.px',
        encoding='ISO-8859-15')
    assert parsed_pcaxis['DATA'].dtypes['DATA'] == 'object'
    assert parsed_pcaxis['METADATA']['VALUES(Masa corporal adulto)'][1] == \
        'Peso insuficiente (IMC <18,5 kg/m2)'
    assert parsed_pcaxis['METADATA']['VALUES(Masa corporal adulto)'][2] == \
        'Normopeso (18,5 kg/m2 <= IMC < 25 kg/m2)'
    assert len(parsed_pcaxis['DATA']) == 8064


def test_statistical_disclosure():
    """Should parse a pc-axis with statistical disclosure into a dataframe.

    Uses convenient Na or NaN representations and a metadata dict.
    """
    parsed_pcaxis = pyaxis.parse(
        data_path + '27067.px',
        encoding='ISO-8859-2')
    assert parsed_pcaxis['DATA'].dtypes['DATA'] == 'object'
    assert isnan(parsed_pcaxis['DATA']['DATA'].iloc[0])
    assert parsed_pcaxis['DATA']['DATA'].iloc[804] == ''


def test_to_csv():
    """Returned data should be able to be converted to CSV format."""
    parsed_pcaxis = pyaxis.parse(
        data_path + '2184.px',
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
    assert last == '"Melilla","Vivienda segunda mano",'
    '"Variación en lo que va de año","2007T1",""\n'


if __name__ == '__main__':
    pytest.main()
