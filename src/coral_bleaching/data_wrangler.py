import csv
import json
import umpyutl as umpy

from pathlib import Path

def build_str(string: str, lookup: list, group: str) -> str:
    """Builds a string of corrected families for a field of the CORAL_FAMILY column. If the field only contains a single family, the correct family name is assigned to string. If there are multiple families, the correct family names are appended to the string. This string of correct families is returned.

    Parameters:
        string (str): string of already corrected families from a single field (will be empty if none have been corrected yet)
        lookup (list): single dictionary within lookups which is a json with a dictionary for each family

    Returns:
        str: correct families from one field in the CORAL_FAMILY column
    """

    if len(string) == 0:
        string = lookup[group]
    else:
        string += f", {lookup[group]}"
    return string

def clean_data(string: str, substrings: tuple):
    """TODO"""

    string = remove_substr(remove_trailing_char(string, ","), substrings)
    return [element.strip().title() for element in string.split(",")]

def create_genus(lookups: list, species, new_string: str, genus_count: int, group : str):
    for genus in species:
        for lookup in lookups:
            if f"{lookup['genus']} " in genus:
                genus_count += 1
                new_string, genus_count = build_str(new_string, lookup, group), genus_count
    return new_string, genus_count

def find_genus(string: str, sp_strings: list, genus: list) -> list:    #maybe belongs in jupyter notebook - single use
    """TODO"""

    string = (
        string.title().replace("And", ",").replace(";", ",").replace("\n", ",").replace("\t", ",")
    )
    string = [element.strip().title() for element in string.split(",")]
    print(f"\nSplit string: {string}")
    for element in string:
        if element:
            if " " not in element and element not in genus and element[1] != "." or "Species" in element:
                genus.append(element)
            for sp_string in sp_strings:
                # print(f"sp string: {sp_string}")
                if element[:-len(sp_string)] == sp_string:
                    element = remove_trailing_char(element.replace(sp_string, ""), ".").strip()
                    if element not in genus:
                        genus.append(element)
                    # print(f"\n{genus}")
                    break
    return genus

def lookup_taxon(count: int, taxa: list, lookups: list, new_string: str, group: str) -> tuple[int, str]:
    """TODO"""

    new_count = count  # reset
    for taxon in taxa:
        new_string, new_count = match_taxon(lookups, taxon, new_string, new_count, group)
    return new_string, new_count

def match_taxon(lookups: list, taxon: str, new_string: str, count: int, group: str) -> tuple[str, int]:
    """TODO"""
    for lookup in lookups:
        if taxon == lookup[group]:
            print(f"{group} match: {taxon}")
            return build_str(new_string, lookup, group), count
        elif taxon in lookup[f"{group}_typos"]:
            print(f"{group} typo: {taxon}")
            return build_str(new_string, lookup, group), count + 1
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
    genus = []
    coral_family_idx = headers.index("CORAL_FAMILY")
    coral_species_idx = headers.index("CORAL_SPECIES")
    count = 0
    genus_count = 0
    for i in range(len(reefs)):
        reef_id = reefs[i][0]
        # print(f"\nReef id: {reef_id}")
        string = reefs[i][coral_family_idx].strip()
        if string:
            # 'Pocillopora Sp', 'Montipora (Submasive Encrusting)', 'Fungiid (Fungia', 'Ctenactis Sandhalolita', 'Acropora (Maybe Grandis)', 'Pectinia', 'Diploastrea Heliopora', 'Echinopora', 'Galaxea'
            families = clean_data(string, substrings)
            species = clean_data(string, substrings)
            # print(f"\nfamilies: {families}")

            # TODO need to move genus values to new genus element etc.

            new_string = ""
            val = lookup_taxon(count, families, lookups, new_string, "family")
            new_string, count = val
            reefs[i][coral_family_idx] = new_string

        sp_strings = [
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
        ]
        string = reefs[i][coral_species_idx].strip()
        if string:
            genus = find_genus(string, sp_strings, genus)
            print(f"\nString: {string}")
    print(f"Genus: {sorted(genus)}")

    print(count)
    write_csv("./cleaned.csv", reefs, headers)

if __name__ == "__main__":
    main()
