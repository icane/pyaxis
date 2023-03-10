"""Unit tests for pyaxis module."""

from csv import QUOTE_NONNUMERIC

from numpy import isnan

from pandas import Series

from pkg_resources import resource_filename

from pyaxis import pyaxis
from pyaxis import helpers_string
from pyaxis import metadata_processing
from pyaxis import data_processing

import pytest


data_path = resource_filename('pyaxis', 'test/data/')


def test_uri_type():
    """uri_type() should be capable of discriminating files and URLs."""
    assert pyaxis.uri_type('2184.px') == 'FILE'
    assert pyaxis.uri_type(data_path + '2184.px') == 'FILE'


def test_read():
    """Check if a file loaded into a string variable."""
    pc_axis = pyaxis.read(
        data_path + '1001.px',
        'iso-8859-15')
    assert len(pc_axis) == 3473
    assert pc_axis.startswith('AXIS-VERSION="2006";')
    assert pc_axis.endswith('6.21 5.95;')


def test_metadata_extract():
    """Should extract pcaxis metadata into a list."""
    pc_axis = pyaxis.read(
        data_path + '14001.px',
        'iso-8859-15')
    metadata_elements, raw_data = metadata_processing.metadata_extract(pc_axis)
    assert type(metadata_elements) == list
    assert len(metadata_elements) == 28
    assert type(raw_data) == str
    assert len(raw_data) == 29441


def test_metadata_split_to_dict():
    """Should split metadata into a dictionary."""
    pc_axis = pyaxis.read(
        data_path + '14001.px',
        'iso-8859-15')
    metadata_elements, raw_data = metadata_processing.metadata_extract(pc_axis)
    metadata = metadata_processing.metadata_split_to_dict(metadata_elements)
    assert type(metadata) == dict
    assert len(metadata) == 28


def test_metadata_split_dict_quotation_marks():
    """Should ignore character split if it is between quotation marks."""
    metadata_elements = ['VALUES("estrato de empleo")="Total",">=10 empleados";']
    metadata = metadata_processing.metadata_split_to_dict(metadata_elements)
    assert type(metadata) == dict
    assert metadata['VALUES(estrato de empleo)'] == ['Total', '>=10 empleados']


def test_split_ignore_quotation_marks():
    """Should ignore the separator if it is between doble quotation marks,
    simple quotation mark is ignored as quotation mark"""
    text = 'SURVEY[fr]="Statistique du mouvement naturel de la population (BEVNAT), '\
           +"Statistique de l'état"+'annuel"  " de la population (1981-2010) (ESPOP),\
            Statistique de la population et des ménages (STATPOP)";  SURVEY[it]="Stat\
            istica del movimento naturale della popolazione"+"(BEVNAT), Statistica de\
            llo stato ann"  "uale della popolazione (1981-2010) (ESPOP), Statistica d\
            ella popolazione e delle economie domestich"  "e (STATPOP);";  SURVEY[en]=\
            "Vital statistics (BEVNAT), Annual Population Statistics (1981-2010) (ESP\
            OP), Population "  "and Households Statistics (STATPOP)";'
    result = helpers_string.split_ignore_quotation_marks(text,';', final=True)
    assert type(result) == list
    assert len(result) == 3


def test_get_dimensions():
    """Should return two lists (dimension names and members)."""
    pc_axis = pyaxis.read(
        data_path + '14001.px',
        'iso-8859-15')
    metadata_elements, raw_data = pyaxis.metadata_extract(pc_axis)
    metadata = pyaxis.metadata_split_to_dict(metadata_elements)
    dimension_names, dimension_members = pyaxis.get_dimensions(metadata)
    assert len(dimension_names) == 4
    assert dimension_names[0] == 'Comunidad Autónoma de residencia del matrimonio'
    assert dimension_names[3] == 'estado civil anterior de los cónyuges'
    assert len(dimension_members) == 4
    assert dimension_members[0][0] == 'Total'
    assert dimension_members[3][3] == 'Divorciados/as'


def test_get_codes():
    """Should return two lists (dimension names with codes and codes)."""
    pc_axis = pyaxis.read(
        data_path + '14001.px',
        'iso-8859-15')
    metadata_elements, raw_data = pyaxis.metadata_extract(pc_axis)
    metadata = pyaxis.metadata_split_to_dict(metadata_elements)
    dimensions_with_codes, dimension_codes = data_processing.get_codes(metadata)
    assert len(dimension_codes) == 1
    assert len(dimensions_with_codes) == 1
    assert dimensions_with_codes[0] == 'Comunidad Autónoma de residencia del matrimonio'
    assert dimension_codes[0][6] == 'CA06'
    assert dimension_codes[0][11] == 'CA11'

    
