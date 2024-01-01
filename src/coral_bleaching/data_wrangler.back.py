import csv
import json
import umpyutl as umpy

from pathlib import Path


def build_str(string: str, lookup: list, key: str) -> str:
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
        string = lookup[key]
    else:
        string += f", {lookup[key]}"
    return string


def clean_data(string: str, substrings: tuple):
    """TODO"""

    string = remove_substr(remove_trailing_char(string, ","), substrings)
    return [element.strip().title() for element in string.split(",")]


def lookup_family(count: int, families: list, lookups: list, new_string: str) -> tuple[int, str]:
    """TODO"""

    new_count = count  # reset
    for family in families:
        new_string, new_count = match_family(lookups, family, new_string, new_count)
    return new_string, new_count


def lookup_genus(count: int, genera: list, lookups: list, new_string: str) -> tuple[int, str]:
    """TODO"""

    new_count = count  # reset
    for genus in genera:
        new_string, new_count = match_genus(lookups, genus, new_string, new_count)
    return new_string, new_count


def lookup_species(count: int, species: list, lookups: list, new_string: str) -> tuple[int, str]:
    """TODO"""

    new_count = count  # reset
    for species_ in species:
        new_string, new_count = match_species(lookups, species_, new_string, new_count)
    return new_string, new_count


def match_family(lookups: list, family: str, new_string: str, count: int) -> tuple[str, int]:
    """TODO"""
    for lookup in lookups:
        if family == lookup["family_name"]:
            print(f"family match: {family}")
            return build_str(new_string, lookup, "family_name"), count
        elif family in lookup["family_typos"]:
            print(f"family typo: {family}")
            return build_str(new_string, lookup, "family_name"), count + 1
        else:
            continue
    return "", count  # avoid returning None.


def match_genus(lookups: list, genus: str, new_string: str, count: int) -> tuple[str, int]:
    """TODO"""
    for lookup in lookups:
        if lookup["genera"]:
            for gen in lookup["genera"]:
                if gen["genus_name"] in genus:
                    print(f"genus match: {genus}")
                    return build_str(new_string, lookup, ["genera"]["genus_name"]), count
                elif genus in gen["genus_typos"]:
                    print(f"genus typo: {genus}")
                    return build_str(new_string, lookup, "genus_name"), count + 1
                else:
                    continue
    return "", count  # avoid returning None.


def match_species(lookups: list, species: str, new_string: str, count: int) -> tuple[str, int]:
    """TODO"""
    for lookup in lookups:
        if species == lookup["species_name"]:
            print(f"family match: {species}")
            return build_str(new_string, lookup, "species_name"), count
        elif species in lookup["family_typos"]:
            print(f"family typo: {species}")
            return build_str(new_string, lookup, "species_name"), count + 1
        else:
            continue
    return "", count  # avoid returning None.


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
    """Removes words which are not relative to the data or get in the way of the analysis of data and returns the data (string) without those substrings.

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

    substrings = ("And ", "And\n", "and ", "and\n")
    coral_family_idx = headers.index("CORAL_FAMILY")
    coral_genus_idx = headers.index("CORAL_SPECIES")
    count = 0
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
            val = lookup_family(count, families, lookups, new_string)
            new_string, count = val
            reefs[i][coral_family_idx] = new_string

        string = reefs[i][coral_genus_idx].strip()
        if string:
            # 'Pocillopora Sp', 'Montipora (Submasive Encrusting)', 'Fungiid (Fungia', 'Ctenactis Sandhalolita', 'Acropora (Maybe Grandis)', 'Pectinia', 'Diploastrea Heliopora', 'Echinopora', 'Galaxea'
            genera = clean_data(string, substrings)
            print(f"\ngenera: {genera}")

            # TODO need to move genus values to new genus element etc.

            new_string = ""
            val = lookup_genus(count, genera, lookups, new_string)
            new_string, count = val

    print(count)
    write_csv("./cleaned.csv", reefs, headers)


if __name__ == "__main__":
    main()
