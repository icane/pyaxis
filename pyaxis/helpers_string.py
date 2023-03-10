"""Helpers_string: Helper Functions for Strings

This module contains all the necessary helper functions for processing the textual content of the PX file and its metadata. 

"""
import re 

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