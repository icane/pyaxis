=======
pyaxis
=======

**pyaxis** is a python library for **PC-Axis (or PX)** formatted data manipulation
which allows reading and writing PC-Axis [1]_ format with python, using the
DataFrame structures provided by the widely accepted pandas library [2]_.
PX is a standard format for statistical files used by a large number of
statistical offices. A package of software has been developed for this format: 
PX-Win, PX-Web and PX-Edit. **pyaxis** eases reading and parsing of PX files data 
and metadata into a pandas Dataframe and a dict structure, allowing their manipulation
in a tabular and pythonic manner.
**pyaxis** is provided under the Apache License 2.0.

.. [1] https://www.scb.se/px-en for PC-Axis information  
.. [2] http://pandas.pydata.org for Python Data Analysis Library information   

Installation
============

For installation::

    pip install pyaxis

Usage
=====

From PX to pandas DataFrame
-----------------------------------

Typical usage often looks like this::

    from pyaxis import pyaxis

    EXAMPLE_URL = 'http://www.ine.es/jaxiT3/files/t/es/px/2184.px'
    
    px = pyaxis.parse(EXAMPLE_URL, encoding=encoding='ISO-8859-2')
    print px['DATA']
    print px['METADATA']
