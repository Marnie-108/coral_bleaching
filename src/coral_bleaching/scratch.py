import pandas as pd
import csv
import json
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


filepath = Path("coral_bleaching.csv").resolve()
data = read_csv(filepath)

filepath = Path("classification.json").resolve()
lookups = read_json(filepath)
# print(data["CORAL_FAMILY"])
# families = data["CORAL_FAMILY"].tolist()
# for i in families:
#     if i == None:
#         break
#     for j in classification:
#         if j["family"] == i:
#             print("Correct")
#         elif i in j["family_typos"]:
#             print("Typo")
#         elif i in j["genus"] or i in j["species"] or i in j["species_typos"]:
#             print("Misinformation")

# complete = []

# genus = [
#     "Pocillopora",
#     "Palythoa",
#     "Montastrea",
#     "Montipora",
#     "Hydnophora",
#     "Echinopora",
#     "Porites",
#     "Platygyra",
#     "Galaxea",
#     "Goniopora",
#     "Astreopora",
#     "Acropora",
#     "Favites",
#     "Goniastrea",
#     "Stylophora",
#     "Pavona.",
#     "Favia",
#     "Alveopora",
#     "Tubinaria",
#     "Leptoria",
#     "Fungia",
#     "Herpolitha",
#     "",
#     "M.\nAnularis",
#     "Millipora",
#     "Octocorals",
#     "Millepora",
#     "Agaricia",
#     "Siderastrea",
#     "Sideastrea",
#     "Diploria",
#     "Pavona",
#     "Psammocora",
#     "Agarica",
#     "Faveolata",
#     "Scleractinians",
#     "Hydrocorals",
#     "Gorgonians",
#     "P.Clavus",
#     "Leptoseris",
#     "Diaseris",
#     "Cycloseris",
#     "Montrastea",
#     "Starghorn",
#     "S.\nRadians",
#     "Colpophyllia.Natans",
#     "Milleporides",
#     "M.Faveolata",
#     "S.Siderea",
#     "C.Natans",
#     "P.Porites",
#     "P.Astreoides",
#     "E.Fastigiata",
#     "M.Cavernosa",
#     "M.Memorialis",
#     "L.Cucullata",
#     "Turbinaria",
#     "Seriatopora",
#     "A.Nobilis",
#     "A.Cytherea",
#     "Echinoporids",
#     "Acroporids",
#     "Pocilloporids",
#     "Fungids",
#     "Faviids",
#     "Pocilloporidae",
#     "Fungiidae",
#     "Faviidae",
#     "Poritidae",
#     "Sinularia",
#     "Fungi",
#     "Herpolita",
#     "Pocillopra",
#     "Hydrophora",
#     "Mussiids",
#     "Branching",
#     "Pocillipora",
#     "Poscillopora",
#     "Stylopora",
#     "Submassive",
#     "Encrusting",
#     "Solitary",
#     "Symphyllia",
#     "Pachyseris",
#     "Briarium",
#     "Zoanthids",
#     "Pachyseris;",
#     "Lobophyllia",
#     "Montipora.",
#     "Turbinaria..",
#     "Porites.",
#     "Turbinaria.",
#     "Plating",
#     "Staghorn",
#     "Leptastrea",
#     "Faviidaeare",
#     "Sarcophyton",
#     "Turbanaria",
#     "Lobophytum",
#     "A.Grandis",
#     "Arcopora",
#     "Acorpora",
#     "Fungidaee",
#     "Sarcophyon",
#     "Massive",
#     "Porities",
#     "Acropra",
#     "Favidae",
#     "Montiproa",
#     "Gonopora",
#     "Pocilloporid",
#     "Brain",
#     "Porties",
#     "Coscinarea",
#     "Cyphastrea",
#     "Acroporapulchra",
#     "Favia.",
#     "Leptorina",
#     "Zooanthid",
#     "Galazea",
#     "Lepastrea",
#     "Acanthastrea",
#     "Sandalolitha",
#     "Seritopora",
#     "Favid",
#     "Diploastrea",
#     "Caulastrea",
#     "Pavona\tFrondifera",
# ]

# genus_ = []

# for lookup in lookups:
#     for gen in genus:
#         for genera in lookup["genera"]:
#             if gen == genera["genus_name"]:
#                 complete.append(gen)
#             for typo in genera["genus_typos"]:
#                 if gen == typo:
#                     complete.append(gen)

# print(f"genus: {len(genus)}")
# for gen in genus:
#     if gen not in complete:
#         genus_.append(gen)

# print(f"complete: {len(complete)}")
# print(f"genus - complete {len(genus_)}")
# # print(genus_)
# print(len(complete))


