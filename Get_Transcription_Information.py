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

        alignment_values = {
            (id, transcriptions): [
                list(map(int, alignment.get("value").split()))[0] # Get target alignment values
                if alignment.get("value") is not None and ipaTier == "model"
                else list(map(int, alignment.get("value").split()))[1] # Get actual alignment values
                for alignment in root.findall( # Go to alignment tag in XML file
                    speaker
                    + str("[@id=" + "'" + id + "'" + "]/")
                    + alignment_segmental
                    + "[@type='segmental']/"
                    + transcription_length
                )
            ]
            for (id, transcriptions) in zip(ids, id_transcriptions) # Iterate over ids and transcriptions
        }
        # print(alignment_values)

        transcription_info = {
            (id, transcriptions): [
                [index.get("indexes"), index.get("scType"), index.get("hiatus")] # Get info for transcription
                if "hiatus" in index.attrib # Check if hiatus exists
                else [index.get("indexes"), index.get("scType")] # If hiatus does not exist, then only get indexes and scType
                for index in root.findall( # Go to tag where info is (<sb>)
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

        print(transcription_info)

    get_transcription_information()

stop = timeit.default_timer()

print("Time: ", stop - start)
