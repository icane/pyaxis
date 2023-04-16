"""Helpers_string: Helper Functions for Strings

This module contains all the necessary helper functions for processing the textual content of the PX file and its metadata. 

"""
import re 
import itertools

def split_ignore_quotation_marks(string_input, separator, final=False):
    """Split the string_input into a list avoiding quotation marks.

    Arg:
        string_input (string): metadata element
        separator (string): character to split ('=')
        final (bool): if the separator is also the last character

    Return:
        list: ['text1', 'text2', ...]
    """
    quotation_mark_start = False
    result = []
    index_from = 0

    for index, element in enumerate(string_input):
        if element == '"' and not quotation_mark_start:
            quotation_mark_start = True
        elif element == '"' and quotation_mark_start:
            quotation_mark_start = False
        if element == separator and not quotation_mark_start:
            result.append(string_input[index_from:index])
            index_from = index + 1
    if len(result) > 0:
        if final:
            return result
        else:
            result.append(string_input[index_from:index+1])
        return result
    return string_input


def make_unique_list(list_duplicates):
    """Make a list from another list composed of unique elements
    Args:
        list_duplicates (list): list of elements with potential duplicates
    Returns:
        list: list of unique elements
    """
 # Small helper function to get unique elements of a list
    # initialize a null list
    unique_list = []
 
    for element in list_duplicates:
        # check if exists in unique_list or not
        if element not in unique_list:
            unique_list.append(element)
    return(unique_list)


def brackets_stripper(expression): 
    """Remove brackets and everything inside them from a string
    Args:
        expression (str): string to be processed
    Returns:
        str: string without brackets and everything inside them
    """
    pattern = r'\[.*?\]'
    expression = re.sub(pattern, '', expression)
    return(expression)


def parenthesis_extractor(input_string, extract_in=True):
    """Checks if there are parenthesis in the string and returns the substring within parenthesis.
    If there are no parenthesis, the string is returned unchanged.
    Parameters: 
    input_string: the string being checked for parenthesis
    extract_in: a boolean indicating if the extractor should return the content of the parenthesis or the name in front. The default is to return the name within parenthesis. 
    Returns:
    output_string: the string extracted or the initial string
    """
    #keep second chunk which was in the parenthesis
    #and keep from first character of the string to before last 
    #because the last character is the 2nd parenthesis
    if "(" in input_string:
        if extract_in:
            output_string = input_string.split("(")[-1][0:-1]
        else: 
            output_string = input_string.split("(")[0]
    else: 
        output_string = input_string
    return output_string

# For DICTIONARIES

def check_same_dict_value(dictionary): 
    """Checks if all the values in a dictionary are the same. 
    The check is also performed when the values of the dictionary are lists (list comparaison).
    This is done by checking if the length of unique values in the dictionary (its set) has a length equal to 1. 
    Parameters:
    dictionary: a dictionary where the values may all be the same
    Returns:
    bool_check_same: a boolean (True means all the values in the dictionary are the same. False meaning they are different.)
    """
    vals = list(dictionary.values())
    if isinstance(vals[1], list):
        #then we are dealing with a list of lists
        vals.sort()
        bool_check_same = len(list(item for item,_ in itertools.groupby(vals)))==1
    else:
        #then we are dealing with a list of strings
        bool_check_same = len(list(set(vals))) == 1
    return bool_check_same
