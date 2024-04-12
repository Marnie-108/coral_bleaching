# Functions to test:

# Version 1

import csv
import json
import umpyutl as umpy

from pathlib import Path

SUBSTRINGS = (
    "and ",
    "and\n",
    "spp.",
    " spp.,",
    "spp. ",
    "spp",
    " spp,",
    "spp ",
    "sp.",
    " sp.,",
    "sp. ",
    "sp",
    " sp,",
    "sp ",
)

def build_str(string: str, key: str) -> str:
    """Builds a string based on the passed in string, lookup list and key name. If the field only contains a single taxon,
    the correct taxon name is assigned to string. If there are multiple taxons, the correct taxon names are appended to the
    string. This string of correct taxons is returned.

    Parameters:
        string (str): string of already corrected families from a single field (will be empty if none have been corrected yet)
        lookup (list): single dictionary within lookups which is a json with a dictionary for each family

    Returns:
        str: correct families from one field in the CORAL_FAMILY column
    """

    if len(string) == 0:
        string = key
    else:
        string += f", {key}"
    return string


def clean_data(string: str, substrings: tuple) -> list:
    """Prepares the data to enter other cleaning functions by delegating to remove_substr and
    remove_trailing character then stripping and titling each element to make sure the data is uniform
    and has no unnecessary extra data.

    Parameters:
        string (str): data from a single row of a single column
        substrings (tuple): tuple of substrings to be removed

    Returns:
        list: each individual value from the string of data made uniform and with any extra data removed
    """

    string = remove_substr(remove_trailing_char(string, ","), substrings)
    return [element.strip().title() for element in string.split(",")]

def clean_data2(string: str, substrings: tuple) -> list:
    """
    Cleans the data by removing trailing characters and substrings which are not germane to the
    analysis before returning a new list to the caller. Delegates to < remove_trailing_char > and
    < remove_substring > the task of removing trailing characters and substrings, respectively.

    Parameters:
        string (str): the data we may need to clean
        substrings (list): a list of words which need to be removed from the data

    Returns:
        list: the data (string) with the trailing character removed and any substrings removed
    """

    string = remove_trailing_char(string, ",")
    string = remove_substring(string, substrings)
    return [element.strip().title() for element in string.split(",")]

def lookup_family(families: list, lookups: list, new_string: str) -> str:
    """Loops over each family from a list of families from a single row of the "CORAL_FAMILY" column and
    delegates to match_family() to find the correct family in the classification then concatenates the correct
    family name to a string.

    Parameters:
        families (list): list of families from a single row of the "CORAL_FAMILY" column
        lookups (list): list of dictionaries, classfication of taxonomy

    Returns:
        str : string of concatenated and corrected family names
    """

    new_string = ""
    for family in families:
        family_string = match_family(lookups, family, new_string)
        if new_string:
            new_string += f", {family_string}"
        else:
            new_string = family_string
    return new_string


def lookup_genus(genera: list, lookups: list) -> tuple[str, list]:
    """Loops over each element from a list of species from a single row of the "CORAL_SPECIES" column and
    delegates to match_genus() to find the correct genus in the classification then concatenates the correct
    genus name to a string. It also utilises the design of the classification to find the family the genus
    belongs to and adds unique family names to a list - families.

    Parameters:
        genera (list): list of elements from a single row of the "CORAL_SPECIES" column
        lookups (list): list of dictionaries, classfication of taxonomy

    Returns:
        tuple: string of identified genera and list of their families.
    """

    families = set()
    for genus in genera:
        genus_string, genus_families = match_genus(
            lookups,
            genus,
            new_string,
        )
        if new_string:
            new_string += f", {genus_string}"
        else:
            new_string = genus_string

        if genus_families:
            families.update(genus_families)
    return new_string, list(families)


def lookup_species(species: list, lookups: list, new_string: str) -> tuple:
    """Loops over each element from a list of species from a single row of the "CORAL_SPECIES" column and
    delegates to match_species() to find the correct species in the classification then concatenates the correct
    species name to a string. It also utilises the design of the classification to find the family and genus the
    species belongs to and adds unique family and genera names to the lists families and genera.

    Parameters:
        species (list): list of species from a single row of the "CORAL_SPECIES" column
        lookups (list): list of dictionaries, classfication of taxonomy

    Returns:
        tuple: string of species names and two lists of associated genera and families respectively

    """

    new_string = ""
    for species_ in species:
        species_string = match_species(
            lookups,
            species_,
            new_string,
        )
        if new_string:
            new_string += f", {species_string}"
        else:
            new_string = species_string
    return new_string


