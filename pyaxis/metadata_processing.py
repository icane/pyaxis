"""Metadata Processing: Shape the metadata

This module contains all the necessary functions to extract the metadata, 
format it, and handle a language choice if the metadata is multilingual.
"""

import re
from pyaxis.helpers_string import *

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
    metadata_attributes = split_ignore_quotation_marks(metadata,
                                                       ';', final=True)
    # metadata_attributes = re.findall('([^=]+=[^=]+)(?:;|$)', metadata)

    # remove all semicolons
    data = data.replace(';', '')
    # remove trailing blanks
    data = data.strip()

    for i, item in enumerate(metadata_attributes):
        metadata_attributes[i] = item.strip().rstrip(';')

    return metadata_attributes, data


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

        # avoid unexpected trailing blanks
        name = name.strip()
        name = name.replace('"', '')
        # remove leading and trailing blanks from element names
        name = name.replace('( ', '(')
        name = name.replace(' )', ')')
        # check if 'values' is delimited by double quotes
        pattern = re.compile('^[^"]*$')
        if pattern.match(values):
            metadata[name] = values
        else:
            # split values delimited by double quotes into list
            # additionally strip leading and trailing blanks
            metadata[name] = re.findall('"[ ]*(.+?)[ ]*"+?', values)
    return metadata

def multilingual_checker(metadata_dict): 
    """ Check if the PX file is multilingual
    Args:
        metadata_dict (dict): dictionary of metadata
    Returns:
        tuple: (translation, languages) where translation is a boolean and languages is a list of languages
    """
    # CHECK MULTILINGUAL
    if 'LANGUAGES' in metadata_dict.keys():
        print("Multilingual PX file")
        translation = True
        languages = metadata_dict["LANGUAGES"]
    else:
        translation = False
        languages = []
    return(translation, languages)

def language_presence_checker(languages, lang):
    """ Check if the language is present in the PX file
    Args:
        languages (list): list of languages in the PX file
        lang (str): language requested
    """
    try:
        lang in languages
    except ValueError:
        logger.error(
            'The language you are referring to is not present in the PX file. %s',
            traceback.format_exc())

def get_default_lang(metadata_dict, languages):
    """ Get the default language metadata and the default field names of the metadata
    Args:
        metadata_dict (dict): dictionary of metadata
        languages (list): list of languages in the PX file
    Returns:
        tuple: (lang_dict, default_multilingual_fields)
        where lang_dict is a dictionary of the metadata in the default language
        and default_multilingual_fields is a list of metadata field names in the default language
    """
    lang_dict = {}
    default_multilingual_fields = []
    #just remove all the metadata for other languages
    for key, value in metadata_dict.items():
        if any("["+l+"]" in key for l in languages):
            default_multilingual_fields.append(previous_key)
        else:
            lang_dict[key] = value
            previous_key = key
    #default_multilingual_fields = list(set(default_multilingual_fields))
    default_multilingual_fields = make_unique_list(default_multilingual_fields)
    return(lang_dict, default_multilingual_fields)

def metadata_dict_maker(metadata_dict, languages, lang):
    """Make a dictionary of metadata for the requested language
    Args:
        metadata_dict (dict): dictionary of metadata
        languages (list): list of languages in the PX file
        lang (str): language requested
    Returns:
        tuple: (lang_dict, default_multilingual_fields) 
        where lang_dict is a dictionary of the metadata in the requested language 
        and default_multilingual_fields is a list of metadata field names in the default language
    """
    # get the default lang_dict and the default field names
    default_lang_dict, default_multilingual_fields = get_default_lang(metadata_dict, languages)
    lang_dict = {}
    # Case: Language is not the default language
    if not lang == metadata_dict['LANGUAGE'][0]:
        #for value, key in enumerate(metadata_dict):
        for key, value in metadata_dict.items():
            #check if multilingual key
            if "["+lang+"]" in key:
                # remove the default language that has just been added
                del lang_dict[previous_key]
                # remove language info from key
                key = brackets_stripper(key)
                # Add the value only the language requested
                lang_dict[key] = value
            else: 
                # condition ensures we skip the keys tied to other languages
                if not any("["+l+"]" in key for l in languages):
                    # add the key common to all languages
                    lang_dict[key] = value
                    #store the key in case it is the default language which will have to be removed
                    previous_key = key
                if key=='LANGUAGE':
                    lang_dict[key] = [lang]
                if key=='LANGUAGES':
                    lang_dict[key] = languages

    else: 
        lang_dict = default_lang_dict
    return(lang_dict, default_multilingual_fields)

def translation_dict_maker(
        metadata_dict,
        default_multilingual_fields,
        languages,
        default_language,
        lang):
    """Make a dictionary of translations of the metadata, with the field 
        names in the requested language
    Args:
        metadata_dict (dict): dictionary of metadata
        default_multilingual_fields (list): list of metadata field names 
        in the default language
        languages (list): list of languages in the PX file
        default_language (str): default language of the PX file
        lang (str): language requested
    Returns:
            dict: dictionary of translations of the metadata, with the field
            names in the requested language
    """
    translation_dict = {}
    subset_languages = languages.copy()
    subset_languages.remove(default_language)
    list_all_keys = list(metadata_dict.keys())
    for default_key in default_multilingual_fields:
        field_dict = {}
        lang_keys = {}
        # Add default language
        field_dict[default_language] = metadata_dict[default_key]
        lang_keys[default_language] = default_key
        # Add each of the other languages
        default_index = list_all_keys.index(default_key)
        starting_index = default_index + 1
        for i, language in enumerate(subset_languages):
            lang_key = list_all_keys[starting_index + i]
            # save all language fields to decide later heading based on language desired
            lang_keys[language] = lang_key
            try:
                language in lang_key
            except ValueError:
                logger.error('The language fields in the metadata are not subsequent. \
                             The translation dictionary is invalid. %s', traceback.format_exc())
            field_dict[language] = metadata_dict[lang_key]
        # name the global field in the language requested by the user
         # remove language info from key
        key = brackets_stripper(lang_keys[lang])
        translation_dict[key] = field_dict
    return translation_dict

def multilingual_parse(metadata_dict, lang):
    """PX file parser for multilingual PX files
    Args:
        metadata_dict (dict): dictionary of metadata
        lang (str): language requested
    Returns:
            tuple: (lang_dict, translation_dict) 
            where lang_dict is a dictionary of the metadata in the requested language 
            and translation_dict is a dictionary of translations of the metadata, 
            with the field names in the requested language
    """
    # STEP 1: CHECK MULTILINGUAL
    translation, languages = multilingual_checker(metadata_dict)
    if translation is True:
        # if there are multiple languages and lang isn't set to a value
        # then we presume the user wants the default language
        default_language = metadata_dict['LANGUAGE'][0]
        if lang is None:
            lang = default_language
        # STEP 2 CHECK LANGUAGE IS AVAILABLE
        language_presence_checker(languages, lang)
        # STEP 3 DEFINE METADATA DICT CORRESPONDING TO LANGUAGE
        lang_dict, default_multilingual_fields = metadata_dict_maker(metadata_dict, languages, lang)
        # STEP 4 MAKE TRANSLATION DICTIONARY
        translation_dict = translation_dict_maker(metadata_dict, default_multilingual_fields,
                                                  languages, default_language, lang)
    else:
        # Single language px file
        lang_dict = metadata_dict
        translation_dict = {}
    return(lang_dict, translation_dict)
