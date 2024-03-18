import pathlib as pl
import umpyutl as umpy

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


def build_string(string: str, substring: str) -> str:
    """Builds a new string by concatenating < string > and < substring > if the substring is not
    found in the string.

    Parameters:
        string (str): the string we want to concatenate
        substring (str): the string we want to concatenate to < string >

    Returns:
        str: the new string
    """

    if string:
        if substring not in string:
            return string + f", {substring}"
        else:
            return string
    else:
        return substring


def clean_data(string: str, substrings: tuple) -> list:
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


def get_family_name(lookup: dict, name: str) -> str | None:
    """TODO"""

    family_name = lookup.get("family_name")
    family_typos = lookup.get("family_typos")
    if (
        family_name and (family_name.lower() == name.lower() or family_name.lower() in name.lower())
    ) or (family_typos and name in family_typos):
        return family_name
    return None


def get_genus_name(lookup: dict, name: str) -> str | None:
    """Returns the genus name if found in the < lookup > dictionary, otherwise returns None.

    Parameters:
        lookup (dict): a dictionary containing genus names
        name (str): the name of the genus

    Returns:
        str: the genus name if found in < lookup >, otherwise None
    """

    for genus in lookup["genera"]:
        genus_name = genus.get("genus_name")
        genus_typos = genus.get("genus_typos")
        if (
            genus_name
            and (genus_name.lower() == name.lower() or genus_name.lower() in name.lower())
        ) or (genus_typos and name in genus_typos):
            return genus_name
    return None


def get_species_name(lookup: dict, name: str) -> str | None:
    """Returns the species name if found in the < lookup > dictionary, otherwise returns None.

    Parameters:
        lookup (dict): a dictionary containing species names
        name (str): the name of the species

    Returns:
        str: the species name if found in < lookup >, otherwise None
    """

    if lookup["genera"]:
        for genus in lookup["genera"]:
            genus_name = genus.get("genus_name")
            genus_species = genus["genus_species"]
            if genus_species:
                for species in genus_species:
                    species_name = species.get("species_name")
                    species_typos = species.get("species_typos")
                    if (
                        species_name
                        and (
                            species_name.lower() == name.lower()
                            or species_name.lower() in name.lower()
                        )
                    ) or (species_typos and name in species_typos):
                        return f"{genus_name} {species_name.split()[1].lower()}"
    return None


def lookup_families(data: list, lookups: list) -> str:
    """Returns a string of family names based on < data > and < lookups >.

    Parameters:
        data (list): a list of family names
        lookups (list): a list of dictionaries containing family names

    Returns:
        str: a string of family names
    """

    string = ""
    for element in data:
        for lookup in lookups:
            name = get_family_name(lookup, element)
            if name:
                string = build_string(string, name)
    return string


def lookup_genera(data: list, lookups: list) -> tuple[str, list]:
    """Returns a string of genus names and a list of familes based on < data > and < lookups >.

    Parameters:
        data (list): a list of genus names
        lookups (list): a list of dictionaries containing genus names

    Returns:
        tuple: two-item tuple comprising a string of genus names and list of families
    """

    string = ""
    families = []
    for element in data:
        for lookup in lookups:
            name = get_genus_name(lookup, element)
            if name:
                string = build_string(string, name)
                family = lookup["family_name"]
                if family and family not in families:
                    families.append(family)

    return string, families


def lookup_species(data: list, lookups: list) -> str:
    """Returns a string of species names based on < data > and < lookups >.

    Parameters:
        data (list): a list of species names
        lookups (list): a list of dictionaries containing species names

    Returns:
        str: a string of species names
    """

    string = ""
    for element in data:
        for lookup in lookups:
            name = get_species_name(lookup, element)
            if name:
                string = build_string(string, name)

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

    # org_len: int = len(string)
    for substring in substrings:
        string = string.lower().replace(substring, "")
        # if len(string) < org_len:
        #     return string
    return string


def remove_trailing_char(string: str, char: str) -> str:
    """Removes trailing characters from the end of a string before returning a new string to the
    caller.

    Parameters:
        string (str): the data we may need to remove a trailing character from
        char (str): the character we want to remove from the end of the string

    Returns:
        str: the data (string) with the trailing character removed
    """

    return string[: len(string) - 1] if string[-1] == char else string


def main():
    """
    Program entry point. Orchestrates workflow.

    Parameters:
        None

    Returns:
        None
    """

    # Read SORTED data file
    filepath = pl.Path("./coral_bleaching-sorted.csv").resolve()
    data = umpy.read.from_csv(filepath)
    headers = data[0]
    reefs = data[1:]

    # Read classification file
    filepath = pl.Path("./classification.json").resolve()
    lookups = umpy.read.from_json(filepath)

    # Column indexes
    coral_family_idx = headers.index("CORAL_FAMILY")
    coral_species_idx = headers.index("CORAL_SPECIES")

    for i in range(len(reefs)):
        # Family
        string = reefs[i][coral_family_idx].strip()
        if string:
            families = clean_data(string, SUBSTRINGS)
            reefs[i][coral_family_idx] = lookup_families(families, lookups)

        # Genera and species (derived from coral species value)
        string = reefs[i][coral_species_idx].strip()
        if string:
            species = clean_data(string, SUBSTRINGS)
            genera, genera_families = lookup_genera(species, lookups)

            reefs[i].insert(coral_species_idx, genera)

            if genera_families:
                for family in genera_families:
                    if family not in reefs[i][coral_family_idx]:
                        reefs[i][coral_family_idx] = build_string(
                            reefs[i][coral_family_idx], family
                        )

            reefs[i][coral_species_idx + 1] = lookup_species(species, lookups)

    # Add header
    headers.insert(coral_species_idx, "CORAL_GENUS")

    # Write to file
    umpy.write.to_csv("./coral_bleaching-cleaned.csv", reefs, headers)


if __name__ == "__main__":
    main()
