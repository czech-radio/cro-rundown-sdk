# -*- coding: utf-8 -*-


import xml.etree.ElementTree as ET
from copy import deepcopy
from pathlib import Path
from typing import List

from cro.rundown.sdk._domain import Station, StationType

__all__ = tuple(["RundownCleaner", "clean_rundown", "station_mapping"])


class RundownCleaner:
    """
    This class removes unnecessary nodes form OpenMedia XML files
    so the file is much more smaller.
    """

    def __init__(self, path: Path, batch_mode=True):
        self._path = path
        self._errors: List = []


station_mapping = {
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
}


def clean_rundown(tree: ET.ElementTree) -> ET.ElementTree:
    """
    Clean the rundown XML file.

    - Remove all empty <OM_FIELD> nodes.
    - Remove all unused nodes:
      -
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
