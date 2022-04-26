# -*- coding: utf-8 -*-


import xml.etree.ElementTree as ET
from copy import deepcopy

from cro.rundown.sdk._domain import Station, StationType

__all__ = tuple(
    [
        "STATON_CODE_TO_NAME",
        "STATION_NAME_TO_OBJECT",
        "clean_rundown_name",
        "clean_rundown_content",
    ]
)


# Maps the station ID to station object.
STATION_NAME_TO_OBJECT: dict[str, Station] = {
    "Plus": Station(11, "Plus", StationType.NATIONWIDE),
    "Radiožurnál": Station(13, "Radiožurnál", StationType.NATIONWIDE),
    "Dvojka": Station(0, "Dvojka", StationType.NATIONWIDE),
    "Vltava": Station(0, "Vltava", StationType.NATIONWIDE),
    "Pohoda": Station(0, "Pohoda", StationType.NATIONWIDE),
    "Wave": Station(0, "Wave", StationType.NATIONWIDE),
    "RŽ_Sport": Station(0, "RŽ_Sport", StationType.NATIONWIDE),
    "ČRo_Brno": Station(0, "ČRo_Brno", StationType.REGIONAL),
    "ČRo_DAB_Praha": Station(0, "ČRo_DAB_Praha", StationType.REGIONAL),
    "ČRo_Sever": Station(0, "ČRo_Sever", StationType.REGIONAL),
    "ČRo_Plzeň": Station(0, "ČRo_Plzeň", StationType.REGIONAL),
    "ČRo_Budějovice": Station(0, "ČRo_Budějovice", StationType.REGIONAL),
    "ČRo_Ostrava": Station(0, "ČRo_Ostrava", StationType.REGIONAL),
    "ČRo_Vysočina": Station(0, "ČRo_Vysočina", StationType.REGIONAL),
    "ČRo_Zlín": Station(0, "ČRo_Zlín", StationType.REGIONAL),
    "ČRo_Region_SC": Station(0, "ČRo_Region_SC", StationType.REGIONAL),
    "ČRo_Liberec": Station(0, "ČRo_Liberec", StationType.REGIONAL),
    "ČRo_Hradec_Králové": Station(0, "ČRo_Hradec_Králové", StationType.REGIONAL),
    "ČRo_Pardubice": Station(0, "ČRo_Pardubice", StationType.REGIONAL),
    "ČRo_Olomouc": Station(0, "ČRo_Olomouc", StationType.REGIONAL),
    "ČRo_Karlovy_Vary": Station(0, "ČRo_Karlovy_Vary", StationType.REGIONAL),
    "ČRo_České_Budějovice": Station(0, "ČRo_České_Budějovice", StationType.REGIONAL),
    "ČRo_Region": Station(0, "ČRo_Region", StationType.REGIONAL),
    "Junior": Station(0, "Junior", StationType.NATIONWIDE),
    "Radio_Prague_International": Station(
        0, "Radio_Prague_International", StationType.NATIONWIDE
    ),
}

# Maps the station numeric code to short name (abbreviation) and station long name tuple.
STATON_CODE_TO_NAME: dict[int, str] = {
    3: ("UN", None),  # TODO: Write stationa name
    5: ("CR", None),
    11: ("RZ", None),
    13: ("PS", None),
    15: ("DV", None),
    17: ("VL", None),
    19: ("WA", None),
    21: ("RJ", None),
    23: ("ZV", None),
    31: ("RD", None),
    33: ("SC", None),
    35: ("PN", None),
    37: ("KV", None),
    39: ("SE", None),
    41: ("LB", None),
    43: ("HK", None),
    45: ("PC", None),
    47: ("CB", None),
    49: ("VY", None),
    51: ("BO", None),
    53: ("OL", None),
    55: ("OV", None),
    57: ("ZL", None),
    73: ("RG", None),
    75: ("RE", None),
}


class RundownCleanErrror(Exception):
    ...


def clean_rundown_name(source: str) -> str:
    """
    Clean the rundown XML file name.
    """
    hour, other = source.stem[3:8], source.stem[9:]
    hour = tuple(hour.split("-"))

    date = other.split("_")[-1]
    year, month, day = date[:4], date[4:6], date[6:8]

    if "-" in other:
        station = other.split("-")[0]
    else:
        station = "".join([i for i in other if not i.isdigit()])

    station = station.strip("_")  # Remove trailing `_`.
    station = STATION_NAME_TO_OBJECT[station]  # Get station model.

    # Return tuple (year, name).
    # @todo: This is hack to be able to save the file to the `year` folder.

    clean_station_name = station.name.replace("_", "-").replace("ČRo-", "")
    file_prefix_name = f"RUNDOWN_{year}-{month}-{day}_{hour[0]}-{hour[1]}"

    return (year, file_prefix_name + f"_{station.type.name[0]}_{clean_station_name}")


def clean_rundown_content(tree: ET.ElementTree) -> ET.ElementTree:
    """
    Clean the rundown XML file content.

    Removes unnecessary nodes so the XML is much more smaller, e.g.
    - unused `<OM_FIELD>` nodes
    - unused `<OM_UPLINK>` nodes
    - etc.
    """
    tree = deepcopy(tree)  # Be sure you don't modify the original tree!

    # > Radio Rundown OM_OBJECT: only one node.
    rr = tree.find('.//*[@TemplateName="Radio Rundown"]')

    header = rr.find("./OM_HEADER")
    for field in header.findall('*[@IsEmpty="yes"]'):
        header.remove(field)

    for field in header.findall("./OM_FIELD"):
        if (
            field.attrib["FieldID"]
            not in "8 5016 1005 1000 5081 6 5070 5072 5082 12 321".split()
        ):
            header.remove(field)

    # Clean OM_RECORD(S)
    for omr in rr.findall(".//OM_RECORD"):

        for field in omr.findall('*[@IsEmpty="yes"]'):
            omr.remove(field)

        for field in omr.findall("./OM_FIELD"):
            if (
                field.attrib["FieldID"]
                not in "8 5016 1005 1000 5081 6 5070 5072 5082 12 321".split()
            ):
                omr.remove(field)

        for field in omr.findall("./OM_UPLINK"):
            omr.remove(field)

    # Clean OM_OBJECT(s)
    for omb in rr.findall(".//OM_OBJECT"):

        header = omb.find(".//OM_HEADER")
        for field in header.findall('*[@IsEmpty="yes"]'):
            header.remove(field)

        for field in header.findall("./OM_FIELD"):
            if (
                field.attrib["FieldID"]
                not in "8 5016 1005 1000 5081 6 5070 5072 5082 12 321".split()
            ):
                header.remove(field)

        for field in omb.findall("./OM_FIELD"):
            if (
                field.attrib["FieldID"]
                not in "8 5016 1005 1000 5081 6 5070 5072 5082 12 321".split()
            ):
                omb.remove(field)

        for field in omb.findall("./OM_UPLINK"):
            omb.remove(field)

    return tree