def match_family(lookups: list, family: str, new_string: str) -> str:
    """Loops over lookups comparing family value to each correct family name within the classification
    and the typos associated with said family name. If the value matches either, the correct family name
    is returned.

    Parameters:
        lookups (list): list of dictionaries, classfication of taxonomy
        family (str): single family name from a single row of the "CORAL_FAMILY" column

    Returns:
        str: correct family name
    """

    for lookup in lookups:
        if family == lookup["family_name"]:
            print(f"family match: {family}")
            return build_str(new_string, lookup["family_name"])
        elif family in lookup["family_typos"]:
            print(f"family typo: {family}")
            return build_str(new_string, lookup["family_name"])
        else:
            continue
    return ""  # avoid returning None.


def match_genus(lookups: list, genus: str, new_string: str) -> tuple[str, list]:
    """Loops over lookups comparing genus value to each correct genus name within the classification
    and the typos associated with said genus name. If the value matches either, the correct genus name
    is returned. The family name of that 'lookup' is also added to a list of family names.

    Parameters:
        lookups (list): list of dictionaries, classfication of taxonomy
        genus (str): """
    for lookup in lookups:
        families = set()
        if lookup["genera"]:
            for gen in lookup["genera"]:
                if gen["genus_name"] in genus:
                    print(f"genus match: {genus}")
                    family = lookup["family_name"]
                    families.update(family)
                    return build_str(new_string, gen["genus_name"]), list(families)
                elif genus in gen["genus_typos"]:
                    print(f"genus typo: {genus}")
                    family = lookup["family_name"]
                    families.update(family)
                    return build_str(new_string, gen["genus_name"]), list(families)
                else:
                    continue
    return "", []  # avoid returning None.


def match_species(lookups: list, species: str, new_string: str) -> str:
    """TODO"""
    for lookup in lookups:
        if species == lookup["species_name"]:
            print(f"family match: {species}")
            return build_str(new_string, lookup, "species_name")
        elif species in lookup["family_typos"]:
            print(f"family typo: {species}")
            return build_str(new_string, lookup, "species_name")
        else:
            continue
    return ""  # avoid returning None.


def read_csv(filepath, encoding="utf-8", newline="", delimiter=","):
    """
    Reads a CSV file, parsing row values per the provided delimiter. Returns a list of lists,
    wherein each nested list represents a single row from the input file.

    WARN: If a byte order mark (BOM) is encountered at the beginning of the first line of decoded
    text, call < read_csv > and pass 'utf-8-sig' as the < encoding > argument.

    WARN: If newline='' is not specified, newlines '\n' or '\r\n' embedded inside quoted fields
    may not be interpreted correctly by the csv.reader.

    Parameters:
        filepath (str): The location of the file to read
        encoding (str): name of encoding used to decode the file
        newline (str): specifies replacement value for newline '\n'
                       or '\r\n' (Windows) character sequences
        delimiter (str): delimiter that separates the row values

    Returns:
        list: nested "row" lists
    """

    with open(filepath, "r", encoding=encoding, newline=newline) as file_obj:
        data = []
        reader = csv.reader(file_obj, delimiter=delimiter)
        for row in reader:
            data.append(row)
        return data


def read_json(filepath, encoding="utf-8"):
    """Reads a JSON document, decodes the file content, and returns a list or dictionary if
    provided with a valid filepath.

    Parameters:
        filepath (str): path to file
        encoding (str): name of encoding used to decode the file

    Returns:
        dict/list: dict or list representations of the decoded JSON document
    """

    with open(filepath, "r", encoding=encoding) as file_obj:
        return json.load(file_obj)


def remove_substr(string: str, substrings: tuple) -> str:
    """Removes words which are not relative to the data or get in the way of the analysis of data and
    returns the data (string) without those substrings.

    Parameters:
        string (str): the data we may need to remove a substring from
        substring (list): a list of words which need to be removed from the data

    Returns:
        str: the string with any substrings removed
    """

    org_len: int = len(string)
    for substring in substrings:
        string = string.replace(substring, "")
        if len(string) != org_len:
            return string
    return string