def test_build_dataframe():
    """Should return a dataframe with n+1 columns (dimensions + data)."""
    null_values=r'^"\."$'
    sd_values=r'"\.\."'
    pc_axis = pyaxis.read(
        data_path + '14001.px',
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
    assert df['DATA'][7] == '28138'
    assert df['DATA'][159] == '422'

def test_make_unique_list():
    """make unique list should return a list without duplicates"""
    mylist = ["a", "b", "t", "a"]
    mylist = helpers_string.make_unique_list(mylist)
    assert len(mylist) == len(set(mylist))

def test_brackets_stripper():
    """brackets_stripper should strip a string from brackets and their content"""
    mystring = "This is a string [with brackets]"
    mystring = helpers_string.brackets_stripper(mystring)
    assert mystring == "This is a string "

def test_multilingual_checker():
    """multilingual_checker should return a tuple with a boolean for translation and a list of languages"""
    px= data_path + "px-x-0602000000_107.px"
    pc_axis = pyaxis.read(px, encoding='ISO-8859-2', timeout=10)
    metadata, raw_data = metadata_processing.metadata_extract(pc_axis)
    metadata_dict = metadata_processing.metadata_split_to_dict(metadata)
    translation, languages = metadata_processing.multilingual_checker(metadata_dict)
    assert translation == True
    assert languages == ["de","fr","it","en"]

def test_get_default_lang():
    """get_default_lang should return a metadata dictionary in the default language and a list of metadata fields in the default language"""
    px= data_path + "px-x-0602000000_107.px"
    pc_axis = pyaxis.read(px, encoding='ISO-8859-2', timeout=10)
    metadata, raw_data = pyaxis.metadata_extract(pc_axis)
    metadata_dict = pyaxis.metadata_split_to_dict(metadata)
    languages = metadata_dict['LANGUAGES']
    lang_dict, default_multilingual_fields = metadata_processing.get_default_lang(metadata_dict, languages)
    assert lang_dict['LANGUAGE'] == ['de']
    assert type(default_multilingual_fields) == list
    assert 'VALUES(Ausbildungsniveau)' in default_multilingual_fields

def test_metadata_dict_maker():
    """metadata_dict_maker should return a dictionary of metadata fields in the requested language and a list of metadata fields in the default language"""
    px= data_path + "px-x-0602000000_107.px"
    pc_axis = pyaxis.read(px, encoding='ISO-8859-2', timeout=10)
    metadata, raw_data = pyaxis.metadata_extract(pc_axis)
    metadata_dict = pyaxis.metadata_split_to_dict(metadata)
    languages = metadata_dict['LANGUAGES']
    lang = "it"
    lang_dict, default_multilingual_fields = metadata_processing.metadata_dict_maker(metadata_dict, languages, lang)
    assert lang_dict['LANGUAGE'] == ['it']
    assert type(default_multilingual_fields) == list
    assert 'VALUES(Ausbildungsniveau)' in default_multilingual_fields

def test_translation_dict_maker(): 
    """translation_dict_maker should return a dictionary of translations of the metadata, with the field names in the requested language"""
    px= data_path + "px-x-0602000000_107.px"
    pc_axis = pyaxis.read(px, encoding='ISO-8859-2', timeout=10)
    metadata, raw_data = pyaxis.metadata_extract(pc_axis)
    metadata_dict = pyaxis.metadata_split_to_dict(metadata)
    languages = metadata_dict['LANGUAGES']
    print(metadata_dict['VALUES(Wirtschaftsabteilung)'])
    lang = "it"
    default_language = metadata_dict['LANGUAGE'][0]
    _, default_multilingual_fields = metadata_processing.metadata_dict_maker(metadata_dict, languages, lang)
    translation_dict = metadata_processing.translation_dict_maker(metadata_dict, default_multilingual_fields, languages, default_language, lang)
    assert type(translation_dict) == dict
    assert 'VALUES(Livello di formazione)' in translation_dict
    assert translation_dict['VALUES(Livello di formazione)'] == {
                                                                 'de': ['Hochschulabsolventen', 'Höhere Berufsbildung', 'Berufslehre', 'Obligatorische Schulbildung'],
                                                                 'fr': ['Haute école', 'Professionnelle supérieure', 'Apprentissage', 'Ecole obligatoire'],
                                                                 'it': ['Scuola Universitaria', 'Professionale Superiore', 'Apprendistato', "Scuola dell'obligo"], 
                                                                 'en': ['University degree', 'Higher professional education', 'Apprenticeship', 'Compulsory education']}



def test_multilingual_parse():
    """multilingual_parse should return a tuple with a dictionary of metadata fields in the requested language 
    and a dictionary of translations of the metadata, with the field names in the requested language"""
    px= data_path + "px-x-0602000000_107.px"
    pc_axis = pyaxis.read(px, encoding='ISO-8859-2', timeout=10)
    metadata, raw_data = metadata_processing.metadata_extract(pc_axis)
    metadata_dict = metadata_processing.metadata_split_to_dict(metadata)
    lang = "it"
    lang_dict, translation_dict = metadata_processing.multilingual_parse(metadata_dict, lang)
    assert type(translation_dict) == dict
    assert type(lang_dict) == dict


def test_parse():
    """Should parse a pc-axis into a dataframe and a metadata dictionary"""
    parsed_pcaxis = pyaxis.parse(
        data_path + '14001.px',
        encoding='ISO-8859-15')
    assert parsed_pcaxis['DATA'].dtypes['DATA'] == 'object'
    assert len(parsed_pcaxis['DATA']) == 8064
    assert parsed_pcaxis['METADATA']
    ['VALUES(Comunidad Autónoma de residencia del matrimonio)'][0][0] == \
        'Total'
    assert parsed_pcaxis['METADATA']
    ['VALUES(Comunidad Autónoma de residencia del matrimonio)'][0][20] == \
        'Extranjero'


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


if __name__ == '__main__':
    pytest.main()
