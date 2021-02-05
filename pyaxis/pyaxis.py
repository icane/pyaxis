"""Pcaxis Parser module parses px files into dataframes.

This module obtains a pandas DataFrame of tabular data from a PC-Axis
file or URL. Reads data and metadata from PC-Axis [1]_ into a dataframe and
dictionary, and returns a dictionary containing both structures.

Example:
    from pyaxis import pyaxis

    px = pyaxis.parse(self.base_path + 'px/2184.px', encoding='ISO-8859-2')

.. [1] https://www.scb.se/en/services/statistical-programs-for-px-files/

..todo::

    meta_split: "NOTE" attribute can be multiple, but only the last one
    is added to the dictionary.

"""

import itertools
import logging
import re

from numpy import nan

from pandas import DataFrame, Series

import requests


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def uri_type(uri):
    """Determine the type of URI.

       Args:
         uri (str): pc-axis file name or URL
       Returns:
         uri_type_result (str): 'URL' | 'FILE'

    ..  Regex debugging:
        https://pythex.org/

    """
    uri_type_result = 'FILE'

    # django url validation regex:
    regex = re.compile(r'^(?:http|ftp)s?://'  # http:// or https://
                       # domain...
                       r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'
                       r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
                       r'localhost|'  # localhost...
                       r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
                       r'(?::\d+)?'  # optional port
                       r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if re.match(regex, uri):
        uri_type_result = 'URL'

    return uri_type_result


def read(uri, encoding, timeout=10):
    """Read a text file from file system or URL.

    Args:
        uri (str): file name or URL
        encoding (str): charset encoding
        timeout (int): request timeout; optional

    Returns:
        raw_pcaxis (str): file contents.

    """
    raw_pcaxis = ''

    if uri_type(uri) == 'URL':
        try:
            response = requests.get(uri, stream=True, timeout=timeout)
            response.raise_for_status()
            response.encoding = encoding
            raw_pcaxis = response.text
            response.close()
        except requests.exceptions.ConnectTimeout as connect_timeout:
            logger.error('ConnectionTimeout = %s', str(connect_timeout))
            raise
        except requests.exceptions.ConnectionError as connection_error:
            logger.error('ConnectionError = %s', str(connection_error))
            raise
        except requests.exceptions.HTTPError as http_error:
            logger.error('HTTPError = %s',
                         str(http_error.response.status_code) + ' ' +
                         http_error.response.reason)
            raise
        except requests.exceptions.InvalidURL as url_error:
            logger.error('URLError = ' + url_error.response.status_code + ' ' +
                         url_error.response.reason)
            raise
        except Exception:
            import traceback
            logger.error('Generic exception: %s', traceback.format_exc())
            raise
    else:  # file parsing
        file_object = open(uri, encoding=encoding)
        raw_pcaxis = file_object.read()
        file_object.close()

    return raw_pcaxis


def metadata_extract(pc_axis):
    r"""Extract metadata and data from pc-axis file contents.

    Args:
        pc_axis (str): pc_axis file contents.

    Returns:
        metadata_attributes (list of string): each item conforms to an\
                                              ATTRIBUTE=VALUES pattern.
        data (string): data values.

    """
    # replace new line characters with blank
    pc_axis = pc_axis.replace('\n', ' ').replace('\r', ' ')

    # split file into metadata and data sections
    metadata, data = pc_axis.split('DATA=')
    # meta: list of strings that conforms to pattern ATTRIBUTE=VALUES
    metadata_attributes = split_ignore_quotation_marks(metadata,';', final=True)
    #metadata_attributes = re.findall('([^=]+=[^=]+)(?:;|$)', metadata)

    # remove all semicolons
    data = data.replace(';', '')
    # remove trailing blanks
    data = data.strip()

    # 
    for i, item in enumerate(metadata_attributes):
        metadata_attributes[i] = item.strip().rstrip(';')

    return metadata_attributes, data


def split_ignore_quotation_marks(input, separator, final=False):
    """Split the input into a list avoiding quotation marks.

    Arg: 
        input (string): metadata element
        separator (string): character to split ('=')
        final (bool): if the separator is also the last character  

    Return:
        list: ['text1', 'text2', ...] 
    """
    quotation_mark_start = False
    quotation_mark_end = False
    result = []
    index_from = 0

    for index, element in enumerate(input):
        if element == '"' and not quotation_mark_start:
            quotation_mark_start = True
        elif element == '"' and quotation_mark_start:
            quotation_mark_end = False
            quotation_mark_start = False
        if element == separator and not quotation_mark_start:
            result.append(input[index_from:index])
            index_from = index + 1 
    if len(result) > 0:
        if final:
            return result
        else:
            result.append(input[index_from:index+1])
        return result
    return input


def metadata_split_to_dict(metadata_elements):
    """Split the list of metadata elements into a multi-valued keys dict.

    Args:
        metadata_elements (list of string): pairs ATTRIBUTE=VALUES

    Returns:
        metadata (dictionary): {'attribute1': ['value1', 'value2', ... ], ...}

    """
    metadata = {}

    for element in metadata_elements:
        name, values = split_ignore_quotation_marks(element, '=', final=False)
        name = name.replace('"', '')
        # remove leading and trailing blanks from element names
        name = name.replace('( ', '(')
        name = name.replace(' )', ')')
        # split values delimited by double quotes into list
        # additionally strip leading and trailing blanks
        metadata[name] = re.findall('"[ ]*(.+?)[ ]*"+?', values)
    return metadata


def get_dimensions(metadata):
    """Read STUB and HEADING values from metadata dictionary.

    Args:
        metadata: dictionary of metadata

    Returns:
        dimension_names (list)
        dimension_members (list)

    """
    dimension_names = []
    dimension_members = []

    # add STUB and HEADING elements to a list of dimension names
    # add VALUES of STUB and HEADING to a list of dimension members
    stubs = metadata['STUB']
    for stub in stubs:
        dimension_names.append(stub)
        stub_values = []
        raw_stub_values = metadata['VALUES(' + stub + ')']
        for value in raw_stub_values:
            stub_values.append(value)
        dimension_members.append(stub_values)

    # add HEADING values to the list of dimension members
    headings = metadata['HEADING']
    for heading in headings:
        dimension_names.append(heading)
        heading_values = []
        raw_heading_values = metadata['VALUES(' + heading + ')']
        for value in raw_heading_values:
            heading_values.append(value)
        dimension_members.append(heading_values)

    return dimension_names, dimension_members


def build_dataframe(dimension_names, dimension_members, data_values,
                    null_values, sd_values):
    """Build a dataframe from dimensions and data.

       Adds the cartesian product of dimension members plus the series of data.

    Args:
        dimension_names (list of string)
        dimension_members (list of string)
        data_values(Series): pandas series with the data values column.
        null_values(str): regex with the pattern for the null values in the px
                          file. Defaults to '.'.
        sd_values(str): regex with the pattern for the statistical disclosured
                        values in the px file. Defaults to '..'.
    Returns:
        df (pandas dataframe)

    """
    # cartesian product of dimension members
    dim_exploded = list(itertools.product(*dimension_members))

    df = DataFrame(data=dim_exploded, columns=dimension_names)

    # column of data values
    df['DATA'] = data_values
    # null values and statistical disclosure treatment
    df = df.replace({'DATA': {null_values: ''}}, regex=True)
    df = df.replace({'DATA': {sd_values: nan}}, regex=True)

    return df


def parse(uri, encoding, timeout=10,
          null_values=r'^"\."$', sd_values=r'"\.\."'):
    """Extract metadata and data sections from pc-axis.

    Args:
        uri (str): file name or URL
        encoding (str): charset encoding
        timeout (int): request timeout in seconds; optional
        null_values(str): regex with the pattern for the null values in the px
                          file. Defaults to '.'.
        sd_values(str): regex with the pattern for the statistical disclosured
                        values in the px file. Defaults to '..'.

    Returns:
         pc_axis_dict (dictionary): dictionary of metadata and pandas df.
                                    METADATA: dictionary of metadata
                                    DATA: pandas dataframe

    """
    # get file content or URL stream
    try:
        pc_axis = read(uri, encoding, timeout)
    except ValueError:
        import traceback
        logger.error('Generic exception: %s', traceback.format_exc())
        raise

    # metadata and data extraction and cleaning
    metadata_elements, raw_data = metadata_extract(pc_axis)

    # stores raw metadata into a dictionary
    metadata = metadata_split_to_dict(metadata_elements)

    # explode raw data into a Series of values, which can contain nullos or sd
    # (statistical disclosure)
    data_values = Series(raw_data.split())

    # extract dimension names and members from
    # 'meta_dict' STUB and HEADING keys
    dimension_names, dimension_members = get_dimensions(metadata)

    # build a dataframe
    df = build_dataframe(
        dimension_names,
        dimension_members,
        data_values,
        null_values=null_values,
        sd_values=sd_values)

    # dictionary of metadata and data (pandas dataframe)
    parsed_pc_axis = {
        'METADATA': metadata,
        'DATA': df
    }
    return parsed_pc_axis
