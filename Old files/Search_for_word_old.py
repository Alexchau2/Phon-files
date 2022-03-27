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
xml_files = [xml_file for xml_file in listdir(media_folder) if isfile(join(media_folder, xml_file))]

# print(xml_files)

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

for files in xml_files:

    tree = ET.parse(files)
    root = tree.getroot()

    def search_for_word():


        # Get ids

        ids = []
        
        for id in root.findall(speaker):
            ids.append(id.attrib['id'])
        
        # Get transcriptions

        target_id_transcriptions = {}
        actual_id_transcriptions = {}

        # Iterate over ids
        for id in ids:
            # print(id)
            # same_id_transcriptions = []

            # Get child target transcriptions for each unique id
            # for transcription in root.findall(speaker + str("[@id=" + "'" + id + "'" + "]/") + orthography_w):

            for (transcription, form) in zip(root.findall(speaker + str("[@id=" + "'" + id + "'" + "]/") + orthography_w), root.findall(speaker + str("[@id=" + "'" + id + "'" + "]/") + ipaTier_model + "[@form='" + ipaTier + "']/" + transcription_pg)):

            # Exclude tag 'sb'
                if form.tag != str(phon_link + 'sb') and transcription.text is not None:
                    # same_id_transcriptions.append(str(transcription.text))
                    # joined = " ".join(same_id_transcriptions)

                    if ipaTier == "model":
                        target_id_transcriptions[transcription.text] = form.text
                    else:
                        actual_id_transcriptions[transcription.text] = form.text

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



        if ipaTier == "model":
            if word_search in target_id_transcriptions:
                # if word_search == word:
                return(target_id_transcriptions[word_search])
            # else:
                # print("Try again.")
                # print(i)
        elif ipaTier == "actual":
            if word_search in actual_id_transcriptions:
                # if word_search == word:
                return(actual_id_transcriptions[word_search])
            # else:
                # print("Try again.")
                # print(i)

    search_for_word()

stop = timeit.default_timer()

print('Time: ', stop - start) 