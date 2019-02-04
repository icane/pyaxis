"""Unit tests for pyaxis."""

import csv
import unittest
import requests
import numpy as np
from pyaxis import pyaxis


class TestPyaxis(unittest.TestCase):
    """Unit tests for pyaxis."""

    def setUp(self):
        """Set initialization variables."""
        self.base_path = './pyaxis/test/data/'

    def test_uri_type(self):
        """uri_type() should be capable of discriminating files and URLs."""
        self.assertEqual(pyaxis.uri_type('2184.px'), 'FILE',
                         'Uri type differs!')
        self.assertEqual(pyaxis.uri_type('http://www.ine.es/jaxiT3'
                                         '/files/t/es/px/2184.px'),
                         'URL', 'Uri type differs!')

    def test_metadata_extract_split(self):
        """Should extract pcaxis metadata into a list.

        Also, metadata_split_to_dict() should split those metadata into a
        dict.
        """
        pc_axis = """AXIS-VERSION="2006";
        CREATION-DATE="20170913";
        CHARSET="ANSI";
        SUBJECT-AREA="Indice de Precios de Consumo. Base 2016";
        SUBJECT-CODE="null";
        MATRIX="148";
        TITLE="Índices por comunidades autónomas: general y de grupos ECOICOP";
        CONTENTS="Índices";
        CODEPAGE="iso-8859-15";
        DESCRIPTION="";
        COPYRIGHT=YES;
        DECIMALS=1;
        SHOWDECIMALS=1;
        STUB="Comunidades y Ciudades Autónomas","Grupos ECOICOP";
        HEADING="Tipo de dato","Periodo";
        VALUES("Comunidades y Ciudades Autónomas")="Nacional","Andalucía",
        "Aragón","Asturias, Principado de","Balears, Illes","Canarias",
        "Cantabria","Castilla y León","Castilla - La Mancha","Cataluña",
        "Comunitat Valenciana","Extremadura","Galicia","Madrid, Comunidad de",
        "Murcia, Región de","Navarra, Comunidad Foral de","País Vasco",
        "Rioja, La","Ceuta","Melilla";VALUES("Grupos ECOICOP")=
        "00 Índice general","01 Alimentos y bebidas no alcohólicas",
        "02 Bebidas alcohólicas y tabaco","03 Vestido y calzado",
        "04 Vivienda, agua, electricidad, gas y otros combustibles",
        "05 Muebles, artículos del hogar y artículos para el mantenimiento
        corriente del hogar",
        "06 Sanidad","07 Transporte","08 Comunicaciones","09 Ocio y cultura",
        "10 Enseñanza",
        "11 Restaurantes y hoteles","12 Otros bienes y servicios ";
        VALUES("Tipo de dato")="Índice","Variación mensual","Variación anual",
        "Variación en lo que va de año";
        VALUES("Periodo")="2017M08","2017M07","2017M06","2017M05","2017M04",
        "2017M03","2017M02","2017M01",
        "2016M12","2016M11","2016M10","2016M09","2016M08","2016M07","2016M06",
        "2016M05","2016M04",
        "2016M03","2016M02","2016M01","2015M12","2015M11","2015M10","2015M09",
        "2015M08","2015M07",
        "2015M06","2015M05","2015M04","2015M03","2015M02","2015M01","2014M12",
        "2014M11","2014M10",
        "2014M09","2014M08","2014M07","2014M06","2014M05","2014M04","2014M03",
        "2014M02","2014M01",
        "2013M12","2013M11","2013M10","2013M09","2013M08","2013M07","2013M06",
        "2013M05","2013M04",
        "2013M03","2013M02","2013M01","2012M12","2012M11","2012M10","2012M09",
        "2012M08","2012M07",
        "2012M06","2012M05","2012M04","2012M03","2012M02","2012M01","2011M12",
        "2011M11","2011M10",
        "2011M09","2011M08","2011M07","2011M06","2011M05","2011M04","2011M03",
        "2011M02","2011M01",
        "2010M12","2010M11","2010M10","2010M09","2010M08","2010M07","2010M06",
        "2010M05","2010M04",
        "2010M03","2010M02","2010M01","2009M12","2009M11","2009M10","2009M09",
        "2009M08","2009M07",
        "2009M06","2009M05","2009M04","2009M03","2009M02","2009M01","2008M12",
        "2008M11","2008M10",
        "2008M09","2008M08","2008M07","2008M06","2008M05","2008M04","2008M03",
        "2008M02","2008M01",
        "2007M12","2007M11","2007M10","2007M09","2007M08","2007M07","2007M06",
        "2007M05","2007M04",
        "2007M03","2007M02","2007M01","2006M12","2006M11","2006M10","2006M09",
        "2006M08","2006M07",
        "2006M06","2006M05","2006M04","2006M03","2006M02","2006M01","2005M12",
        "2005M11","2005M10",
        "2005M09","2005M08","2005M07","2005M06","2005M05","2005M04","2005M03",
        "2005M02","2005M01",
        "2004M12","2004M11","2004M10","2004M09","2004M08","2004M07","2004M06",
        "2004M05","2004M04",
        "2004M03","2004M02","2004M01","2003M12","2003M11","2003M10","2003M09",
        "2003M08","2003M07",
        "2003M06","2003M05","2003M04","2003M03","2003M02","2003M01","2002M12",
        "2002M11","2002M10",
        "2002M09","2002M08","2002M07","2002M06","2002M05","2002M04","2002M03",
        "2002M02","2002M01";
        CODES("Comunidades y Ciudades Autónomas")="null","CA01","CA02","CA03",
        "CA04","CA05","CA06","CA07","CA08","CA09",
        "CA10","CA11","CA12","CA13",
        "CA14","CA15","CA16","CA17","CA18","CA19";
        MAP("Comunidades y Ciudades Autónomas")="spain_regions_img_ind";
        PRECISION("Tipo de dato","Índice")=3;
        UNITS="  Índice,   Tasas";
        SOURCE="Instituto Nacional de Estadística";
        DATA=
        101.553 101.351 102.055 102.011 102.073 101.101 101.122 101.488
        102.049 101.447
        """
        # we only need the first returned result
        metadata_elements = pyaxis.metadata_extract(pc_axis)[0]
        self.assertEqual(metadata_elements[13],
                         'STUB="Comunidades y Ciudades Autónomas",'
                         '"Grupos ECOICOP"', 'Metadata differs!')
        self.assertEqual(metadata_elements[14], 'HEADING="Tipo de dato",'
                         '"Periodo"', 'Metadata differs!')
        self.assertEqual(metadata_elements[22], 'UNITS="  Índice,   Tasas"',
                         'Metadata differs!')
        metadata = pyaxis.metadata_split_to_dict(metadata_elements)
        self.assertEqual(metadata['VALUES(Comunidades y Ciudades Autónomas)']
                         [2], 'Aragón', 'Metadata differs!')
        self.assertEqual(metadata['VALUES(Comunidades y Ciudades Autónomas)']
                         [4], 'Balears, Illes', 'Metadata differs!')

    def test_get_dimensions(self):
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
        self.assertEqual(dimension_names[0], 'Tipo de indicador',
                         'Dimension name differs!')
        self.assertEqual(dimension_names[1], 'Nivel educativo (agregado)',
                         'Dimension name differs!')
        self.assertEqual(dimension_members[0][0], 'Número de Centros',
                         'Dimension member differs!')
        self.assertEqual(dimension_members[0][1], 'Número de Alumnos',
                         'Dimension member differs!')

    def test_parse(self):
        """Should parse a pc-axis into a dataframe and a metadata dict."""
        parsed_pcaxis = pyaxis.parse(self.base_path + '2184.px',
                                     encoding='ISO-8859-2')
        self.assertEqual(parsed_pcaxis['DATA'].dtypes['DATA'], 'object')
        self.assertEqual(parsed_pcaxis['METADATA']
                         ['VALUES(Índices y tasas)'].index('Índice'),
                         0, 'Dictionary index differs!')
        self.assertGreater(len(parsed_pcaxis['DATA']), 9500)

    def test_statistical_disclosure(self):
        """Should parse a pc-axis with statistical disclosure into a dataframe.

        Uses convenient Na or NaN representations and a metadata dict.
        """
        parsed_pcaxis = pyaxis.parse(self.base_path + '27067.px',
                                     encoding='ISO-8859-2')
        self.assertEqual(parsed_pcaxis['DATA'].dtypes['DATA'], 'object')
        self.assertTrue(np.isnan(parsed_pcaxis['DATA']['DATA'].iloc[0]))
        self.assertEqual(parsed_pcaxis['DATA']['DATA'].iloc[804], '')

    def test_to_csv(self):
        """Returned data should be able to be converted to CSV format."""
        # fichero 1
        parsed_pcaxis = pyaxis.parse('http://www.ine.es/jaxiT3/'
                                     'files/es/2184.px',
                                     encoding='windows-1252')
        parsed_pcaxis['DATA'].to_csv(
            path_or_buf=self.base_path + '2184.csv',
            sep=',',
            header=True,
            index=False,
            doublequote=True,
            quoting=csv.QUOTE_NONNUMERIC,
            encoding='utf-8')
        test_file = open(self.base_path + '2184.csv', 'r')
        line = ''
        for line in test_file:
            pass
        last = line
        test_file.close()
        self.assertEqual(last, '"19 Melilla","Vivienda segunda mano",'
                         '"Variación en lo que va de año","2007T1",""\n')
        # fichero 2
        parsed_pcaxis = pyaxis.parse('http://www.ine.es/jaxiT3/'
                                     'files/es/1443.px',
                                     encoding='windows-1252')
        parsed_pcaxis['DATA'].to_csv(
            path_or_buf=self.base_path + '1443.csv',
            sep=',',
            header=True,
            index=False,
            doublequote=True,
            quoting=csv.QUOTE_NONNUMERIC,
            encoding='utf-8')
        test_file = open(self.base_path + '1443.csv', 'r')
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
        """Using parse() with a wrong URL should return a connect timeout."""
        # raises a timeout error
        url = 'http://www.ine.net/jaxiT3/files/t/es/px/1001.px'

        with self.assertRaises(requests.exceptions.ConnectTimeout):
            pyaxis.parse(url, encoding='windows-1252')


if __name__ == '__main__':
    unittest.main()
