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
import openpyxl
import xlrd
import re

media_folder = "C:\\Users\\alex\\Documents\\GitHub\\Combiths Lab\\Phon\\XML Files"

os.chdir(media_folder)

# Get XML files
xml_files = [
    xml_file
    for xml_file in listdir(media_folder)
    if isfile(join(media_folder, xml_file))
]

while True:

    # Ask for what phoneme the user would like to search for
    phoneme_search = input("What phoneme(s) would you like to search for? ")

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


start = timeit.default_timer()

# Go through all XML files in the directory
for files in xml_files:

    tree = ET.parse(files)
    root = tree.getroot()

    def search_for_phoneme():

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

        # Search for phoneme in transcriptions
        for word in id_transcriptions:
            if phoneme_search in word:
                print(word)
                return word

    search_for_phoneme()

stop = timeit.default_timer()

print("Time: ", stop - start)

# Old

# transcriptions = [
#     transcription.text # Get transcription
#     for id in ids # Iterate over ids
#     for transcription in root.findall( # Get transcription for each unique id
#         speaker
#         + str("[@id=" + "'" + id + "'" + "]/")
#         + ipaTier_model
#         + "[@form='"
#         + ipaTier
#         + "']/"
#         + transcription_pg
#     )
#     if transcription.tag != str(phon_link + "sb") # Exclude sb tag and if there is no text
#     and transcription.text is not None
# ]

#         # words_with_phoneme = [word for word in id_transcriptions if phoneme_search in word]
