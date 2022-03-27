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

# XML_file = "1007_CCP_CCP Pre.xml"

# for xml_files in media_folder

# Get XML files
xml_files = [
    xml_file
    for xml_file in listdir(media_folder)
    if isfile(join(media_folder, xml_file))
]

# print(xml_files)

while True:

    phoneme_search = input("What phoneme(s) would you like to search for? ")

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

for files in xml_files:

    tree = ET.parse(files)
    root = tree.getroot()

    def search_for_phoneme():

        # Get ids

        # Get ids

        # ids = []

        ids = [id.attrib["id"] for id in root.findall(speaker)]

        # print(ids)

        # for id in root.findall(speaker):
        # ids.append(id.attrib['id'])

        # raw_orthography = speaker + str("[@id=" + "'" + id + "'" + "]/") + orthography_w
        # get_transcription = speaker + str("[@id=" + "'" + id + "'" + "]/") + ipaTier_model + "[@form='" + ipaTier + "']/" + transcription_pg
        # Get transcriptions

        target_id_transcriptions = {}
        actual_id_transcriptions = {}

        # id_transcriptions = [[id for id in ids] for (transcription, form) in zip(raw_orthography, get_transcription) if form.tag != str(phon_link + 'sb') and transcription.text is not None]

        # for id in ids:

        transcriptions = [
            transcription.text
            for id in ids
            for transcription in root.findall(
                speaker
                + str("[@id=" + "'" + id + "'" + "]/")
                + ipaTier_model
                + "[@form='"
                + ipaTier
                + "']/"
                + transcription_pg
            )
            if transcription.tag != str(phon_link + "sb")
            and transcription.text is not None
        ]

        # print(transcriptions)

        words_with_phoneme = [
            word for word in transcriptions if phoneme_search in word
        ]

        print(words_with_phoneme)

        # # Iterate over ids
        # for id in ids:
        #     # print(id)
        #     # same_id_transcriptions = []

        #     # Get child target transcriptions for each unique id
        #     # for transcription in root.findall(speaker + str("[@id=" + "'" + id + "'" + "]/") + orthography_w):

        #     for (transcription, form) in zip(root.findall(speaker + str("[@id=" + "'" + id + "'" + "]/") + orthography_w), root.findall(speaker + str("[@id=" + "'" + id + "'" + "]/") + ipaTier_model + "[@form='" + ipaTier + "']/" + transcription_pg)):

        #     # Exclude tag 'sb'
        #         if form.tag != str(phon_link + 'sb') and transcription.text is not None:
        #             # same_id_transcriptions.append(str(transcription.text))
        #             # joined = " ".join(same_id_transcriptions)

        #             if ipaTier == "model":
        #                 target_id_transcriptions[transcription.text] = form.text
        #             else:
        #                 actual_id_transcriptions[transcription.text] = form.text

        # if ipaTier == "model":
        # print("Target: ", target_id_transcriptions)
        # time.sleep(5)
        # else:
        # print("Actual: ", actual_id_transcriptions)

        # All target or actual transcriptions

        # if ipaTier == "model":
        # return(target_id_transcriptions.values())

        # target_transcriptions = list(target_id_transcriptions.values())
        # print("Target transcriptions: ", target_transcriptions)
        # else:
        # return(actual_id_transcriptions.values())

        # actual_transcriptions = list(actual_id_transcriptions.values())
        # print("Actual transcriptions: ", actual_transcriptions)

        # words_with_phoneme = []

        # # print(phoneme_search)

        # if ipaTier == "model":
        #     for transcriptions in target_id_transcriptions.values():
        #         if transcriptions == None:
        #             skip
        #         else:
        #         # print(transcriptions)
        #         # if word_search == word:
        #             # print(transcriptions)
        #             if phoneme_search in transcriptions:
        #                 words_with_phoneme.append(transcriptions)
        #             # print(target_id_transcriptions[word_search])
        #             else:
        #                 continue

        # elif ipaTier == "actual":
        #     for transcriptions in actual_id_transcriptions.values():
        #         if transcriptions == None:
        #             skip
        #         else:
        #             if phoneme_search in transcriptions:
        #                 words_with_phoneme.append(transcriptions)
        #             # if word_search == word:
        #             # print(actual_id_transcriptions[word_search])
        #             else:
        #                 continue
        # else:
        #     print("Try again.")
        #     # print(i)

        # print(words_with_phoneme)

    search_for_phoneme()

stop = timeit.default_timer()

print("Time: ", stop - start)
