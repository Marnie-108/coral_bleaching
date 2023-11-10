import csv
import json
import umpyutl as umpy

from pathlib import Path


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


def remove_substr(string: str, substrings: tuple) -> str:
    """TODO"""

    org_len: int = len(string)
    for substring in substrings:
        string = string.replace(substring, "")
        if len(string) != org_len:
            return string
    return string


def remove_trailing_char(string: str, char: str) -> str:
    """TODO"""

    return string[: len(string) - 1] if string[-1] == char else string


def build_str(string: str, lookup: list) -> str:
    """TODO"""

    if len(string) == 0:
        string = lookup["family"]
    else:
        string += f", {lookup['family']}"
    return string


def lookup_family(count: int, families: list, lookups: list, new_string: str) -> tuple[int, str]:
    """TODO"""

    new_count = 0
    new_string = ""

    for family in families:
        string, count = match_family(lookups, family, new_string, count)
        new_string += string
        new_count += count
        # if not val:
        #     # umpy.write.to_txt("bad_families.txt", [family])
        #     with open("bad_families.txt", "a") as file_obj:
        #         file_obj.write(f"{family}\n")
        # for lookup in lookups:
        # if family == lookup["family"]:
        #     print(f"family match: {family}")
        #     new_string = build_str(new_string, lookup)
        #     break
        # elif family in lookup["family_typos"]:
        #     print(f"family typo: {family}")
        #     count += 1  # count the number of family names corrected
        #     new_string = build_str(new_string, lookup)
        #     break
        # else:
        #     continue
    return new_string, new_count


def match_family(lookups: list, family: str, new_string: str, count: int) -> tuple[str, int]:
    """TODO"""
    for lookup in lookups:
        if family == lookup["family"]:
            print(f"family match: {family}")
            return build_str(new_string, lookup), count
        elif family in lookup["family_typos"]:
            print(f"family typo: {family}")
            return build_str(new_string, lookup), count + 1
        else:
            continue
    return "", 0  # avoid returning None.


def main():
    """TODO"""

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
    count = 0
    for i in range(len(reefs)):
        reef_id = reefs[i][0]
        print(f"\nReef id: {reef_id}")
        string = reefs[i][coral_family_idx].strip()
        if string:
            # 'Pocillopora Sp', 'Montipora (Submasive Encrusting)', 'Fungiid (Fungia', 'Ctenactis Sandhalolita', 'Acropora (Maybe Grandis)', 'Pectinia', 'Diploastrea Heliopora', 'Echinopora', 'Galaxea'
            string = remove_trailing_char(string, ",")
            string = remove_substr(string, substrings)
            # Convert first letter of each word to uppercase then split
            families = string.split(",")
            families = [family.strip().title() for family in families]
            print(f"\nfamilies: {families}")

            # TODO need to move genus values to new genus element etc.

            new_string = ""
            val = lookup_family(count, families, lookups, new_string)
            if isinstance(val, tuple):
                new_string, count = val
            else:
                new_string = ""
            reefs[i][coral_family_idx] = new_string

    print(count)
    write_csv("./cleaned.csv", reefs, headers)


if __name__ == "__main__":
    main()