def remove_substring(string: str, substrings: tuple) -> str:
    """Removes substrings which are not germane to the analysis before returning a new string to the
    caller.

    Parameters:
        string (str): the data we may need to remove a substring from
        substring (list): a list of words which need to be removed from the data

    Returns:
        str: the string with any substrings removed
    """

    for substring in substrings:
        if substring == "and " or substring == "and\n":
            string = string.lower().replace(substring, ",")
        else:
            string = string.lower().replace(substring, "")
    return string

def remove_trailing_char(string: str, char: str) -> str:
    """Removes trailing characters from the end of a string and returns that string.

    Parameters:
        string (str): the data we may need to remove a trailing character from
        char (str): the character we want to remove from the end of the string

    Returns:
        str: the data (string) with the trailing character removed
    """

    return string[: len(string) - 1] if string[-1] == char else string


def write_csv(filepath, data, headers=None, encoding="utf-8", newline=""):
    """
    Writes data to a target CSV file. Column headers are written as the first
    row of the CSV file if optional headers are specified.

    WARN: If newline='' is not specified, newlines '\n' or '\r\n' embedded inside quoted
    fields may not be interpreted correctly by the csv.reader. On platforms that utilize
    `\r\n` an extra `\r` will be added.

    Parameters:
        filepath (str): path to target file (if file does not exist it will be created)
        data (list | tuple): sequence to be written to the target file
        headers (seq): optional header row list or tuple
        encoding (str): name of encoding used to encode the file
        newline (str): specifies replacement value for newline '\n'
                       or '\r\n' (Windows) character sequences

    Returns:
        None
    """

    with open(filepath, "w", encoding=encoding, newline=newline) as file_obj:
        writer = csv.writer(file_obj)
        if headers:
            writer.writerow(headers)
            for row in data:
                writer.writerow(row)
        else:
            writer.writerows(data)


def write_json(filepath, data, encoding="utf-8", ensure_ascii=False, indent=2):
    """Serializes object as JSON. Writes content to the provided filepath.

    Parameters:
        filepath (str): the path to the file
        data (dict)/(list): the data to be encoded as JSON and written to the file
        encoding (str): name of encoding used to encode the file
        ensure_ascii (str): if False non-ASCII characters are printed as is; otherwise
                            non-ASCII characters are escaped.
        indent (int): number of "pretty printed" indention spaces applied to encoded JSON

    Returns:
        None
    """

    with open(filepath, "w", encoding=encoding) as file_obj:
        json.dump(data, file_obj, ensure_ascii=ensure_ascii, indent=indent)


def main():
    """
    Program entry point. Orchestrates workflow. This is where I will test each funtion I have written
    using test values.

    Parameters:
        None

    Returns:
        None
    """
    # Testing build_string()
    # string = build_str()

    # Testing clean_data()

    test1 = clean_data2("Acropora sp., staghorn acropora, Acropora and pocilloporidae", SUBSTRINGS)
    # tests the functions ability to deal with multiple comma seperated values each with their own error
    test2 = clean_data2("acropora  ", SUBSTRINGS)
    # tests removing trailing space and title casing
    test3 = clean_data2("acropora  spp.", SUBSTRINGS)
    # tests removing substring, title casing and removing trailing space
    test4 = clean_data2("Acropora,", SUBSTRINGS)
    # tests removing trailing character

    print(f"{test1}\n{test2}\n{test3}\n{test4}")

    # Testing lookup_family()

    # Test data
    lookups = [
        {
            "family_name": "fam1",
            "family_typos": ["fams1, fam"],
            "genera": []
        },
        {
            "family_name": "fam2",
            "family_typos": ["fams2, famy"],
            "genera": []
        },
        {
            "family_name": "fam3",
            "family_typos": ["fams3, family3"],
            "genera": []
        }
                ]

    new_string = ""

    # # Tests
    # test5 = lookup_family(["fam1", "fam2", "fam3"], lookups, new_string)
    # # tests looking up the correct names
    # test6 = lookup_family(["fams", "famy", "fams3"], lookups, new_string)
    # # tests looking up all typos
    # test7 = lookup_family(["fam1", "fams2", "random"], lookups, new_string)
    # # tests looking up a correct name, a typo and a word not in the lookup

    # print(f"Test5: {test5}\nTest6: {test6}\nTest7: {test7}")



if __name__ == "__main__":
    main()