from pyaxis import pyaxis

EXAMPLE_URL = 'http://www.ine.es/jaxiT3/files/t/es/px/2184.px'
px = pyaxis.parse(EXAMPLE_URL, encoding='ISO-8859-2')
print(px['DATA'])
print(px['METADATA'])