species = [
    "Cladocora Caespitosa",
    "Oculina Patagonensis",
    "Acropora Sp.",
    "Pocillopora Sp.",
    "Pocillopora",
    "Pavona And Porites",
    "Acropora Palmata",
    "Porites Astreoides",
    "Colpophyllia Natans",
    "Diploria Labyrinthiformis",
    "Montastraea Annularis",
    "Stephanocoenia Intersepta",
    "Agaricia Tenuifolia",
    "Leptoseris Cucullata",
    "Millepora Alcicornis",
    "Acropora Cervicornis",
    "A . Palmata",
    "Porites Porites",
    "Siderastrea Siderea",
    "Palythoa",
    "Montastrea",
    "Stylophora Sp. And Porites Sp.",
    "Montipora",
    "Hydnophora",
    "Echinopora",
    "Pocillopora Eydouxi",
    "P. Verrucosa",
    "P. Damicornis",
    "Porites",
    "Platygyra",
    "Galaxea",
    "Goniopora",
    "Astreopora",
    "Montipora And Hydnophora",
    "Acropora",
    "Porites Bra",
    "Galexea Astreata",
    "Favites",
    "Goniastrea",
    "Stylophora",
    "Fungia And Pocillopora",
    "Various Faviids And Fungiids",
    "Pavona.",
    "Goniopora Sp",
    "Turbinaria Sp",
    "Sinularia And Alcyonium Genera",
    "Porites Massive",
    "Favia",
    "Montipora And Coscinarea.",
    "Pocillopora Sp",
    "Alveopora",
    "Galaxea Fascicularis",
    "Pocillopora And Seriatiopora",
    "Tubinaria",
    "Platygyra And Favia",
    "A Cropora",
    "Leptoria",
    "Fungia",
    "Acropora Sp. Pocillaria Sp.",
    "Refer To Table",
    "A. Hyacinthus And A. Austera",
    "Similar To Tmr",
    "Primarily Affecting Montipora And\nAlveopora Spp. And The Sponge S. Kelleri",
    "M. Aequituberculata",
    "M. Monasteriata And\nM. Tuberculosa (55:0 +-24:4% Of All The Montipora\nColonies)",
    "A. Spongiosa And A. Clathrata. The\nAlcyoniidae S. Dura",
    "L. Depressum And To A Lesser\nExtent L. Patulum",
    "Sponge S. Kelleri",
    "Coscinarea Sp.",
    "Echinophyllia Sp.",
    "Echinopora Sp.",
    "Fungia Sp.",
    "Galaxea Astreata",
    "Herpolitha",
    "Hydnophora Sp.",
    "Pavona Sp.",
    "Physogyra Sp.",
    "Platygyra Sp.",
    "Plerogyra Sp.",
    "Porites Branching",
    "Seriatopora Sp.",
    "Synarea Sp.",
    "Astreopora Sp.",
    "Favia Sp.",
    "Favites Sp.",
    "Goniastrea Sp.",
    "Goniopora Sp.",
    "Lobopyllia Sp.",
    "Merulina Sp.",
    "Millepora Sp.",
    "Mycedium Sp.",
    "Oxypora Sp.",
    "Pachyseris Sp.",
    "Stylophora Sp.",
    "Turbinaria Sp.",
    "",
    "Cyphastrea Sp.",
    "Galaxea Astreata Sp.",
    "Montipora Sp.",
    "Psammacora Sp.",
    "Halomitra Sp.",
    "Herpolitha Sp.",
    "Leptoria Sp.",
    "Acanthastrea Sp.",
    "Diploastrea Sp.",
    "Gardinoseris Sp.",
    "Heliopora Sp.",
    "Leptastrea Sp.",
    "Leptoseris Sp.",
    "V Sp.",
    "Symphyllia Sp.",
    "Acropora Sp",
    "Diploastrea Sp",
    "Hard Coral",
    "Pocillaria Sp.",
    "Mostly Acopora",
    "All But Porites",
    "Acropora Digitifera",
    "A. Austera",
    "A. Abrotanoides",
    "A. Cytherea",
    "A. Clathrata",
    "Montipora Aequituberculata",
    "Pocillopora Spp.",
    "Favia Stelligera",
    "Massive Porites Sp.",
    "Porites Rus And Platygyra Daedalea",
    "Diploria Strigosa",
    "Meandrina Meandrites",
    "Montastrea Annularis",
    "And Diploria Labryinthiformis",
    "Mussa Angulosa",
    "Millepora Complanata",
    "Erythropodium Caribaeorum",
    "Plexaurella Sp.",
    "Dendrogyra Cylindrus",
    "Montastraea Faveolata",
    "Montastraea Cavernosa",
    "Diplora Strigosa",
    "Diplora Labyrinthiformis",
    "Agaricia Fragilis And Palythoa Caribaeorum",
    "Miliopora Complanata",
    "Meandrina Mendrites",
    "Sea Fan",
    "Agaricia Lamarcki",
    "Agaricia Agaricites",
    "Diploria Clivosa",
    "Montastraea Franksi",
    "Siderastrea Radians",
    "Diplorea Strigosa",
    "Colpohylia Natans Montastraea Annularis",
    "Stephanocoenia Intersepts",
    "Montastraea Cavermosa",
    "Siderastrea Sidera",
    "Madracis Mirabilis",
    "Madracis Formosa",
    "Sea Plumes- Pseudopterogorgia Spp.",
    "Common Sea Fan- Gorgonia Ventalina",
    "Millepora Alicornis",
    "Eusmilia Fastigiana",
    "Agaricia Undata",
    "Agaricia Sp.",
    "Montastrea  Annularis",
    "Acropora  Palmata",
    "Condylactis Gigantea",
    "Palythoa Caribaeorum",
    "Xestospongia\nMuta (Caribbean Barrel Sponge)",
    "Aplysina Fistularia ( Yellow Tube Sponge)",
    "Giant Barrel Sponges (Xestospongia Muta)",
    "Montastrea Faviolata",
    "S. Radians",
    "All Diplorias",
    "M.\nAnularis",
    "Millipora",
    "Octocorals",
    "Millepora",
    "Agaricia",
    "Diploria Sp.",
    "Colpophylia Natans. Millepora",
    "Scleractinian Sp. Porites",
    "Siderastrea",
    "Porites Asteroides",
    "Acropora Palmata And A. Cervicornis",
    "Montastraea Sp. (= Annularis Complex)",
    "Scleractinian Coral Sp.",
    "Colpophyllia Natans.",
    "Sideastrea",
    "Dichocoenia Stokesi",
    "Diploria",
    "Diploria\t Strigosa",
    "Siderastrea \tSiderea",
    "Agaricia\tT Enuifolia",
    "Porities\t Porites",
    "Siderea\t Siderastrea",
    "D. Strigosa M. Annularis",
    "A. Cervicornis A. Palmata",
    "Porities\t Astreoides",
    "Millapora\t Complanata",
    "A. Tenuifolia",
    "Diploria Labrynthyformis",
    "Briareum Asbestinum",
    "M. Faveolata",
    "A. Tennuifolia",
    "D. Strigosa",
    "S. Siderea",
    "Porites Furcata",
    "Eunicea Sp",
    "Palythoa Caribbea.",
    "Pavona",
    "Psammocora",
    "Agarica",
    "Montastraea\t Annularis",
    "Faveolata",
    "Millepora \tAlcicornis",
    "Agaricial\t Tennuifolia",
    "Briareum\t Asbestinum",
    "Diplori A\tStrigosa",
    "Eunicea Sp.",
    "Palythoa Caribbea",
    "Siderastrea Siderea Porites Furcata Acropora Palmata Eunicea Sp",
    "Pocillopora Panamensis",
    "Unknown Species",
    "Scleractinians",
    "Hydrocorals",
    "Gorgonians",
    "Not Montastrea Cavernosa",
    "Agaricia Sp.; Porites Porites; Millepora Sp.;\nSidearstrea Sidereal;",
    (
        "Agaricia Sp.; Porites Porites; Millepora Sp.; Montastrea Annularis; Diploria Strigosa;"
        " Diploria Labryinthiformis;\nFavia Fragum; Meandrina Meandrites"
    ),
    "Montastraea Cf. Annularis",
    "Porites Porites; Millepora Sp.; Agaricia Sp.; Porites Asteriodes",
    "Porites Porites; Montastrea Annularis;",
    "M. Cavernosa",
    "Favia Fragum",
    "And Porites Sp.",
    "(Finger Corals)",
    "Porites Asteroids",
    "Porites Porites; Millepora Sp.; Sidearstrea Siderea; Porites Asteriodes",
    "Diploria \tLabyrinthiformis",
    "Agaricia \tFragilis",
    "Millepora\t Alcicornis",
    "Diploria\t Labyrinthiformis",
    "Montastrea Franksi",
    "D. Labyrinthiformis And Porites Asteroides",
    "D. Labyrinthiformis",
    "Porites Asteroides And Agaricia Fragilis",
    "Montastreae Franksii",
    "Montastraea Frankesi",
    "Diploria Labyrithiformis",
    "Agaricia  Fragilis",
    "Argaricia Lamarcki",
    "Monastraea Faveolata",
    "Agaricia Spp",
    "Brain Corals And Branched Porites",
    "Montastraea Spp. And Agaricia Spp.",
    "Agaricia Spp.",
    "Diploria Spp.",
    "Montastraea Franksi And Acropora Palmata",
    "Diploria And Other Massive",
    "Not So For Acropora Palmata Nor Millepora",
    "Brain Coral",
    "Porites Spp. And Diploria Spp.",
    "Agaricia Spp And Montastraea Spp.",
    "Montastraea Spp. And Porites Spp.",
    "Montastraea Franksi And Agaricia Spp.",
    "Montastraea Cavernosa And Diploria Spp.",
    "Agaricia Spp. And Siderastrea Siderea",
    "Acropara Palmata",
    "Agaracia Lamarcki",
    "Diploria Labririnthiformis",
    "Diplora Labrynthiformis",
    "Meandrina Meandricites",
    "Millepora Alcicornis And M. Complanata",
    "Millepora Spp. (Mainly Complanata)",
    "Acropora Cervicornis Agaricia Agaricites: Porites Porites: \nPalythoa Caribaeorum",
    "Mussismilia Hispida",
    "Siderastrea Stellata",
    "Pocillopora Verrucosa",
    "A. Grahamae",
    "A. Undata",
    "M. Franksi",
    "P. Astreoides",
    "And Others.",
    "Colopophyllia Natans",
    (
        "Montastraea Faveolata; M. Annularis; M. Franksi; M. Cavernosa; Diploria Labyrinthiformis;"
        " D. Strigosa"
    ),
    (
        "Colpophyllia Natans; Porites Astreoides; Scolymia Sp; Siderastrea Siderea; Meandrina"
        " Meandrites; Porites Porites; Millepora Alcicornis; M. Complanata"
    ),
    "A . Cervicornis",
    "A . Tenuifolia",
    "P . Porites",
    "Favia Fragun",
    "D . Labyrinthiformis",
    "D . Strigosa",
    "Pavona Gigantea",
    "P.Clavus",
    "Colpophyllia Sp.",
    "Favia Fragum And Millepora Spp.",
    "M. Complanata",
    "E. Fastigiata",
    "F. Fragum",
    "Pavona Varians",
    (
        "Montastraea Faveolata; M. Annularis; Diploria Labyrinthiformis; D. Strigosa; Porites"
        " Astreoides; Siderastrea Siderea"
    ),
    "Acropora Palmate",
    "Siderastrea Sidereal",
    "A Tenuifolia",
    "Colpophyilia Natans",
    "Millepora Spp.",
    "And The Zoanthid Palythoa\nCaribbaeorum",
    "Leptoseris",
    "Psammocora Sp",
    "Pavona Clavus",
    "Porites Lobata",
    "P. Varians",
    "Psammocora Stellata",
    "Diaseris Distorta",
    "Cycloseris Curvata",
    "Diaseris",
    "Cycloseris",
    "Psammacora Stellata",
    "Millepora Alcicornis And P. Astereoides.",
    "A. Palmata And M. Complanta",
    "Millepora Intricata",
    "C. Natans",
    "M. Meandrites",
    "A. Agaricites",
    "Montrastea",
    "Colpophyllia And Porites",
    "Stephanocoenia Michelini",
    (
        "Millepora Alcicornis\nM. Complanta \nAgaricia Tenuifolia\nA. Agaricites\nDiploria"
        " Labyrinthiformis"
    ),
    "Montastrea Sp.",
    "Siderastrea Sp. And Millepora Sp.",
    "Agaricia Agaracites",
    "Sidereastrea Siderea",
    "Stephanocoenia Mechellini And\nPalythoa Sp. Species Unaffected Were Dichocoenia Stokesii",
    "Montastrea Cavernosa",
    "M. Alcicornis",
    "Erythropodium Caribaeorum (Encrusting Gorgonian) And Briaream\nAsbestinum",
    "Sideratrea Sp. Dichocoenia Stokesii",
    "Montastrea Faveolata",
    "M. Annularis",
    "Dichocoenia Stokesii",
    "D. Labrynthiformis",
    "P. Porites",
    "And Stephanocoenia Intersepta",
    "And Some Other Gorgonians.",
    "Amphistengina Gibbosa",
    "Agaricia\t Agaricites",
    "Porites\t Astreoides",
    "Diploria\t Clivosa",
    "Briareum\t  Asbestinum",
    "Palythoa\t  Caribbaeorum",
    "Eusmilia Fastigiata",
    "Starghorn",
    "Montastrea\t Cavernosa",
    "Meandrina\t Meandrites",
    "S.\nRadians",
    "And S. Siderea",
    "Millepora (Fire Coral)",
    "Montastrea Annularis\nDiploria Strigosa",
    "Palythoa Caribaeourm",
    "Millepora Complanta",
    "P. Furcata",
    "P. Divaricata",
    "Millipora Alcicornis",
    "M. Complanata And M. Complanata And Palythoa Caribaeorum",
    "Erythropodium Sp.",
    "A. Palmata",
    "Colpophyllia.Natans",
    "M. Complanata And Palythoa Caribaeorum",
    "Montastraea Spp.",
    "Porites Spp.",
    (
        "<Br>\nEncrusting Gorgonians (Erythropodium Caribbaeorum) And Zoanthids (Palythoa"
        " Caribbaeorum)"
    ),
    "Diploria Clivosa And Millepora Alcicornis.",
    "Siderastrea\nSiderea And Montastrea Annularis.",
    "M. Squarrosa",
    "Diploria Strigosa And D. Labyrinthyformis",
    "Undaria Agaricites",
    (
        "Siderastrea Siderea Are The Most Affected Within The Hard Corals. Millepora Spp."
        " Erythropodium Caribbaeorum"
    ),
    "Palythoa Caribbaeorum",
    "Palythoa Caribaerum",
    "Briaeorun Asbestinum",
    "Agaricia Agaricites Species ( A. Agaricites",
    "A. Humilis",
    "A. Danae",
    "A. Purpurea)",
    "Porites Porites  And P. Divaricata",
    "Montastraea Group ( M. Faveolata And M. Franksi )",
    "Only Pseudoplexaura Porosa And Plexaurella Nutans.",
    "Montastrea Sp",
    "Milleporides",
    "Scolymia Cubensis",
    "Agaricia Fragilis",
    "Agaricia Humilis",
    "Milleporids Alcicornis",
    "M.Faveolata",
    "S.Siderea",
    "C.Natans",
    "P.Porites",
    "P.Astreoides",
    "E.Fastigiata",
    "M.Cavernosa",
    "M.Memorialis",
    "L.Cucullata",
    "Stephanocoenia Intersepta And Montastraea Cavernosa",
    "Millepora Alcicornis And Montastrea Cavernosa",
    "Montastraea Cavernosa And At Least Eleven Other Species",
    "Porites Divaricata",
    "Almost All Of The Montastraea Colonies (Except M. Cavernosa)",
    "And Millepora <Br>\nPalythoa Spp.",
    "Pories Porites",
    "Mycetophyllia Spp.",
    "Isophyllia Spp.",
    "Solenastrea Spp.",
    "Manicina Areolata",
    "Madracis Spp.",
    "And The Zoanthid Palythoa",
    "Montastraea Annularis (Complex)",
    "And P. Astreoides",
    "Colpophyllia \nNatans",
    "Leptoseris Cuculata",
    "Acropora Nobilis",
    "A. Hyacinthus",
    "A. Digitifera",
    "Platygyra Lamellina",
    "Acropora Monticulosa",
    "Pocillopora Eudoxii",
    "Montipora Informis",
    "Porites Sp",
    "Turbinaria",
    "Favites Etc. And Porites",
    "Favia Sp",
    "Lobophytum Crassum",
    "Porites Lutea And Montipora Digitata",
    "Echinophyllia And Soft Corals.",
    "Millepora And Soft Corals",
    "Seriatopora",
    "Soft Coral And Sea Anemone",
    "Pocilopora Damicornis",
    "Acropora Formosa",
    "A. Intermedia",
    "A.Nobilis",
    "A.Cytherea",
    "Montipora Digitata",
    "Goniastera Sp.",
    "Porites Sp.",
    "Echinopora Sp. And  Favia Sp.",
    "Branching Coral",
    "Acropora Cytherea",
    "A. Formosa",
    "A. Nobilis",
    "M. Foliosa",
    "M. Digitata And Pocillopora Damicornis.",
    "M. Foiliosa",
    "M. Divaricata",
    "Hydnopora Sp.",
    "And  Favia Sp.",
    "Acropora Humilis",
    "Favia Pallida",
    "Fungia Concinna",
    "Lobophyllia Robusta",
    "Montostrea Sp.",
    "Lobophyllia Corymbosa",
    "Montipora Foliosa",
    "Fvia Sp.",
    "Gonioastrea Sp.",
    "Pocilipora Damicornis",
    "Goniastrea Sp. And Favites Sp.",
    "Montipora Digitata And Favia Sp.",
    "Table Acropora",
    "Pocilloproa Verrucosa And P. Damicornis",
    "Acropora Cerealis",
    "Gardineroseries Sp.",
    "Lobophyllia Sp.",
    "Favites Abdita",
    "Montipora Foliosa And M. Divaricata",
    "Echinoporids",
    "Acroporids",
    "Pocilloporids",
    "Fungids",
    "Sea Anemones",
    "Faviids",
    "Pocilloporidae",
    "Fungiidae",
    "Tabular Acroporidae",
    "Faviidae",
    "Poritidae",
    "Sinularia",
    "Fungi",
    "Platygyra Sp. Porites.",
    "Herpolita",
    "Leptoria Phrygia",
    "Favia Favus",
    "Platygyra Daedalea",
    "Hydnophora Microconos",
    "Symphyllia Radians",
    "Pocillopora Damicornis",
    "Acropora Muricata",
    "Favids. Not Montipora",
    "Pocillopra",
    "Acropora Spp. And D. Heliopora",
    "Hydrophora",
    "Massive Porites",
    "Mussiids",
    "Branching",
    "Table Form And Brain Coral",
    "Acropora Table",
    "Pocillipora",
    "Acropora Branching",
    "Seriotopora Hystrix",
    "Poscillopora",
    "Montipora (Submasive And Encrusting)",
    "Stylopora",
    "Fungiid (Fungia",
    "Ctenactis And Sandhalolita)",
    "Diploastrea Heliopora Pectinia",
    "Submassive",
    "Encrusting",
    "Solitary",
    "Soft And Hard Corals Are Bleached",
    "Predominantly Leather Coral",
    "Encrusting Coral And Plate Coral",
    "Hard Corals Bleached",
    "Predominantly Encrusting Coral On This Reef",
    "Poritidae Boulder Corals",
    "Euphyllia Glabrescens",
    "Symphyllia",
    "Plate Coral",
    "Mushroom Coral",
    "Acropora Sp. Euphyllia Glabrescens",
    "Porites Bommies",
    "Pachyseris",
    "Briarium",
    "Hard Coral Bommies",
    "Organ Pipe Coral",
    "Encrusting Coral",
    "Soft Coral",
    "Plate Corals",
    "Montipora And Pachyseris",
    "Zoanthids",
    "Pachyseris;",
    "Branching Acropora",
    "Porites Cylindrica",
    "P. Lutea",
    "Psammocora Digitata",
    "Lobophyllia",
    "Acropora Spp",
    "Massive Corals Especially Patches Of Porites",
    "Sea Anemonies",
    "Barrel Sponges (Bleached White And Sponges Disintegrated)",
    "Dendronepthiid Soft Corals",
    "Sea Anemone",
    "Sea Anemone (Heteractis Magnifica)",
    "Plate And Encrusting Corals",
    "Hard Corals",
    "Predominantly Encrusting Coral And Plate Coral On This Reef",
    "Predominantly Encrusting Coral And Plate Coral",
    "Hard Corals Are Bleached",
    "Predominantly Plate Coral",
    "Symphyllia Sp",
    "Favites Sp. And Zooantids",
    "Plate And Encrusting Coral",
    "Encrusting Coral (Galaxea)",
    "Montipora.",
    "Turbinaria..",
    "Porites.",
    "Turbinaria.",
    "Galaxea Fasicularis",
    "Plating",
    "Branching And Foliose Forms. Mainly Acropora",
    "Not Porites",
    "Porites And Pavona And Millepora.",
    "Staghorn",
    "Brain Types. Not Firecoral.",
    "Acropora Spp. Seriatopora Hystrix",
    "P. Lobata",
    "Sarcophyton Spp.\nAnd Bottlebrush Acropora Spp Pocillopora Damicornis",
    "Soft Coral Forms (Sinularia Flexibilis",
    "Other Sinularia Spp. And Sarcophyton Spp",
    "Porites And Pavona And Millepora And Carijoa Sp.",
    "Goniastrea Asper",
    "Platygyra Sinensis",
    "Porites Lutea",
    "Goniastrea Asper And G. Retiformis",
    "G. Retiformis",
    "P. Daedales",
    "Acropora Asper",
    "Coeloseris Mayeri",
    "Leptastrea Transversa",
    "Massive Porties",
    "Leptastrea",
    "And Acropora",
    "Faviidaeare",
    "Sarcophyton",
    "Lobophytum And Sinularia.",
    "Turbanaria",
    "Lobophytum And Sinularia",
    "Lobophytum",
    "Acropora Chytherea",
    "A.Grandis",
    "A. Microphhtalmata",
    "A. Hyacinthus.",
    "Arcopora",
    "Massive Corals",
    "Stylophora Pistillata",
    "Acorpora",
    "Fungidaee",
    "Sarcophyon",
    "Stylophora Pistillate",
    "Massive",
    "Porities",
    "Acropra",
    "Favidae",
    "Montiproa",
    "Hard And Soft Corals Of A Wide Range Of Species With Anemones",
    "Gonopora",
    "Pocilloporid",
    "Acropora Plates",
    "Fungid Sp",
    "Brain",
    "Fire Coral",
    "Acropora Arabensis",
    "A. Clathata",
    "Coscinarea Monile",
    "Porites Compressa",
    "Massive Hard Corals",
    "Soft Corals",
    "Porties",
    "Symphyllia Recta",
    "Platygyra And Soft Corals.",
    "Coscinarea",
    "Cyphastrea",
    "Acropora Clathrata",
    "A. Downingi",
    "Cyphastrea Microphthalma",
    "Oculina Patagonica",
    "Montastrea Curta",
    "Pocillopora Verrusosa And Porites",
    "Acropora \tMicrophthama",
    "Acroporapulchra",
    "Acropora Pulcha",
    "Pocillopora Eydox",
    "P. Verrucosa Pale",
    "Pavona Maldivensis",
    "Acropora Crateriformis",
    "Lepastrea Purpurea",
    "Goniastrea Edwardsi",
    "Goniastrea Retiformis",
    "Fungia Sp",
    "Acropora Microphthama",
    "Acropora And Pocillopora",
    "Pocillopora And Montastrea Curta",
    "Pocillopora Eydoxi And P. Verrucosa",
    "Porites Sp. Leptoria \tPhryga",
    "Montipora Verrucosa",
    "Favia.",
    "Acropora Pulchra",
    "Leptorina",
    "Montastrea Curta And Some Porites",
    (
        "Major Species Affected- Acropora Staghorn (3 Species) \nAcropora Palifera And A. Cf."
        " Listeri - Very Minor Bleaching"
    ),
    "Montipora Venosa",
    "Branching And Plate Aropora",
    "Millepora Platyphylla",
    "Montipora Sp. Acropora Verweyi",
    "Seriatopora Aculeta",
    "Pachyeris Speciosa",
    "Montastraea Curta",
    "Small Acropora Spp",
    "Such As A.\nDigitifera",
    "Acropora Seriata(?)",
    "Zooanthid",
    "Porites And Millepora",
    "Acroporas (At Least Cerealis And Robusta And Maybe Nana",
    "All Acropora Species\nLobophytum Sp\nPocillopora Sp\n\nOther Coral Show No Bleaching",
    "Acropora Sp. \nLobophytum Pauciflorum \nPavona Cactus",
    "Fungia Fungites \nLobophylla Hemprichii",
    "Montipora Foveolata",
    "Pocillopora Elegans",
    "Acropora Humulis",
    "Boloceriodes Sp & The Sponge Spirastrella Cf. Vagabundi",
    "Montipora Sp",
    "Galazea",
    "Montipora & Pavona Resistant To Bleaching",
    "Montipora And Leptoseris",
    "Porites\nAnd Fungia",
    "Lepastrea",
    "Acanthastrea",
    (
        "Branching Forms Are Small (Diameter<30Cm) And More Heavily Impacted ; Encrusing Forms"
        " Abundant But Occasional Bleaching."
    ),
    "Small (<20Cm Diameter) Branching Colonies (Acorporids",
    (
        "Pocillopra) And Encrusting Montipora; No Bleaching On Massive Porites (Largest 25% Of"
        " Massive Corals Is ~2Meters); Total Cover - 1-10%"
    ),
    "Bleaching Occur Mostly\nFor Tabular Acroporid Forms",
    "~10-30% Of Colonies Were Bleached",
    "Sandalolitha",
    "And Favia",
    "Acropora Sp. Echinopora Sp.",
    "Sinnularia Sp",
    "Acropora And Pocillopora.",
    "Halimetra Pilleus",
    "Dominated By Acropora.",
    "Acropora Hyacinthus",
    "Shallow Fringing Reef Off A Small Inshore\nIsland. No Particular Dominants.",
    "Seritopora",
    "Favid",
    "Dominated By Soft Corals",
    "Scleractinian Corals Dominated By Small Pocillopora.",
    "Diploastrea",
    "Caulastrea",
    "Stylophora Pocillopora",
    "A. Muricata",
    "A. Aspera",
    "Goniastrea Spp.",
    "Symphillia Spp.",
    "Pocillopora Darmicornis",
    "P. Eydouxi",
    "P. Meandrina And P. Verrucosa",
    "Acropora\t Microphthalma",
    "Acropora\t Pulchra",
    "Acropora\t Nobilis",
    "Porites\t Cylindrica",
    "Acropora \tPulchra",
    "Porites\tC Ylindrica",
    "Acropora \tMicrophthalma",
    "Porites \tCylindrica",
    "Pavona\tFrondifera",
    "Staghorn Acropora",
    "Acropora\t Microphthalma (Starghorn)",
    "Porites\t Cylindrica (Finger)",
    "Porites\t Lobata (Lobe)",
    "Acropora Sp (Plate And Staghorn)",
    "Acropora Robusta",
    "Montipora Patula",
    "Porites Evermanni",
    "And Porites Lobata",
    "Montipora Capitata",
    "Pocillopora Meandrina",
    "And Pocillopora Damicornis",
    "Pocillipora Eydouxi",
]
species_ = []
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

