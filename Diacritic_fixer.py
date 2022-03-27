from cgi import test
from cmd import PROMPT
import string
from types import NoneType
from unittest import skip
import xml
import os
from os.path import exists
from os import listdir
from os.path import isfile, join
import xml.etree.ElementTree as ET
import time
import itertools
import timeit
import csv
import openpyxl
import pandas as pd
import xlrd
import re

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

media_folder = "C:\\Users\\alex\\Documents\\GitHub\\Combiths Lab\\AutoPATT\\XML Files"

os.chdir(media_folder)

# Get XML files
xml_files = [
    xml_file
    for xml_file in listdir(media_folder)
    if isfile(join(media_folder, xml_file))
]

while True:

    # Ask for model/target or actual transcription information
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
orthography_w = str((".//" + phon_link + "g/*"))
transcription_indices = str((".//" + phon_link + "sb/*"))
alignment_segmental = str((".//" + phon_link + "alignment"))
transcription_length = str((".//" + phon_link + "ag/*"))

start = timeit.default_timer()

# Go through all XML files in the directory
for files in xml_files:

    tree = ET.parse(files)
    root = tree.getroot()

    def get_transcription_information():

        # Get ids

        ids = [id.attrib["id"] for id in root.findall(speaker)]

        # Get transcriptions

        id_transcriptions = [
            transcription.text  # Get transcription
            for id in ids  # Iterate over ids
            for transcription in root.findall(  # Get transcription for each unique id
                speaker
                + str("[@id=" + "'" + id + "'" + "]/")
                + ipaTier_model
                + "[@form='"
                + ipaTier
                + "']/"
                + transcription_pg
            )
            if transcription.tag != str(phon_link + "sb")  # Exclude sb tag and if there is no text
            and transcription.text is not None
        ]

        diacritic_fix = {
            (id, transcriptions): [ # Dictionary with id and transcription as keys
                list(map(str, index.get("indexes").split())) # Get indexes for phoneme with diacritics
                if len(index.get("indexes")) > 1 # Check if diacritic exists in indexes
                else index.get("indexes") # If there is no diacritic, then just get indexes
                for index in root.findall(
                    speaker
                    + str("[@id=" + "'" + id + "'" + "]/")
                    + ipaTier_model
                    + "[@form='"
                    + ipaTier
                    + "']/"
                    + transcription_indices
                )
            ]
            for (id, transcriptions) in zip(ids, id_transcriptions) # Iterate over ids and transcriptions
        }
        print(diacritic_fix) 

    get_transcription_information()

stop = timeit.default_timer()

print("Time: ", stop - start)
