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
from types import NoneType
from unittest import skip

import openpyxl
import xlrd

# from diacritics_list import diacritics_list

media_folder = "C:\\Users\\alex\\Documents\\GitHub\\Combiths Lab\\Phon\\XML Files"

os.chdir(media_folder)

# Get XML files

xml_files = [
    xml_file
    for xml_file in listdir(media_folder)
    if isfile(join(media_folder, xml_file))
]

# Ask user if they want model/target or actual transcriptions

while True:
    ipaTier = input("Model (target) or actual transcription? ")

    if ipaTier == "model":
        print("Model")
        break

    elif ipaTier == "actual":
        print("Actual")
        break

    else:
        print("Please select either model (target) or actual. ")
        continue

phon_link = "{http://phon.ling.mun.ca/ns/phonbank}"
ipaTier_model = str((".//" + phon_link + "ipaTier"))
transcription = str((".//" + phon_link + "w"))
transcription_pg = str((".//" + phon_link + "pg/*"))
speaker = str((".//" + phon_link + "u"))

start = timeit.default_timer()

# xml_file = "1007_CCP_CCP Pre.xml"

# Go through all XML files in the directory
for files in xml_files:
    # Parse through files

    tree = ET.parse(files)
    root = tree.getroot()

    def get_transcriptions():
        # Get ids

        ids = [id.attrib["id"] for id in root.findall(speaker)]

        # Get transcriptions for each unique id into a list

        id_transcriptions = []

        # Iterate over ids
        for id in ids:
            transcriptions = []

            # Get transcription for each unique id
            for transcription in root.findall(
                speaker
                + str("[@id=" + "'" + id + "'" + "]/")
                + ipaTier_model
                + "[@form='"
                + ipaTier
                + "']/"
                + transcription_pg
            ):
                # Exclude sb tag and if there is no text
                if (
                    transcription.tag != str(phon_link + "sb")
                    and transcription.text is not None
                ):
                    transcriptions.append(transcription.text)
            transcriptions = " ".join(transcriptions)
            id_transcriptions.append(transcriptions)

        # print(id_transcriptions)
        return id_transcriptions

    get_transcriptions()


stop = timeit.default_timer()

print("Time: ", stop - start)

# Old

# id_transcriptions = [
#             transcription.text  # Get transcription
#             for id in ids  # Iterate over ids
#             for transcription in root.findall(  # Get transcription for each unique id
#                 speaker
#                 + str("[@id=" + "'" + id + "'" + "]/")
#                 + ipaTier_model
#                 + "[@form='"
#                 + ipaTier
#                 + "']/"
#                 + transcription_pg
#             )
#             if transcription.tag != str(phon_link + "sb")  # Exclude sb tag and if there is no text
#             and transcription.text is not None
#         ]

# for transcription in id_transcriptions:
#     for letter in transcription:
#         if letter in diacritics_list:
#             diacritics.add(letter)
#             # print(letter, "in diacritic list.")
#         else:
#             not_diacritics.add(letter)
# print(letter, " not in diacritic list.")

# print("diacritics: ", diacritics)
# print("not diacritics: ", not_diacritics)
