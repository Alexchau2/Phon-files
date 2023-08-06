import itertools
import os
import re
import string
import time
import timeit
import xml
import xml.etree.ElementTree as ET
from cgi import test
from cmd import PROMPT
from os import listdir
from os.path import exists, isfile, join
# from types import NoneType
from typing import Any, List, Union
from unittest import skip

# import openpyxl
# import xlrd

# Example
# ɛlᵖ has 3 characters in the string
# ɛ is index 0
# l is index 1
# ᵖ is index 2
# However, Phon treats lᵖ as one index rather than two separate ones due to diacritic
# If you were to get the indexes without fixing, the output would be something like ['0', '1 2']
# where '0' corresponds to ɛ and '1 2' corresponds to lᵖ
# This function treats lᵖ as one index, but you are able to index the phoneme and diacritic separately
# Output: {('8c437a92-64f3-4438-8098-62273be265a7', 'ɛlᵖ'): ['0', ['1', '2']]}


def Diacritic_fixer(record_xml_element, tiers=["model", "actual"]):
    # -> dict[list[dict[str, str]], list[dict[str,str]]]
    # os.chdir(media_folder)

    # # Get XML files
    # xml_files = [
    #     xml_file
    #     for xml_file in listdir(media_folder)
    #     if isfile(join(media_folder, xml_file))
    # ]

    # Replaced user input with function parameter ipaTier
    # For streamlined use when called from another script
    # assert (
    #     ipaTier == "model" or ipaTier == "actual"
    # ), "ipaTier must be specified as either model (target) or actual"

    try:
        phon_link = "{http://phon.ling.mun.ca/ns/phonbank}"
        ns = {"": "http://phon.ling.mun.ca/ns/phonbank"}
        ipaTier_model = str((".//" + phon_link + "ipaTier"))
        transcription = str((".//" + phon_link + "w"))
        transcription_pg = str((".//" + phon_link + "pg/*"))
        speaker = str((".//" + phon_link + "u"))
        orthography_w = str((".//" + phon_link + "g/*"))
        transcription_indices = str((".//" + phon_link + "sb/*"))
        alignment_segmental = str((".//" + phon_link + "alignment"))
        transcription_length = str((".//" + phon_link + "ag/*"))

        start = timeit.default_timer()
        id = record_xml_element.get("id")
        # Instantiate output dictionary
        output = {}

        tier: ET.Element
        for tier in tiers:
            tier_e: ET.Element = record_xml_element.find(f".//ipaTier[@form='{tier}']", ns)
            pg_list:list[ET.Element]= tier_e.findall(".//pg", ns)  # Prosodic Groups
            count_pg = len(pg_list)  # debugging
            pgs = []  # List for diacritic_fix dict for each pg
            for i, pg in enumerate(pg_list):
                transcriptions = [w.text for w in pg.findall("w", ns)]
                count_w = len(transcriptions)  # debugging
                indices = pg.findall(".//ph", ns)  # Character indices
                transcriptions = " ".join(transcriptions)
                # Fix indexing for this prosodic group (pg)
                diacritic_fix = {  # Dictionary with id and transcription as keys
                    "id": id,
                    "tier": tier,
                    "pg": i,
                    "transcriptions": transcriptions,
                    "indices": [  # fixed embedded character indices
                        list(
                            map(int, index.get("indexes").split())
                        )  # Get indexes for phoneme with diacritics
                        if len(index.get("indexes").split())
                        > 1  # Check if diacritic exists in indexes
                        else int(
                            index.get("indexes")
                        )  # If no diacritic just get indexes
                        for index in indices
                    ]
                    # Could zip in the sctype and hiatus info here
                }
                stop = timeit.default_timer()
                # print(f"{tier}, pg:{i} time: ", stop - start)  # Debugging
                # Add diacritic_fix dict for this pg to output dictionary
                pgs.append(diacritic_fix)
            output[tier] = pgs
        # Example access: output['actual'][0]["indices"]
    except TypeError:
        pass
    return output


if __name__ == "__main__":
    ns = {"": "http://phon.ling.mun.ca/ns/phonbank"}
    test_dir = "/Users/pcombiths/Documents/GitHub/Phon-files/XML Test/dpa"
    test_file = "/Users/pcombiths/Documents/GitHub/Phon-files/XML Test/groups-words/Anne_Pre_PC.xml"
    test_tree = ET.parse(test_file)
    test_root = test_tree.getroot()
    test_records = test_tree.findall(".//u", ns)
    output = Diacritic_fixer(test_records[0])