for sp in species:
    for substring in substrings:
        if substring in sp:
            sp = sp.replace(substring, "")
            if sp.strip() not in species_:
                species_.append(sp.strip())
        else:
            if sp.strip() not in species_:
                species_.append(sp.strip())

# species2 = []
# genus = []
# subsp = []
# dot = []


sing_species = [
    "Favites",
    "Pavona.",
    "",
    "M.\nAnularis",
    "Octocorals",
    "Faveolata",
    "Scleractinians",
    "Hydrocorals",
    "Gorgonians",
    "P.Clavus",
    "Starghorn",
    "S.\nRadians",
    "Colpophyllia.Natans",
    "Milleporides",
    "M.Faveolata",
    "S.Siderea",
    "C.Natans",
    "P.Porites",
    "P.Astreoides",
    "E.Fastigiata",
    "M.Cavernosa",
    "M.Memorialis",
    "L.Cucullata",
    "A.Nobilis",
    "A.Cytherea",
    "Acroporids",
    "Pocilloporids",
    "Fungids",
    "Faviids",
    "Pocilloporidae",
    "Fungiidae",
    "Poritidae",
    "Hydrophora",
    "Mussiids",
    "Branching",
    "Submassive",
    "Encrusting",
    "Solitary",
    "Zoanthids",
    "Pachyseris;",
    "Montipora.",
    "Turbinaria..",
    "Porites.",
    "Turbinaria.",
    "Plating",
    "Staghorn",
    "Faviidaeare",
    "A.Grandis",
    "Fungidaee",
    "Massive",
    "Gonopora",
    "Pocilloporid",
    "Brain",
    "Acroporapulchra",
    "Favia.",
    "Zooanthid",
    "Caulastrea",
    "Pavona\tFrondifera",
]

