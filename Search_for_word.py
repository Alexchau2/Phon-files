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

media_folder = "/Users/pcombiths/Documents/GitHub/Phon-files/XML Files"

os.chdir(media_folder)

# Get XML files
xml_files = [
    xml_file
    for xml_file in listdir(media_folder)
    if isfile(join(media_folder, xml_file))
]

while True:
    word_search = input("What word would you like to search for? ")

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

start = timeit.default_timer()


# start = timeit.default_timer()
phon_link = "{http://phon.ling.mun.ca/ns/phonbank}"
ipaTier_model = str((".//" + phon_link + "ipaTier"))
transcription = str((".//" + phon_link + "w"))
transcription_pg = str((".//" + phon_link + "pg/*"))
orthography_w = str((".//" + phon_link + "g/*"))
speaker = str((".//" + phon_link + "u"))

# Go through all XML files in the directory
for files in xml_files:
    tree = ET.parse(files)
    root = tree.getroot()

    def search_for_word():
        # Get ids

        ids = [id.attrib["id"] for id in root.findall(speaker)]

        # Get transcriptions for each unique id into a list

        word_transcriptions = {}

        # Iterate over ids
        for id in ids:
            transcriptions = []
            forms = []

            # Get transcription for each unique id
            for (
                transcription,
                form,
            ) in zip(  # Iterate over transcriptions and orthographic representation
                root.findall(  # Get word for each unique id
                    speaker + str("[@id=" + "'" + id + "'" + "]/") + orthography_w
                ),
                root.findall(  # Get transcription for each unique id
                    speaker
                    + str("[@id=" + "'" + id + "'" + "]/")
                    + ipaTier_model
                    + "[@form='"
                    + ipaTier
                    + "']/"
                    + transcription_pg
                ),
            ):
                # Exclude sb tag and if there is no text
                if (
                    transcription.tag != str(phon_link + "sb")
                    and transcription.text is not None
                    and form.tag != str(phon_link + "sb")
                    and form.text is not None
                ):
                    transcriptions.append(transcription.text)
                    forms.append(form.text)

            transcriptions = " ".join(transcriptions)
            forms = " ".join(forms)
            word_transcriptions[transcriptions] = forms

        # Search for word in transcriptions
        if word_search in word_transcriptions:
            print(word_search, word_transcriptions[word_search], files)

    search_for_word()

stop = timeit.default_timer()

print("Time: ", stop - start)
