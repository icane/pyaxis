""" Example use case of pyaxis"""
from pyaxis import pyaxis

EXAMPLE_URL = 'http://www.ine.es/jaxiT3/files/t/es/px/2184.px'
parsed_px = pyaxis.parse(EXAMPLE_URL, encoding='ISO-8859-2')
print(parsed_px['DATA'])
print(parsed_px['METADATA'])
