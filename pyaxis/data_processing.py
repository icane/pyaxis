"""Data Processing: Make a dataframe 

This module contains all the necessary functions to extract the DATA field of the PX file and build the structure of the dataframe based on the metadata.
"""
import itertools
from numpy import nan, where
from pandas import DataFrame

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
    stubs = metadata.get('STUB', [])
    for stub in stubs:
        dimension_names.append(stub)
        stub_values = []
        raw_stub_values = metadata['VALUES(' + stub + ')']
        for value in raw_stub_values:
            stub_values.append(value)
        dimension_members.append(stub_values)

    # add HEADING values to the list of dimension members
    headings = metadata.get('HEADING', [])
    for heading in headings:
        dimension_names.append(heading)
        heading_values = []
        raw_heading_values = metadata['VALUES(' + heading + ')']
        for value in raw_heading_values:
            heading_values.append(value)
        dimension_members.append(heading_values)

    return dimension_names, dimension_members


def get_codes(metadata):
    """Read dimension codes and their dimension names from metadata dictionary.

    Args:
        metadata: dictionary of metadata

    Returns:
        dimensions_with_codes(list)
        dimension_codes(list)

    """
    dimensions_with_codes = []
    dimension_codes = []

    # add CODES of STUB to a list of dimension codes
    stubs = metadata.get('STUB', [])
    for stub in stubs:
        stub_values = []
        code_key = 'CODES(' + stub + ')'
        # Not all stubs necessarily have CODES
        if code_key in metadata:
            dimensions_with_codes.append(stub)
            raw_stub_values = metadata['CODES(' + stub + ')']
            for value in raw_stub_values:
                stub_values.append(value)
            dimension_codes.append(stub_values)

    # add HEADING values to the list of dimension codes
    headings = metadata.get('HEADING', [])
    for heading in headings:
        heading_values = []
        code_key = 'CODES(' + heading + ')'
        # Not all headings necessarily have CODES
        if code_key in metadata:
            dimensions_with_codes.append(heading)
            raw_heading_values = metadata['CODES(' + heading + ')']
            for value in raw_heading_values:
                heading_values.append(value)
            dimension_codes.append(heading_values)

    return dimensions_with_codes, dimension_codes

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

    # Create DataFrame from the exploded dimensions
    df = DataFrame(data=dim_exploded, columns=dimension_names)

    # Create a boolean mask for null and statistical disclosure values
    null_mask = data_values.str.match(null_values)
    sd_mask = data_values.str.match(sd_values)

    # Use np.where for efficient conditional assignment
    df['DATA'] = where(null_mask, '', data_values)
    df['DATA'] = where(sd_mask, nan, df['DATA'])

    return df