complete = [
    "Montipora",
    "Astreopora",
    "Acropora",
    "Alveopora",
    "Arcopora",
    "Acorpora",
    "Acropra",
    "Montiproa",
    "Agaricia",
    "Pavona",
    "Agarica",
    "Leptoseris",
    "Pachyseris",
    "Sinularia",
    "Sarcophyton",
    "Lobophytum",
    "Sarcophyon",
    "Briarium",
    "Coscinarea",
    "Tubinaria",
    "Turbinaria",
    "Turbanaria",
    "Diploastrea",
    "Galaxea",
    "Galazea",
    "Favia",
    "Faviidae",
    "Favidae",
    "Favid",
    "Fungia",
    "Herpolitha",
    "Diaseris",
    "Cycloseris",
    "Fungi",
    "Herpolita",
    "Sandalolitha",
    "Leptastrea",
    "Lepastrea",
    "Symphyllia",
    "Lobophyllia",
    "Acanthastrea",
    "Hydnophora",
    "Echinopora",
    "Platygyra",
    "Goniastrea",
    "Leptoria",
    "Echinoporids",
    "Cyphastrea",
    "Leptorina",
    "Millipora",
    "Millepora",
    "Montastrea",
    "Montrastea",
    "Diploria",
    "Pocillopora",
    "Stylophora",
    "Seriatopora",
    "Pocillopra",
    "Pocillipora",
    "Poscillopora",
    "Stylopora",
    "Seritopora",
    "Porites",
    "Goniopora",
    "Goniopora",
    "Porities",
    "Porties",
    "Psammocora",
    "Siderastrea",
    "Sideastrea",
    "Palythoa",
]
# print(f"Species: {len(species)}")
# print(f"Species_: {len(species_)}")
# for gen in sing_species:
#     if gen not in complete:
#         species2.append(gen)

