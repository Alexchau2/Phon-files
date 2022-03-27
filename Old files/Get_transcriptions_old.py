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

xml_file = "1007_CCP_CCP Pre.xml"

for files in xml_files:

    tree = ET.parse(files)
    root = tree.getroot()

    def get_transcriptions():

        

        # Get ids

        # ids = [id.attrib['id'] for id in root.findall(speaker)]


        ids = []
        
        for id in root.findall(speaker):
            ids.append(id.attrib['id'])
        
        # Get transcriptions

        target_id_transcriptions = {}
        actual_id_transcriptions = {}

        # transcription_pg = str((".//" + phon_link + "pg/*"))
        
        # Iterate over ids

        # id_transcriptions = [transcription.text for id in ids for transcription in root.findall(speaker + str("[@id=" + "'" + id + "'" + "]/") + ipaTier_model + "[@form='" + ipaTier + "']/" + transcription_pg) if transcription.tag != str(phon_link + 'sb') and transcription.text is not None]

        # print(id_transcriptions)

        for id in ids:

            # Get transcriptions for each unique id
            for transcription in root.findall(speaker + str("[@id=" + "'" + id + "'" + "]/") + ipaTier_model + "[@form='" + ipaTier + "']/" + transcription_pg):

                # Exclude tag 'sb'
                if transcription.tag != str(phon_link + 'sb') and transcription.text is not None:

                    if ipaTier == "model":
                        target_id_transcriptions[id] = transcription.text
                    else:
                        actual_id_transcriptions[id] = transcription.text

        # if ipaTier == "model":
        #     print("Target: ", target_id_transcriptions)
        # else:
        #     print("Actual: ", actual_id_transcriptions)

        # All target or actual transcriptions
        
        if ipaTier == "model":
            print(target_id_transcriptions.values())
            # return(target_id_transcriptions.values())
            # target_transcriptions = list(target_id_transcriptions.values())
            # print("Target transcriptions: ", target_transcriptions.values())
        else:
            # print(id)
            print(actual_id_transcriptions.values())
            # return(target_id_transcriptions.values())
            # actual_transcriptions = list(actual_id_transcriptions.values())
            # print("Actual transcriptions: ", actual_transcriptions)

    get_transcriptions()

# tree = ET.parse(xml_file)
# root = tree.getroot()

# def get_transcriptions():

        

#     # Get ids

#     # ids = [id.attrib['id'] for id in root.findall(speaker)]


#     ids = []
    
#     for id in root.findall(speaker):
#         ids.append(id.attrib['id'])
    
#     # Get transcriptions

#     target_id_transcriptions = {}
#     actual_id_transcriptions = {}

#     # transcription_pg = str((".//" + phon_link + "pg/*"))
    
#     # Iterate over ids

#     # id_transcriptions = [transcription.text for id in ids for transcription in root.findall(speaker + str("[@id=" + "'" + id + "'" + "]/") + ipaTier_model + "[@form='" + ipaTier + "']/" + transcription_pg) if transcription.tag != str(phon_link + 'sb') and transcription.text is not None]

#     # print(id_transcriptions)

#     for id in ids:

#         # Get transcriptions for each unique id
#         for transcription in root.findall(speaker + str("[@id=" + "'" + id + "'" + "]/") + ipaTier_model + "[@form='" + ipaTier + "']/" + transcription_pg):

#             # Exclude tag 'sb'
#             if transcription.tag != str(phon_link + 'sb') and transcription.text is not None:

#                 if ipaTier == "model":
#                     target_id_transcriptions[id] = transcription.text
#                 else:
#                     actual_id_transcriptions[id] = transcription.text

#     # if ipaTier == "model":
#     #     print("Target: ", target_id_transcriptions)
#     # else:
#     #     print("Actual: ", actual_id_transcriptions)

#     # All target or actual transcriptions
    
#     if ipaTier == "model":
#         print(target_id_transcriptions.values())
#         # return(target_id_transcriptions.values())
#         # target_transcriptions = list(target_id_transcriptions.values())
#         # print("Target transcriptions: ", target_transcriptions.values())
#     else:
#         print(id)
#         print(actual_id_transcriptions.values())
#         # return(target_id_transcriptions.values())
#         # actual_transcriptions = list(actual_id_transcriptions.values())
#         # print("Actual transcriptions: ", actual_transcriptions)

# get_transcriptions()

stop = timeit.default_timer()

print('Time: ', stop - start) 