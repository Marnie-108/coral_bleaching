import csv
import json
import umpyutl as umpy

from pathlib import Path


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
    """TODO"""
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


def match_genus(lookups: list, genus: str, new_string: str) -> tuple[str, str]:
    """TODO"""
    for lookup in lookups:
        families = []
        if lookup["genera"]:
            for gen in lookup["genera"]:
                if gen["genus_name"] in genus:
                    print(f"genus match: {genus}")
                    family = lookup["family_name"]
                    if family not in families:
                        families.append(family)
                    return build_str(new_string, gen["genus_name"]), families
                elif genus in gen["genus_typos"]:
                    print(f"genus typo: {genus}")
                    family = lookup["family_name"]
                    if family not in families:
                        families.append(family)
                    return build_str(new_string, gen["genus_name"]), families
                else:
                    continue
    return "", ""  # avoid returning None.


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
    Program entry point. Orchestrates workflow.

    Parameters:
        None

    Returns:
        None
    """

    # filepath = Path(__file__).parent.resolve().joinpath("coral_bleaching.csv")
    filepath = Path("coral_bleaching.csv").resolve()
    data = read_csv(filepath)
    headers = data[0]
    reefs = data[1:]

    filepath = Path("classification.json").resolve()
    lookups = read_json(filepath)
    # print(lookups[0])

    substrings = (
        "And ",
        "And\n",
        "and ",
        "and\n",
        "Spp.",
        " Spp.,",
        "Spp. ",
        "Spp",
        " Spp,",
        "Spp ",
        "Sp.",
        " Sp.,",
        "Sp. ",
        "Sp",
        " Sp,",
        "Sp ",
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
    # sp_strings = [
    #         "Spp.",
    #         " Spp.,",
    #         "Spp. ",
    #         "Spp",
    #         " Spp,",
    #         "Spp ",
    #         "Sp.",
    #         " Sp.,",
    #         "Sp. ",
    #         "Sp",
    #         " Sp,",
    #         "Sp ",
    #     ]
    coral_family_idx = headers.index("CORAL_FAMILY")
    coral_species_idx = headers.index("CORAL_SPECIES")
    for i in range(len(reefs)):
        reef_id = reefs[i][0]
        print(f"\nReef id: {reef_id}")
        string = reefs[i][coral_family_idx].strip()
        if string:
            # 'Pocillopora Sp', 'Montipora (Submasive Encrusting)', 'Fungiid (Fungia', 'Ctenactis Sandhalolita', 'Acropora (Maybe Grandis)', 'Pectinia', 'Diploastrea Heliopora', 'Echinopora', 'Galaxea'
            families = clean_data(string, substrings)
            print(f"\nfamilies: {families}")

            # TODO need to move genus values to new genus element etc.

            new_string = ""
            new_string = lookup_family(families, lookups, new_string)
            reefs[i][coral_family_idx] = new_string

        string = reefs[i][coral_species_idx].strip()
        if string:
            # 'Pocillopora Sp', 'Montipora (Submasive Encrusting)', 'Fungiid (Fungia', 'Ctenactis Sandhalolita', 'Acropora (Maybe Grandis)', 'Pectinia', 'Diploastrea Heliopora', 'Echinopora', 'Galaxea'
            species = clean_data(string, substrings)
            print(f"\ngenera: {species}")

            # TODO need to move genus values to new genus element etc.

            new_string = ""
            val = lookup_genus(species, lookups, new_string)
            new_string, genus_families = val
            print(f"\nnew_string = {new_string}")
            print(f"\ngenus_families = {genus_families}")
            reefs[i].insert(coral_species_idx, new_string)
            for genus_family in genus_families:
                if genus_family not in reefs[i][coral_family_idx]:
                    if reefs[i][coral_family_idx]:
                        reefs[i][coral_family_idx] += f", {genus_family}"
                    else:
                        reefs[i][coral_family_idx] += genus_family

            new_species_string = ""
            if new_string:
                genera = new_string.split(", ")
                for element in species:
                    if element not in genera:
                        if new_species_string:
                            new_species_string += f", {element}"
                        else:
                            new_species_string = element
                reefs[i][coral_species_idx + 1] = new_species_string

    headers.insert(coral_species_idx, "CORAL_GENUS")
    coral_species_idx += 1

    write_csv("./cleaned.csv", reefs, headers)


if __name__ == "__main__":
    main()
