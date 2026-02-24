"""json_stat module converts px objects to JSON-Stat format.

This module implements the conversion of a dataframe and a
dictionary of metadata to a JSON object, following the specification
of JSON-Stat (https://json-stat.org/).

Example:
    import json
    from pyaxis import pyaxis, json_stat

    px = pyaxis.parse(self.base_path + 'px/2184.px', encoding='ISO-8859-2')
    json_obj = to_json_stat(px)
    json_str = json.dumps(json_obj)
    file = open('2184.json-stat', 'w')
    file.write(json_str)
    file.close()
"""

import json

from pyjstat import pyjstat


def to_json_stat(p_x):
    """Converts a parsed px object to JSON-Stat format.

    Args:
        p_x (dict): parsed px object

    Returns:
        json_obj (json): 
    """
    meta_keys = {
        'label': 'TITLE',
        'note': 'NOTE',
        'source': 'SOURCE'
    }

    id_vars = p_x['METADATA']['STUB']
    id_vars.extend(p_x['METADATA']['HEADING'])
    value_vars = ['DATA']
    d_f = p_x['DATA']
    d_f = d_f.melt(
        id_vars=id_vars,
        value_vars=value_vars,
        var_name='Variables')
    id_vars.append('Variables')
    d_f = d_f.sort_values(by=id_vars)
    dataset = pyjstat.Dataset.read(d_f)
    metric = {'metric': ['Variables']}
    dataset.setdefault('role', metric)
    json_str = dataset.write(output='jsonstat')
    json_obj = json.loads(json_str)

    for key in meta_keys:
        try:
            json_obj[key] = p_x['METADATA'][meta_keys[key]]
        except KeyError:
            continue

    try:
        json_obj['dimension']['Variables']['category']['unit'] = {
            'DATA': {
                'decimals': p_x['METADATA']['DECIMALS'],
                'label': p_x['METADATA']['UNITS']}
        }
    except KeyError:
        pass

    return json_obj