#print(f"Species2 {species2}\n")
# complete.append(species2)
# #print(complete)
# tstr = []
# print(len(complete))
# print(len(species_))
# for sp in species_:
#     if "\t" in sp:
#         tstr.append(sp)
# print(f"T strings: {tstr}")
# print(len(species_))
# for sp in species2:
#     for substring in substrings:
#         if substring in sp and sp not in subsp:
#             subsp.append(sp)
#         elif "." in sp and sp not in dot:
#             dot.append(sp)

# print(f"dot: {len(dot)}")
# print(f"subsp: {len(subsp)}")

# subsp2 = []
# for sp in subsp:
#     for substring in substrings:
#         if substring in sp:
#             subsp2.append(sp.replace(substring, ""))

# print(f"subsp2: {len(subsp2)}")

print(f"Species: {len(species)}")

s_typo_t = False
f_typo_t = False
g_typo_t = False
new_sp = []
get_out = False

for sp in species:
    for substring in substrings:
        sp = sp.replace(substring, "")
    sp = sp.strip().title()
    for lookup in lookups:
        if get_out:
            break
        if sp == lookup["family_name"]:
            get_out = True
            break
        else:
            for f_typo in lookup["family_typos"]:
                if get_out:
                    break
                if sp != f_typo:
                    f_typo_t = False
                else:
                    f_typo_t = True
                    get_out = True
                    break
            if f_typo_t == False:
                for genus in lookup["genera"]:
                    if get_out:
                        break
                    if sp == genus["genus_name"]:
                        get_out = True
                        break
                    else:
                        for g_typo in genus["genus_typos"]:
                            if get_out:
                                break
                            if sp != g_typo:
                                g_typo_t = False
                            else:
                                g_typo_t = True
                                get_out = True
                                break
                        if g_typo_t == False:
                            for sp_ in genus["genus_species"]:
                                if get_out:
                                    break
                                if sp == sp_["species_name"]:
                                    get_out = True
                                    break
                                else:
                                    for s_typo in sp_["species_typos"]:
                                        if get_out:
                                            break
                                        if sp != s_typo:
                                            s_typo_t = False
                                        else:
                                            s_typo_t = True
                                            get_out = True
                                            break
                                    if s_typo_t == False:
                                        if sp not in new_sp:
                                            new_sp.append(sp)
    get_out = False

print(f"New Species: {len(new_sp)}")
print(new_sp)