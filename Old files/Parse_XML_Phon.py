from cgi import test
from cmd import PROMPT
import string
from types import NoneType
from unittest import skip
import xml
import os
from os.path import exists
import xml.etree.ElementTree as ET
import time
import itertools
import timeit
import csv
import openpyxl
import pandas as pd
import xlrd
import re

# while True:

#     # Ask for location of media directory
#     media_folder = input("Input the path of your desired session folder: ")

#     try:

#         # Checks if directory exists
#         if os.path.isdir(media_folder):

#             print(media_folder)

#             os.chdir(media_folder)

#             while True:

#                 # Ask for XML file
#                 XML_file = str(input("Input the name of the XML file that you desire to analyze:") + ".xml")

#                 try:
                
#                     # Check to see if file exists, if not, ask again
#                     if exists(XML_file):
#                         print(XML_file + " exists.")

#                     else:
#                         print("That file does not exist. Please try again.")
#                         continue
            
#                 except:
#                     break

#                 else:
#                     break

#         # Directory does not exist
#         else:
#             print("That folder does not exist. Please try again.")

#     except:
#         break

#     else:
#         break

#C:\Users\alex\Documents\Phon\Media\Test Media\Phil Lab\Disordered Speech
start = timeit.default_timer()
print(os.getcwd())

media_folder = "C:\\Users\\alex\\Documents\\Laptop\\Personal\\Combiths Lab\\Phon Project"

os.chdir(media_folder)

XML_file = "1007_CCP_CCP Pre.xml"

tree = ET.parse(XML_file)
root = tree.getroot()

phon_link = "{http://phon.ling.mun.ca/ns/phonbank}"
# participant = str((".//" + phon_link + "participant"))
speaker = str((".//" + phon_link + "u"))
# child_id = str((".//" + phon_link + "u"))
ipaTier_model = str((".//" + phon_link + "ipaTier"))
transcription = str((".//" + phon_link + "w"))
transcription_pg = str((".//" + phon_link + "pg/*"))

# target_transcriptions = []

# actual_transcriptions = []

# child_ids = []



# for child in root.findall("./" + phon_link + "transcript"):
# for child in root.findall(speaker):
    # print(child)
    # child_ids.append(child.find("./child").attrib['id'])

# print(root.findall(speaker))

# print(child_ids)

# Get child model/target transcriptions
# for target in root.findall(speaker + "[@speaker='CHI']/" + ipaTier_model + "[@form='model']/" + transcription):
    # print(target.text)
    
    # target_transcriptions.append(target.text)


# Get child actual transcriptions
# for actual in root.findall(speaker + "[@speaker='CHI']/" + ipaTier_model + "[@form='actual']/" + transcription):
    # print(actual.text)
    # actual_transcriptions.append(actual.text)

# print(target_transcriptions)
# print(actual_transcriptions)

ids = []
target_id_transcriptions = {}
actual_id_transcriptions = {}


# Get ids
for id_test in root.findall(speaker):
    ids.append(id_test.attrib['id'])

# Iterate over ids
for id in ids:
    same_id_transcriptions = []

    # Get child target transcriptions for each unique id
    for target_id_ in root.findall(speaker + "[@speaker='CHI']/" +str("[@id=" + "'" + id + "'" + "]/") + ipaTier_model + "[@form='model']/" + transcription_pg):
        
        # Exclude tag 'sb'
        if target_id_.tag != str(phon_link + 'sb') and target_id_.text is not None:
            same_id_transcriptions.append(str(target_id_.text))
            joined = " ".join(same_id_transcriptions)
            target_id_transcriptions[id] = joined

# Iterate over ids
for id in ids:
    same_id_transcriptions = []

    # Get child actual transcriptions for each unique id
    for target_id_ in root.findall(speaker + "[@speaker='CHI']/" +str("[@id=" + "'" + id + "'" + "]/") + ipaTier_model + "[@form='actual']/" + transcription_pg):
        
        # Exclude tag 'sb'
        if target_id_.tag != str(phon_link + 'sb') and target_id_.text is not None:
            same_id_transcriptions.append(str(target_id_.text))
            joined = " ".join(same_id_transcriptions)
            actual_id_transcriptions[id] = joined

# print(target_id_transcriptions)
# print(actual_id_transcriptions)

alignment_segmental = str((".//" + phon_link + "alignment"))
transcription_length = str((".//" + phon_link + "ag/*"))
transcription_length_ = str((".//" + phon_link + "alignment/*"))
alignment_target_transcriptions = {}
alignment_actual_transcriptions = {}


# Iterate over ids
for id in ids:
    same_id_values_target = []
    same_id_values_actual = []

    # Get indices for each target and actual transcription
    for length in root.findall(speaker + "[@speaker='CHI']/" +str("[@id=" + "'" + id + "'" + "]/") + alignment_segmental + "[@type='segmental']/" + transcription_length):

        # Skip if None appears
        if length.get('value') is not None:

            # Turn value string into list of integers
            values = length.get('value')
            split_string = values.split()
            map_values = map(int, split_string)
            list_values = list(map_values)

            same_id_values_target.append(list_values[0])
            same_id_values_actual.append(list_values[1])

            # Associate id with target and actual transcription indices
            alignment_target_transcriptions[id] = same_id_values_target
            alignment_actual_transcriptions[id] = same_id_values_actual

        else:
            skip

# print(alignment_target_transcriptions)
# print(alignment_actual_transcriptions)

target_transcriptions_indices = {}
actual_transcriptions_indices = {}

# Associate target transcriptions with their indices
for (transcriptions, indices) in zip(target_id_transcriptions.values(), alignment_target_transcriptions.values()):
    target_transcriptions_indices[transcriptions] = indices

# Associate actual transcriptions with their indices
for (transcriptions, indices) in zip(actual_id_transcriptions.values(), alignment_actual_transcriptions.values()):
    actual_transcriptions_indices[transcriptions] = indices

print(actual_transcriptions_indices)

# print(target_transcriptions_indices.values())
# print(actual_transcriptions_indices)

# The alignments and their lengths in alignment, not in target or actual syllables.
# For example, /wɪndoʊ/ has a length of 6 in target alignment, but has a length of 8
# in alignment due to added spaces (-1) at the end to compensate for alignment
#
# Target syllable: wɪndoʊ (length 6)
# Actual syllable: wɪnoʊdz (length 7)
# Alignment:
# wɪndoʊ(" ")(" ") (length 8)
# wɪn(" ")oʊdz (length 8)
target_transcription_fixed = {}
actual_transcription_fixed = {}

# Iterate over ids
for id in ids:

    # Look at unique id transcriptions for child
    for length in root.findall(speaker + "[@speaker='CHI']/" +str("[@id=" + "'" + id + "'" + "]/") + transcription_length_):
  
        # Exclude alignment lengths that are 0
        if length.get('length') != '0':
            length_value = int(length.get('length')) # Get alignment length

            # Look at each target transcription and their phomap values
            for (transcription, lists) in zip(target_transcriptions_indices, target_transcriptions_indices.values()):

                # Check to see if length of target transcription is less than alignment length
                if len(transcription) < length_value:

                        # Check to see if there is -1 in phomap values
                        if -1 in lists:

                            # Check to see if length of transcription is equal to alignment length
                            if len(transcription) != length_value:
                                
                                # Check to see if there's a space in the syllable/transcription and get rid of it
                                if " " in transcription:
                                    temporary_list_transcription = list(transcription.replace(" ", ""))

                                    # Insert -1 (space) into index of transcription from index of -1 in phomap value list
                                    for j in [i for i, e in enumerate(lists) if e == -1]:

                                        # Making sure there are no spaces
                                        if " " in temporary_list_transcription:

                                            # If there is already a space where index of -1 is, then skip
                                            if temporary_list_transcription.index(" ") == j:
                                                skip

                                            # If not, then put -1 in syllable/transcription
                                            else:
                                                temporary_list_transcription.insert(j, " ")

                                        # If not, then put -1 in syllable/transcription
                                        else:
                                            temporary_list_transcription.insert(j, " ")

                                    # Turn list into string and add to dictionary
                                    temporary_list_transcription = "".join(temporary_list_transcription)
                                    target_transcription_fixed[temporary_list_transcription] = lists

                                # If no space, then convert syllable/transcription to list
                                else:
                                    temporary_list_transcription = list(transcription)

                                    for j in [i for i, e in enumerate(lists) if e == -1]:

                                        if " " in temporary_list_transcription:

                                            if temporary_list_transcription.index(" ") == j:
                                                skip

                                            else:
                                                temporary_list_transcription.insert(j, " ")

                                        else:
                                            temporary_list_transcription.insert(j, " ")

                                    temporary_list_transcription = "".join(temporary_list_transcription)
                                    target_transcription_fixed[temporary_list_transcription] = lists
                    
# Iterate over ids
for id in ids:

    # Look at unique id transcriptions for child
    for length in root.findall(speaker + "[@speaker='CHI']/" +str("[@id=" + "'" + id + "'" + "]/") + transcription_length_):
  
        # Exclude alignment lengths that are 0
        if length.get('length') != '0':
            length_value = int(length.get('length')) # Get alignment length

            # Look at each actual transcription and their phomap values
            for (transcription, lists) in zip(actual_transcriptions_indices, actual_transcriptions_indices.values()):

                # Check to see if length of actual transcription is less than alignment length
                if len(transcription) < length_value:

                        # Check to see if there is -1 in phomap values
                        if -1 in lists:

                            # Check to see if length of transcription is equal to alignment length
                            if len(transcription) != length_value:

                                # Check to see if there's a space in the syllable/transcription and get rid of it
                                if " " in transcription:
                                    temporary_list_transcription = list(transcription.replace(" ", ""))

                                    # Insert -1 (space) into index of transcription from index of -1 in phomap value list
                                    for j in [i for i, e in enumerate(lists) if e == -1]:

                                        # Making sure there are no spaces
                                        if " " in temporary_list_transcription:

                                            # If there is already a space where index of -1 is, then skip
                                            if temporary_list_transcription.index(" ") == j:
                                                skip
                                            
                                            # If not, then put -1 in syllable/transcription
                                            else:
                                                temporary_list_transcription.insert(j, " ")

                                        # If not, then put -1 in syllable/transcription
                                        else:
                                            temporary_list_transcription.insert(j, " ")

                                    # Turn list into string and add to dictionary
                                    temporary_list_transcription = "".join(temporary_list_transcription)
                                    actual_transcription_fixed[temporary_list_transcription] = lists

                                # If no space, then convert syllable/transcription to list
                                else:
                                    temporary_list_transcription = list(transcription)

                                    for j in [i for i, e in enumerate(lists) if e == -1]:

                                        if " " in temporary_list_transcription:

                                            if temporary_list_transcription.index(" ") == j:
                                                skip

                                            else:
                                                temporary_list_transcription.insert(j, " ")

                                        else:
                                            temporary_list_transcription.insert(j, " ")

                                    temporary_list_transcription = "".join(temporary_list_transcription)
                                    actual_transcription_fixed[temporary_list_transcription] = lists

# print(target_transcription_fixed)
# print(actual_transcription_fixed)

liquid_consonants = ['l', 'r', 'ɹ']
vowels = ['u', 'ʊ']

def get_transcriptions():

    speaker = str((".//" + phon_link + "u")) 

    # Get ids

    ids = []
    
    for id_test in root.findall(speaker):
        ids.append(id_test.attrib['id'])
    
    # Get transcriptions

    target_id_transcriptions = {}
    actual_id_transcriptions = {}

    transcription_pg = str((".//" + phon_link + "pg/*"))

    while True:

        ipaTier = input("Model (target) or actual transcription? ")

    # while True:
        # try:
        if ipaTier == "model":
            print("Model")
            # return ipaTier
            # skip
            break
            
        elif ipaTier == "actual":
            print("Actual")
            # return ipaTier
            # skip
            # print("Please select either model (target) or actual.")
            break
            
        else:
            print("Please select either model (target) or actual. ")
            continue
                # continue

            # except:
                # break
                # skip
            # else:
                # break
    
    # Iterate over ids
    for id in ids:
        # print(id)
        same_id_transcriptions = []
        # Get transcriptions for each unique id
        for target_id_ in root.findall(speaker + str("[@id=" + "'" + id + "'" + "]/") + ipaTier_model + "[@form='" + ipaTier + "']/" + transcription_pg):
            # print(target_id_)
            # Exclude tag 'sb'
            if target_id_.tag != str(phon_link + 'sb') and target_id_.text is not None:
                print(target_id_.text)
                same_id_transcriptions.append(str(target_id_.text))
                joined = " ".join(same_id_transcriptions)


                if ipaTier == "model":
                    target_id_transcriptions[id] = joined
    # print("Target: ", target_id_transcriptions)
                else:
                    actual_id_transcriptions[id] = joined
    # print("Actual: ", actual_id_transcriptions)

    if ipaTier == "model":
        print("Target: ", target_id_transcriptions)
    else:
        print("Actual: ", actual_id_transcriptions)

    # All target or actual transcriptions
    
    if ipaTier == "model":
        target_transcriptions = list(target_id_transcriptions.values())
        print("Target transcriptions: ", target_transcriptions)
    else:
        actual_transcriptions = list(actual_id_transcriptions.values())
        print("Actual transcriptions: ", actual_transcriptions)
    
# get_transcriptions()

def search_for_word():

    speaker = str((".//" + phon_link + "u")) 

    # Get ids

    ids = []
    
    for id_test in root.findall(speaker):
        ids.append(id_test.attrib['id'])
    
    # Get transcriptions

    target_id_transcriptions = {}
    actual_id_transcriptions = {}

    transcription_pg = str((".//" + phon_link + "pg/*"))
    orthography_w = str((".//" + phon_link + "g/*"))

    # while True:

    ipaTier = input("Model (target) or actual transcription? ")
    # try:
    if ipaTier == "model":
        print("Model")
        # return ipaTier
        # skip
        
    elif ipaTier == "actual":
        print("Actual")
        # return ipaTier
        # skip
        # print("Please select either model (target) or actual.")
        
    else:
        print("Please select either model (target) or actual. ")
                # continue

            # except:
                # break
                # skip
            # else:
                # break
    
    # Iterate over ids
    # for id in ids:
    #     # print(id)
    #     same_id_transcriptions = []

    #     # Get child target transcriptions for each unique id
    #     for target_id_ in root.findall(speaker + str("[@id=" + "'" + id + "'" + "]/") + ipaTier_model + "[@form='" + ipaTier + "']/" + transcription_pg):
    #         # print(target_id_)
    #         # Exclude tag 'sb'
    #         if target_id_.tag != str(phon_link + 'sb') and target_id_.text is not None:
    #             same_id_transcriptions.append(str(target_id_.text))
    #             joined = " ".join(same_id_transcriptions)

    #             if ipaTier == "model":
    #                 target_id_transcriptions[id] = joined
    # # print("Target: ", target_id_transcriptions)
    #             else:
    #                 actual_id_transcriptions[id] = joined
    # print("Actual: ", actual_id_transcriptions)

    # Iterate over ids
    for id in ids:
        # print(id)
        same_id_transcriptions = []

        # Get child target transcriptions for each unique id
        for target_id_ in root.findall(speaker + str("[@id=" + "'" + id + "'" + "]/") + orthography_w):

            for form in root.findall(speaker + str("[@id=" + "'" + id + "'" + "]/") + ipaTier_model + "[@form='" + ipaTier + "']/" + transcription_pg):

            # Exclude tag 'sb'
                if form.tag != str(phon_link + 'sb') and target_id_.text is not None:
                    same_id_transcriptions.append(str(target_id_.text))
                    joined = " ".join(same_id_transcriptions)

                    if ipaTier == "model":
                        target_id_transcriptions[joined] = form.text
                    else:
                        actual_id_transcriptions[joined] = form.text

    if ipaTier == "model":
        print("Target: ", target_id_transcriptions)
    else:
        print("Actual: ", actual_id_transcriptions)

    # All target or actual transcriptions
    
    if ipaTier == "model":
        target_transcriptions = list(target_id_transcriptions.values())
        # print("Target transcriptions: ", target_transcriptions)
    else:
        actual_transcriptions = list(actual_id_transcriptions.values())
        # print("Actual transcriptions: ", actual_transcriptions)

    while True:

        word_search = input("What word would you like to search for? ")

        if ipaTier == "model":
            if word_search in target_id_transcriptions:
                # if word_search == word:
                print(target_id_transcriptions[word_search])
                break
            else:
                print("Try again.")
                continue
                # print(i)
        elif ipaTier == "actual":
            if word_search in actual_id_transcriptions:
                # if word_search == word:
                print(actual_id_transcriptions[word_search])
                break
            else:
                print("Try again.")
                continue
                # print(i)

# search_for_word()

def search_for_phoneme():

    speaker = str((".//" + phon_link + "u")) 

    # Get ids

    ids = []
    
    for id_test in root.findall(speaker):
        ids.append(id_test.attrib['id'])
    
    # Get transcriptions

    target_id_transcriptions = {}
    actual_id_transcriptions = {}

    transcription_pg = str((".//" + phon_link + "pg/*"))
    orthography_w = str((".//" + phon_link + "g/*"))

    # while True:

    ipaTier = input("Model (target) or actual transcription? ")
    # try:
    if ipaTier == "model":
        print("Model")
        # return ipaTier
        # skip
        
    elif ipaTier == "actual":
        print("Actual")
        # return ipaTier
        # skip
        # print("Please select either model (target) or actual.")
        
    else:
        print("Please select either model (target) or actual. ")
                # continue

            # except:
                # break
                # skip
            # else:
                # break
    
    # Iterate over ids
    # for id in ids:
    #     # print(id)
    #     same_id_transcriptions = []

    #     # Get child target transcriptions for each unique id
    #     for target_id_ in root.findall(speaker + str("[@id=" + "'" + id + "'" + "]/") + ipaTier_model + "[@form='" + ipaTier + "']/" + transcription_pg):
    #         # print(target_id_)
    #         # Exclude tag 'sb'
    #         if target_id_.tag != str(phon_link + 'sb') and target_id_.text is not None:
    #             same_id_transcriptions.append(str(target_id_.text))
    #             joined = " ".join(same_id_transcriptions)

    #             if ipaTier == "model":
    #                 target_id_transcriptions[id] = joined
    # # print("Target: ", target_id_transcriptions)
    #             else:
    #                 actual_id_transcriptions[id] = joined
    # print("Actual: ", actual_id_transcriptions)

    # Iterate over ids
    for id in ids:
        # print(id)
        same_id_transcriptions = []

        # Get child target transcriptions for each unique id
        for target_id_ in root.findall(speaker + str("[@id=" + "'" + id + "'" + "]/") + orthography_w):

            for form in root.findall(speaker + str("[@id=" + "'" + id + "'" + "]/") + ipaTier_model + "[@form='" + ipaTier + "']/" + transcription_pg):

            # Exclude tag 'sb'
                if form.tag != str(phon_link + 'sb') and target_id_.text is not None:
                    same_id_transcriptions.append(str(target_id_.text))
                    joined = " ".join(same_id_transcriptions)

                    if ipaTier == "model":
                        target_id_transcriptions[joined] = form.text
                    else:
                        actual_id_transcriptions[joined] = form.text

    if ipaTier == "model":
        print("Target: ", target_id_transcriptions)
    else:
        print("Actual: ", actual_id_transcriptions)

    # All target or actual transcriptions
    
    if ipaTier == "model":
        target_transcriptions = list(target_id_transcriptions.values())
        # print("Target transcriptions: ", target_transcriptions)
    else:
        actual_transcriptions = list(actual_id_transcriptions.values())
        # print("Actual transcriptions: ", actual_transcriptions)

    words_with_phoneme = []

    while True:

        phoneme_search = input("What phoneme would you like to search for? ")
        print(phoneme_search)

        if ipaTier == "model":
            for transcriptions in target_id_transcriptions.values():
                # print(transcriptions)
                # if word_search == word:
                if phoneme_search in transcriptions:
                    words_with_phoneme.append(transcriptions)
                # print(target_id_transcriptions[word_search])
            break

        elif ipaTier == "actual":
            for transcriptions in actual_id_transcriptions.values():

                if phoneme_search in transcriptions:
                    words_with_phoneme.append(transcriptions)
                # if word_search == word:
                # print(actual_id_transcriptions[word_search])
            break
        else:
            print("Try again.")
            continue
            # print(i)
        
    print(words_with_phoneme)

def get_transcription_information():

    ipaTier_model = str((".//" + phon_link + "ipaTier"))

    transcription_indices = str((".//" + phon_link + "sb/*"))


    while True:

        ipaTier = input("Model (target) or actual transcription? ")
        # try:
        if ipaTier == "model":
            print("Model")
            # return ipaTier
            break
            
        elif ipaTier == "actual":
            print("Actual")
            # return ipaTier
            break
            # print("Please select either model (target) or actual.")
            
        else:
            print("Please select either model (target) or actual. ")
            continue

        # except:
            # break
        # else:
            # break
    
    # while True:

    #     index = input("Which index of the transcription? Put a number more than 0. ")

    #     # try:
    #     if int(index) < 0:
    #         # print(type(index))
    #         print("Please put in a number more than 0.")
    #         continue
    #     else:
    #         # return index
    #         break
    #     # except:
    #     #     break

    #     # else:
    #     #     break

    # while True:

    #     scType = input("Onset, nucleus, coda, word boundary, or RA? ")

    #     # try:
    #     if scType == "Onset":
    #         scType = "O"
    #         break
    #     elif scType == "nucleus":
    #         scType = "N"
    #         break
    #     elif scType == "coda":
    #         scType = "C"
    #         break
    #     elif scType == "word boundary":
    #         scType = "WB"
    #         break
    #     elif scType == "RA":
    #         scType = "RA"
    #         break
    #     else:
    #         print("Please select either onset, nucleus, coda, word boundary, or RA.")
    #         continue
        # except:
        #     break

        # else:
        #     break
        
    speaker = str((".//" + phon_link + "u")) 

    # Get ids

    ids = []
    target_ids = []
    actual_ids = []

    for id_test in root.findall(speaker):
            ids.append(id_test.attrib['id'])

    # for id in ids:
    #     # print(id.attrib['id'])
    #     # time.sleep(1)
    #     for form in root.findall(speaker + str("[@id=" + "'" + id + "'" + "]/") + ipaTier_model + "[@form='" + ipaTier + "']/"):
    #         # print(form.attrib['form'])
    #         # print(form)
    #         # time.sleep(1)
    #         if ipaTier == "model":
    #             target_ids.append(id)
    #         elif ipaTier == "actual":
    #             actual_ids.append(id)

    # print(target_ids)

    
    
    # Get transcriptions

    target_id_transcriptions = {}
    actual_id_transcriptions = {}

    transcription_pg = str((".//" + phon_link + "pg/*"))
    orthography_w = str((".//" + phon_link + "g/*"))

    # Iterate over ids
    for id in ids:
        # print(id)
        same_id_transcriptions = []
        # Get transcriptions for each unique id
        for target_id_ in root.findall(speaker + str("[@id=" + "'" + id + "'" + "]/") + ipaTier_model + "[@form='" + ipaTier + "']/" + transcription_pg):
            # print(target_id_)
            # Exclude tag 'sb'
            if target_id_.tag != str(phon_link + 'sb') and target_id_.text is not None:
                print(target_id_.text)
                same_id_transcriptions.append(str(target_id_.text))
                joined = " ".join(same_id_transcriptions)


                if ipaTier == "model":
                    target_id_transcriptions[id] = joined
    # print("Target: ", target_id_transcriptions)
                else:
                    actual_id_transcriptions[id] = joined
    # print("Actual: ", actual_id_transcriptions)

    # # Iterate over ids
    # for id in ids:
    #     # print(id)
    #     same_id_transcriptions = []

    #     # Get child target transcriptions for each unique id
    #     for target_id_ in root.findall(speaker + str("[@id=" + "'" + id + "'" + "]/") + orthography_w):

    #         # for form in root.findall(speaker + str("[@id=" + "'" + id + "'" + "]/") + ipaTier_model + "[@form='" + ipaTier + "']/" + transcription_pg):

    #         # Exclude tag 'sb'
    #         if target_id_.tag != str(phon_link + 'sb') and target_id_.text is not None:
    #             same_id_transcriptions.append(str(target_id_.text))
    #             joined = " ".join(same_id_transcriptions)

    #             if ipaTier == "model":
    #                 target_id_transcriptions[joined] = target_id_.text
    #             else:
    #                 actual_id_transcriptions[joined] = target_id_.text

    if ipaTier == "model":
        print("Target: ", target_id_transcriptions)
    else:
        print("Actual: ", actual_id_transcriptions)

    # All target or actual transcriptions
    
    if ipaTier == "model":
        target_transcriptions = list(target_id_transcriptions.values())
        print("Target transcriptions: ", target_transcriptions)
    else:
        actual_transcriptions = list(actual_id_transcriptions.values())
        # print("Actual transcriptions: ", actual_transcriptions)

    words_with_phoneme = []
    phoneme_index_scType = {}

    while True:

        phoneme_search = input("What phoneme would you like to search for? ")
        print(phoneme_search)
            

        if ipaTier == "model":
            # for id in ids:
            for (id, transcriptions) in zip(ids, target_transcriptions):
                # for transcriptions in target_transcriptions:
                if phoneme_search in transcriptions:
                    # words_with_phoneme.append(transcriptions)
                        # print(words_with_phoneme)
                    # for id in ids:
                        # print(id)
                    indexes_list = []
                    scType_list = []
                    hiatus_list = []
                    hiatus_index = []
                    for index in root.findall(speaker + str("[@id=" + "'" + id + "'" + "]/") + ipaTier_model + "[@form='" + ipaTier + "']/" + transcription_indices):                        
                        
                        if "hiatus" in index.attrib:
                            indexes = index.get('indexes')
                            indexes_list.append(indexes)
                            scType_ = index.get('scType')
                            scType_list.append(scType_)
                            hiatus_ = index.get('hiatus')
                            hiatus_list.append(hiatus_)

                            hiatus_index.append(indexes)
                            # for words in words_with_phoneme:
                                # print(words)
                            phoneme_index_scType[transcriptions] = [indexes_list, scType_list, hiatus_list, hiatus_index]
                        else:
                            indexes = index.get('indexes')
                            indexes_list.append(indexes)
                            scType_ = index.get('scType')
                            scType_list.append(scType_)
                            # for words in words_with_phoneme:
                            phoneme_index_scType[transcriptions] = [indexes_list, scType_list,hiatus_list, hiatus_index]
                            continue
                            
            
        elif ipaTier == "actual":
            # for id in ids:
            for (id, transcriptions) in zip(ids, actual_transcriptions):
                # for transcriptions in target_transcriptions:
                if phoneme_search in transcriptions:
                    # words_with_phoneme.append(transcriptions)
                        # print(words_with_phoneme)
                    # for id in ids:
                        # print(id)
                    indexes_list = []
                    scType_list = []
                    hiatus_list = []
                    hiatus_index = []
                    for index in root.findall(speaker + str("[@id=" + "'" + id + "'" + "]/") + ipaTier_model + "[@form='" + ipaTier + "']/" + transcription_indices):                        
                        
                        if "hiatus" in index.attrib:
                            indexes = index.get('indexes')
                            indexes_list.append(indexes)
                            scType_ = index.get('scType')
                            scType_list.append(scType_)
                            hiatus_ = index.get('hiatus')
                            hiatus_list.append(hiatus_)

                            hiatus_index.append(indexes)
                            # for words in words_with_phoneme:
                                # print(words)
                            phoneme_index_scType[transcriptions] = [indexes_list, scType_list, hiatus_list, hiatus_index]
                        else:
                            indexes = index.get('indexes')
                            indexes_list.append(indexes)
                            scType_ = index.get('scType')
                            scType_list.append(scType_)
                            # for words in words_with_phoneme:
                            phoneme_index_scType[transcriptions] = [indexes_list, scType_list,hiatus_list, hiatus_index]
                            continue
                
        else:
            print("Try again.")
            continue
        break


    print(phoneme_index_scType)


    # for id in ids:

    # alignment_target_transcriptions = {}
    # alignment_actual_transcriptions = {}


    # Iterate over ids
    # for id in ids:
    #     same_id_values_target = []
    #     same_id_values_actual = []

    #     # Get indices for each target and actual transcription
    #     for length in root.findall(speaker + str("[@id=" + "'" + id + "'" + "]/") + alignment_segmental + "[@type='segmental']/" + transcription_length):

    #         # Skip if None appears
    #         if length.get('value') is not None:

    #             # Turn value string into list of integers
    #             values = length.get('value')
    #             split_string = values.split()
    #             map_values = map(int, split_string)
    #             list_values = list(map_values)

    #             same_id_values_target.append(list_values[0])
    #             same_id_values_actual.append(list_values[1])

    #             # Associate id with target and actual transcription indices
    #             alignment_target_transcriptions[id] = same_id_values_target
    #             alignment_actual_transcriptions[id] = same_id_values_actual

    #         else:
    #             skip

    # print(alignment_target_transcriptions)
    # print(alignment_actual_transcriptions)

    # target_transcriptions_indices = {}
    # actual_transcriptions_indices = {}

    # # Associate target transcriptions with their indices
    # for (transcriptions, indices) in zip(target_id_transcriptions.values(), alignment_target_transcriptions.values()):
    #     target_transcriptions_indices[transcriptions] = indices

    # # Associate actual transcriptions with their indices
    # for (transcriptions, indices) in zip(actual_id_transcriptions.values(), alignment_actual_transcriptions.values()):
    #     actual_transcriptions_indices[transcriptions] = indices

    
# get_transcription_information()

def get_transcription_phoneme_information():

    ipaTier_model = str((".//" + phon_link + "ipaTier"))

    transcription_indices = str((".//" + phon_link + "sb/*"))


    while True:

        ipaTier = input("Model (target) or actual transcription? ")
        # try:
        if ipaTier == "model":
            print("Model")
            # return ipaTier
            break
            
        elif ipaTier == "actual":
            print("Actual")
            # return ipaTier
            break
            # print("Please select either model (target) or actual.")
            
        else:
            print("Please select either model (target) or actual. ")
            continue

        # except:
            # break
        # else:
            # break
    
    # while True:

    #     index = input("Which index of the transcription? Put a number more than 0. ")

    #     # try:
    #     if int(index) < 0:
    #         # print(type(index))
    #         print("Please put in a number more than 0.")
    #         continue
    #     else:
    #         # return index
    #         break
    #     # except:
    #     #     break

    #     # else:
    #     #     break

    # while True:

    #     scType = input("Onset, nucleus, coda, word boundary, or RA? ")

    #     # try:
    #     if scType == "Onset":
    #         scType = "O"
    #         break
    #     elif scType == "nucleus":
    #         scType = "N"
    #         break
    #     elif scType == "coda":
    #         scType = "C"
    #         break
    #     elif scType == "word boundary":
    #         scType = "WB"
    #         break
    #     elif scType == "RA":
    #         scType = "RA"
    #         break
    #     else:
    #         print("Please select either onset, nucleus, coda, word boundary, or RA.")
    #         continue
        # except:
        #     break

        # else:
        #     break
        
    speaker = str((".//" + phon_link + "u")) 

    # Get ids

    ids = []
    target_ids = []
    actual_ids = []

    for id_test in root.findall(speaker):
            ids.append(id_test.attrib['id'])

    # for id in ids:
    #     # print(id.attrib['id'])
    #     # time.sleep(1)
    #     for form in root.findall(speaker + str("[@id=" + "'" + id + "'" + "]/") + ipaTier_model + "[@form='" + ipaTier + "']/"):
    #         # print(form.attrib['form'])
    #         # print(form)
    #         # time.sleep(1)
    #         if ipaTier == "model":
    #             target_ids.append(id)
    #         elif ipaTier == "actual":
    #             actual_ids.append(id)

    # print(target_ids)

    
    
    # Get transcriptions

    target_id_transcriptions = {}
    actual_id_transcriptions = {}

    transcription_pg = str((".//" + phon_link + "pg/*"))
    orthography_w = str((".//" + phon_link + "g/*"))

    # Iterate over ids
    for id in ids:
        # print(id)
        same_id_transcriptions = []
        # Get transcriptions for each unique id
        for target_id_ in root.findall(speaker + str("[@id=" + "'" + id + "'" + "]/") + ipaTier_model + "[@form='" + ipaTier + "']/" + transcription_pg):
            # print(target_id_)
            # Exclude tag 'sb'
            if target_id_.tag != str(phon_link + 'sb') and target_id_.text is not None:
                print(target_id_.text)
                same_id_transcriptions.append(str(target_id_.text))
                joined = " ".join(same_id_transcriptions)


                if ipaTier == "model":
                    target_id_transcriptions[id] = joined
    # print("Target: ", target_id_transcriptions)
                else:
                    actual_id_transcriptions[id] = joined
    # print("Actual: ", actual_id_transcriptions)

    # # Iterate over ids
    # for id in ids:
    #     # print(id)
    #     same_id_transcriptions = []

    #     # Get child target transcriptions for each unique id
    #     for target_id_ in root.findall(speaker + str("[@id=" + "'" + id + "'" + "]/") + orthography_w):

    #         # for form in root.findall(speaker + str("[@id=" + "'" + id + "'" + "]/") + ipaTier_model + "[@form='" + ipaTier + "']/" + transcription_pg):

    #         # Exclude tag 'sb'
    #         if target_id_.tag != str(phon_link + 'sb') and target_id_.text is not None:
    #             same_id_transcriptions.append(str(target_id_.text))
    #             joined = " ".join(same_id_transcriptions)

    #             if ipaTier == "model":
    #                 target_id_transcriptions[joined] = target_id_.text
    #             else:
    #                 actual_id_transcriptions[joined] = target_id_.text

    if ipaTier == "model":
        print("Target: ", target_id_transcriptions)
    else:
        print("Actual: ", actual_id_transcriptions)

    # All target or actual transcriptions
    
    if ipaTier == "model":
        target_transcriptions = list(target_id_transcriptions.values())
        print("Target transcriptions: ", target_transcriptions)
    else:
        actual_transcriptions = list(actual_id_transcriptions.values())
        # print("Actual transcriptions: ", actual_transcriptions)

    alignment_segmental = str((".//" + phon_link + "alignment"))

    alignment_target_transcriptions = {}
    alignment_target_transcriptions = {}

    # Iterate over ids
    for id in ids:
        same_id_values_target = []
        same_id_values_actual = []

        # Get indices for each target and actual transcription
        for length in root.findall(speaker + str("[@id=" + "'" + id + "'" + "]/") + alignment_segmental + "[@type='segmental']/" + transcription_length):

            # Skip if None appears
            if length.get('value') is not None:

                # Turn value string into list of integers
                values = length.get('value')
                split_string = values.split()
                map_values = map(int, split_string)
                list_values = list(map_values)

                same_id_values_target.append(list_values[0])
                same_id_values_actual.append(list_values[1])

                # Associate id with target and actual transcription indices
                alignment_target_transcriptions[id] = same_id_values_target
                alignment_actual_transcriptions[id] = same_id_values_actual

            else:
                skip

    # print(alignment_target_transcriptions)

    words_with_phoneme = []
    phoneme_index_scType = {}

    while True:

        phoneme_search = input("What phoneme would you like to search for? ")
        print(phoneme_search)
            

        if ipaTier == "model":
            # for id in ids:
            for (id, transcriptions, alignment_id, value) in zip(ids, target_transcriptions, alignment_target_transcriptions, alignment_target_transcriptions.values()):
                if id != alignment_id:
                    continue
                else:
                # for transcriptions in target_transcriptions:
                    if phoneme_search in transcriptions:
                        # words_with_phoneme.append(transcriptions)
                            # print(words_with_phoneme)
                        # for id in ids:
                            # print(id)
                        indexes_list = []
                        scType_list = []
                        hiatus_list = []
                        hiatus_index = []
                        for index in root.findall(speaker + str("[@id=" + "'" + id + "'" + "]/") + ipaTier_model + "[@form='" + ipaTier + "']/" + transcription_indices):                        
                            
                            if "hiatus" in index.attrib:
                                indexes = index.get('indexes')
                                indexes_list.append(indexes)
                                scType_ = index.get('scType')
                                scType_list.append(scType_)
                                hiatus_ = index.get('hiatus')
                                hiatus_list.append(hiatus_)

                                hiatus_index.append(indexes)
                                # for words in words_with_phoneme:
                                    # print(words)
                                
                                phoneme_index_scType[transcriptions] = [indexes_list, scType_list, hiatus_list, hiatus_index, value]
                            else:
                                indexes = index.get('indexes')
                                indexes_list.append(indexes)
                                scType_ = index.get('scType')
                                scType_list.append(scType_)
                                # for words in words_with_phoneme:
                                phoneme_index_scType[transcriptions] = [indexes_list, scType_list,hiatus_list, hiatus_index, value]
                                continue
                            
            
        elif ipaTier == "actual":
            # for id in ids:
            for (id, transcriptions, alignment_id, value) in zip(ids, actual_transcriptions, alignment_actual_transcriptions, alignment_actual_transcriptions.values()):
                if id != alignment_id:
                    continue
                else:
                    if phoneme_search in transcriptions:
                        # words_with_phoneme.append(transcriptions)
                            # print(words_with_phoneme)
                        # for id in ids:
                            # print(id)
                        indexes_list = []
                        scType_list = []
                        hiatus_list = []
                        hiatus_index = []
                        for index in root.findall(speaker + str("[@id=" + "'" + id + "'" + "]/") + ipaTier_model + "[@form='" + ipaTier + "']/" + transcription_indices):                        
                            
                            if "hiatus" in index.attrib:
                                indexes = index.get('indexes')
                                indexes_list.append(indexes)
                                scType_ = index.get('scType')
                                scType_list.append(scType_)
                                hiatus_ = index.get('hiatus')
                                hiatus_list.append(hiatus_)

                                hiatus_index.append(indexes)
                                # for words in words_with_phoneme:
                                    # print(words)
                                phoneme_index_scType[transcriptions] = [indexes_list, scType_list, hiatus_list, hiatus_index, value]
                            else:
                                indexes = index.get('indexes')
                                indexes_list.append(indexes)
                                scType_ = index.get('scType')
                                scType_list.append(scType_)
                                # for words in words_with_phoneme:
                                phoneme_index_scType[transcriptions] = [indexes_list, scType_list,hiatus_list, hiatus_index, value]
                                continue
                    
        else:
            print("Try again.")
            continue
        break


    print("Phoneme_index_scType: ", phoneme_index_scType)

    phoneme_info = {}

    # while True:

    #     phoneme_search = input("What phoneme in the word would you like to search for? ")

    #     if len(phoneme_search) > 1:
    #         print("Please only put one phoneme.")
    #         continue
    #     else:
    #         # print(phoneme_search)
    #         for (words, values) in zip(phoneme_index_scType, phoneme_index_scType.values()):
    #             print(words)
    #             print(values)
    #             print(words[0], words[1])
    #             time.sleep(0.1)
    #             # phoneme_info = {}
    #             info = []
    #             phoneme_indices = []
    #             indexes_index = []
    #             if phoneme_search in words:
    #                 for indexes in values[0]:
    #                     print(indexes)
    #                     if len(indexes) > 1:
    #                         print("more than 1.")
    #                         temp_list = list(indexes)
    #                         for elements in temp_list:
    #                             if elements.strip():
    #                                 # values[0].remove(indexes)
    #                                 values[0].append(elements)
    #                                 print(values[0])
    #                                 # indices = 
    #                         # values[0].remove(indexes)
    #                         indexes_index.append(values[0].index(indexes))
    #                         values[0].remove(indexes)
    #                         print("indexes_index: ", indexes_index)
    #                 # print(words.index(phoneme_search))
    #                 # if words.find(phoneme_search) > 1:

    #                 # phoneme_index = words.index(phoneme_search)
    #                         for m in re.finditer(phoneme_search, words):
    #                             phoneme_index = m.start()
    #                             phoneme_indices.append(phoneme_index)
    #                         # print(words)
    #                         # print(phoneme_indices)
    #                         # time.sleep(0.1)
    #                         # else:
    #                             # phoneme_index = words.index(phoneme_search)
    #                         # print(phoneme_index)
    #                         # print(phoneme_index)
    #                         # for values in phoneme_index_scType.values():
    #                             # print(values)
    #                             # for lists in values:
    #                                 # print(lists)
    #                                 # for i in range(len(lists))
    #                         indices = values[0]
    #                         print("indices: ", indices)
    #                         scTypes = values[1]
    #                         hiatus = values[2]
    #                         hiatus_index = values[3]
    #                         for each_index in phoneme_indices:
    #                             print("phoneme_indices: ", phoneme_indices)
    #                             print("each_index: ", each_index)
    #                             # if len(words) > each_index:
    #                                 # info.append(indices[each_index - 1])
    #                                 # info.append(scTypes[each_index - 1])
    #                             # elif len(words) == each_index:
    #                             # else:
    #                             info.append(indices[each_index])
    #                             info.append(scTypes[indexes_index[0]])
    #                             # print(hiatus_index)
    #                             # print(len(hiatus_index))
    #                             # time.sleep(1)
    #                             if len(hiatus_index) > 1:
    #                                 len_hiatus_index = len(words)
    #                                 for i in range(len(hiatus_index)):
    #                                     # print(words)
    #                                     # print(i)
    #                                     # time.sleep(0.1)
    #                                     if len(hiatus_index[i]) > 1:
    #                                         len_hiatus_index -= 1
    #                                         # print("word length: ", len_hiatus_index)
    #                                         try:
    #                                             info.append(hiatus[i])
    #                                             info.append(hiatus_index[i])
    #                                         except:
    #                                             continue
    #                                     # print(i)
    #                                     elif int(hiatus_index[i]) == each_index: 
    #                                         # print("success")
    #                                         info.append(hiatus[i])
    #                                         info.append(hiatus_index[i])
    #                             elif len(hiatus_index) == 1:
    #                                 len_hiatus_index = len(words)
    #                                 for i in range(len(hiatus_index)):
    #                                     if len(hiatus_index[i]) > 1:
    #                                         len_hiatus_index -= 1
    #                                         # print("word length: ", len_hiatus_index)
    #                                         try:
    #                                             info.append(hiatus[i])
    #                                             info.append(hiatus_index[i])
    #                                         except:
    #                                             continue
    #                                     elif int(hiatus_index[i]) == each_index: 
    #                                         info.append(hiatus[i])
    #                                         info.append(hiatus_index[i])
    #                             # :
    #                                 # for i in range(len(hiatus_index)):
    #                                     # if 
    #                             phoneme_info[words] = info
    #                             print(phoneme_info)
    #                             # print(phoneme_info)
    #                                     # print(lists[phoneme_index])
    #                                 # for i in range(len(words)):
    #                                 # for j in range(len(phoneme_index_scType.values()[i])):
    #                                 # print(phoneme_index_scType.values()[i])
    #                     else:
    #                         for m in re.finditer(phoneme_search, words):
    #                             phoneme_index = m.start()
    #                             phoneme_indices.append(phoneme_index)
    #                         # print(words)
    #                         # print(phoneme_indices)
    #                         # time.sleep(0.1)
    #                         # else:
    #                             # phoneme_index = words.index(phoneme_search)
    #                         # print(phoneme_index)
    #                         # print(phoneme_index)
    #                         # for values in phoneme_index_scType.values():
    #                             # print(values)
    #                             # for lists in values:
    #                                 # print(lists)
    #                                 # for i in range(len(lists))
    #                             indices = values[0]
    #                             print("indices: ", indices)
    #                             scTypes = values[1]
    #                             hiatus = values[2]
    #                             hiatus_index = values[3]
    #                             for each_index in phoneme_indices:
    #                                 print("phoneme_indices: ", phoneme_indices)
    #                                 print("each_index: ", each_index)
    #                                 # if len(words) > each_index:
    #                                     # info.append(indices[each_index - 1])
    #                                     # info.append(scTypes[each_index - 1])
    #                                 # elif len(words) == each_index:
    #                                 # else:
    #                                 info.append(indices[each_index])
    #                                 info.append(scTypes[each_index])
    #                                 # print(hiatus_index)
    #                                 # print(len(hiatus_index))
    #                                 # time.sleep(1)
    #                                 if len(hiatus_index) > 1:
    #                                     len_hiatus_index = len(words)
    #                                     for i in range(len(hiatus_index)):
    #                                         # print(words)
    #                                         # print(i)
    #                                         # time.sleep(0.1)
    #                                         if len(hiatus_index[i]) > 1:
    #                                             len_hiatus_index -= 1
    #                                             # print("word length: ", len_hiatus_index)
    #                                             try:
    #                                                 info.append(hiatus[i])
    #                                                 info.append(hiatus_index[i])
    #                                             except:
    #                                                 continue
    #                                         # print(i)
    #                                         elif int(hiatus_index[i]) == each_index: 
    #                                             # print("success")
    #                                             info.append(hiatus[i])
    #                                             info.append(hiatus_index[i])
    #                                 elif len(hiatus_index) == 1:
    #                                     len_hiatus_index = len(words)
    #                                     for i in range(len(hiatus_index)):
    #                                         if len(hiatus_index[i]) > 1:
    #                                             len_hiatus_index -= 1
    #                                             # print("word length: ", len_hiatus_index)
    #                                             try:
    #                                                 info.append(hiatus[i])
    #                                                 info.append(hiatus_index[i])
    #                                             except:
    #                                                 continue
    #                                         elif int(hiatus_index[i]) == each_index: 
    #                                             info.append(hiatus[i])
    #                                             info.append(hiatus_index[i])
    #                                 # :
    #                                     # for i in range(len(hiatus_index)):
    #                                         # if 
    #                                 phoneme_info[words] = info
    #                                 print(phoneme_info)
    #                                 # print(phoneme_info)
    #                                         # print(lists[phoneme_index])
    #                                     # for i in range(len(words)):
    #                                     # for j in range(len(phoneme_index_scType.values()[i])):
    #                                     # print(phoneme_index_scType.values()[i])
    #             else:
    #                 print("Try again.")
    #                 continue

    #         break
    # print(phoneme_info)

            
get_transcription_phoneme_information()

def move_phoneme(word, phoneme, index):

    while True:

        if (type(word) != str) and (len(word) < 0):
            word = input("Please put in a string. ")
            continue
        else:
            break

    while True:

        if type(phoneme) != str:
            phoneme = input("Please put in a phoneme. ")
            continue
        elif phoneme not in word:
            phoneme = input("Please put in a phoneme from the word. ")
            continue
        else:
            break

    while True:

        if type(index) != int:
            # print(type(index))
            index = int(input("Please put in a number. "))
            continue
        elif type(index) == int:
            if index > len(word):
                index = int(input("Please put in a number less than the length of the word. "))
            elif index == word.index(phoneme):
                index = int(input("Please put different index. You are moving the same phoneme into the same index. "))
                continue
                
            else:
                break
        
        else:
            break


    ipaTier_model = str((".//" + phon_link + "ipaTier"))

    transcription_indices = str((".//" + phon_link + "sb/*"))


    while True:

        ipaTier = input("Model (target) or actual transcription? ")
        # try:
        if ipaTier == "model":
            print("Model")
            # return ipaTier
            break
            
        elif ipaTier == "actual":
            print("Actual")
            # return ipaTier
            break
            # print("Please select either model (target) or actual.")
            
        else:
            print("Please select either model (target) or actual. ")
            continue

        # except:
            # break
        # else:
            # break
    
    # while True:

    #     index = input("Which index of the transcription? Put a number more than 0. ")

    #     # try:
    #     if int(index) < 0:
    #         # print(type(index))
    #         print("Please put in a number more than 0.")
    #         continue
    #     else:
    #         # return index
    #         break
    #     # except:
    #     #     break

    #     # else:
    #     #     break

    # while True:

    #     scType = input("Onset, nucleus, coda, word boundary, or RA? ")

    #     # try:
    #     if scType == "Onset":
    #         scType = "O"
    #         break
    #     elif scType == "nucleus":
    #         scType = "N"
    #         break
    #     elif scType == "coda":
    #         scType = "C"
    #         break
    #     elif scType == "word boundary":
    #         scType = "WB"
    #         break
    #     elif scType == "RA":
    #         scType = "RA"
    #         break
    #     else:
    #         print("Please select either onset, nucleus, coda, word boundary, or RA.")
    #         continue
        # except:
        #     break

        # else:
        #     break
        
    speaker = str((".//" + phon_link + "u")) 

    # Get ids

    ids = []
    target_ids = []
    actual_ids = []

    for id_test in root.findall(speaker):
            ids.append(id_test.attrib['id'])

    # for id in ids:
    #     # print(id.attrib['id'])
    #     # time.sleep(1)
    #     for form in root.findall(speaker + str("[@id=" + "'" + id + "'" + "]/") + ipaTier_model + "[@form='" + ipaTier + "']/"):
    #         # print(form.attrib['form'])
    #         # print(form)
    #         # time.sleep(1)
    #         if ipaTier == "model":
    #             target_ids.append(id)
    #         elif ipaTier == "actual":
    #             actual_ids.append(id)

    # print(target_ids)

    
    
    # Get transcriptions

    target_id_transcriptions = {}
    actual_id_transcriptions = {}

    transcription_pg = str((".//" + phon_link + "pg/*"))
    orthography_w = str((".//" + phon_link + "g/*"))

    # Iterate over ids
    for id in ids:
        # print(id)
        same_id_transcriptions = []
        # Get transcriptions for each unique id
        for target_id_ in root.findall(speaker + str("[@id=" + "'" + id + "'" + "]/") + ipaTier_model + "[@form='" + ipaTier + "']/" + transcription_pg):
            # print(target_id_)
            # Exclude tag 'sb'
            if target_id_.tag != str(phon_link + 'sb') and target_id_.text is not None:
                print(target_id_.text)
                same_id_transcriptions.append(str(target_id_.text))
                joined = " ".join(same_id_transcriptions)


                if ipaTier == "model":
                    target_id_transcriptions[id] = joined
    # print("Target: ", target_id_transcriptions)
                else:
                    actual_id_transcriptions[id] = joined
    # print("Actual: ", actual_id_transcriptions)

    # # Iterate over ids
    # for id in ids:
    #     # print(id)
    #     same_id_transcriptions = []

    #     # Get child target transcriptions for each unique id
    #     for target_id_ in root.findall(speaker + str("[@id=" + "'" + id + "'" + "]/") + orthography_w):

    #         # for form in root.findall(speaker + str("[@id=" + "'" + id + "'" + "]/") + ipaTier_model + "[@form='" + ipaTier + "']/" + transcription_pg):

    #         # Exclude tag 'sb'
    #         if target_id_.tag != str(phon_link + 'sb') and target_id_.text is not None:
    #             same_id_transcriptions.append(str(target_id_.text))
    #             joined = " ".join(same_id_transcriptions)

    #             if ipaTier == "model":
    #                 target_id_transcriptions[joined] = target_id_.text
    #             else:
    #                 actual_id_transcriptions[joined] = target_id_.text

    # if ipaTier == "model":
    #     print("Target: ", target_id_transcriptions)
    # else:
    #     print("Actual: ", actual_id_transcriptions)

    # All target or actual transcriptions
    
    if ipaTier == "model":
        target_transcriptions = list(target_id_transcriptions.values())
        print("Target transcriptions: ", target_transcriptions)
    else:
        actual_transcriptions = list(actual_id_transcriptions.values())
        print("Actual transcriptions: ", actual_transcriptions)

    words_with_phoneme = []
    phoneme_index_scType = {}

    # while True:

    #     phoneme_search = input("What phoneme would you like to search for? ")
    #     print(phoneme_search)
            

    #     if ipaTier == "model":
    #         # for id in ids:
    #         for (id, transcriptions) in zip(ids, target_transcriptions):
    #             # for transcriptions in target_transcriptions:
    #             if phoneme_search in transcriptions:
    #                 # words_with_phoneme.append(transcriptions)
    #                     # print(words_with_phoneme)
    #                 # for id in ids:
    #                     # print(id)
    #                 indexes_list = []
    #                 scType_list = []
    #                 hiatus_list = []
    #                 hiatus_index = []
    #                 for index in root.findall(speaker + str("[@id=" + "'" + id + "'" + "]/") + ipaTier_model + "[@form='" + ipaTier + "']/" + transcription_indices):                        
                        
    #                     if "hiatus" in index.attrib:
    #                         indexes = index.get('indexes')
    #                         indexes_list.append(indexes)
    #                         scType_ = index.get('scType')
    #                         scType_list.append(scType_)
    #                         hiatus_ = index.get('hiatus')
    #                         hiatus_list.append(hiatus_)

    #                         hiatus_index.append(indexes)
    #                         # for words in words_with_phoneme:
    #                             # print(words)
    #                         phoneme_index_scType[transcriptions] = [indexes_list, scType_list, hiatus_list, hiatus_index]
    #                     else:
    #                         indexes = index.get('indexes')
    #                         indexes_list.append(indexes)
    #                         scType_ = index.get('scType')
    #                         scType_list.append(scType_)
    #                         # for words in words_with_phoneme:
    #                         phoneme_index_scType[transcriptions] = [indexes_list, scType_list,hiatus_list, hiatus_index]
    #                         continue
                            
            
    #     elif ipaTier == "actual":
    #         # for id in ids:
    #         for (id, transcriptions) in zip(ids, actual_transcriptions):
    #             # for transcriptions in target_transcriptions:
    #             if phoneme_search in transcriptions:
    #                 # words_with_phoneme.append(transcriptions)
    #                     # print(words_with_phoneme)
    #                 # for id in ids:
    #                     # print(id)
    #                 indexes_list = []
    #                 scType_list = []
    #                 hiatus_list = []
    #                 hiatus_index = []
    #                 for index in root.findall(speaker + str("[@id=" + "'" + id + "'" + "]/") + ipaTier_model + "[@form='" + ipaTier + "']/" + transcription_indices):                        
                        
    #                     if "hiatus" in index.attrib:
    #                         indexes = index.get('indexes')
    #                         indexes_list.append(indexes)
    #                         scType_ = index.get('scType')
    #                         scType_list.append(scType_)
    #                         hiatus_ = index.get('hiatus')
    #                         hiatus_list.append(hiatus_)

    #                         hiatus_index.append(indexes)
    #                         # for words in words_with_phoneme:
    #                             # print(words)
    #                         phoneme_index_scType[transcriptions] = [indexes_list, scType_list, hiatus_list, hiatus_index]
    #                     else:
    #                         indexes = index.get('indexes')
    #                         indexes_list.append(indexes)
    #                         scType_ = index.get('scType')
    #                         scType_list.append(scType_)
    #                         # for words in words_with_phoneme:
    #                         phoneme_index_scType[transcriptions] = [indexes_list, scType_list,hiatus_list, hiatus_index]
    #                         continue
                
    #     else:
    #         print("Try again.")
    #         continue
    #     break


    # print(phoneme_index_scType)

    # Iterate over ids
    for id in ids:
        same_id_values_target = []
        same_id_values_actual = []

        # Get indices for each target and actual transcription
        for length in root.findall(speaker + str("[@id=" + "'" + id + "'" + "]/") + alignment_segmental + "[@type='segmental']/" + transcription_length):

            # Skip if None appears
            if length.get('value') is not None:

                # Turn value string into list of integers
                values = length.get('value')
                split_string = values.split()
                map_values = map(int, split_string)
                list_values = list(map_values)

                same_id_values_target.append(list_values[0])
                same_id_values_actual.append(list_values[1])

                # Associate id with target and actual transcription indices
                alignment_target_transcriptions[id] = same_id_values_target
                print("test", alignment_target_transcriptions)
                alignment_actual_transcriptions[id] = same_id_values_actual

            else:
                skip

    

    if ipaTier == "model":
            # for id in ids:
            for (id, transcriptions, alignment_id, value) in zip(ids, target_transcriptions, alignment_target_transcriptions, alignment_target_transcriptions.values()):
                if id != alignment_id:
                    continue
                else:
                # for transcriptions in target_transcriptions:
                    if phoneme in transcriptions:
                        # words_with_phoneme.append(transcriptions)
                            # print(words_with_phoneme)
                        # for id in ids:
                            # print(id)
                        indexes_list = []
                        scType_list = []
                        hiatus_list = []
                        hiatus_index = []
                        for index in root.findall(speaker + str("[@id=" + "'" + id + "'" + "]/") + ipaTier_model + "[@form='" + ipaTier + "']/" + transcription_indices):                        
                            
                            if "hiatus" in index.attrib:
                                indexes = index.get('indexes')
                                indexes_list.append(indexes)
                                scType_ = index.get('scType')
                                scType_list.append(scType_)
                                hiatus_ = index.get('hiatus')
                                hiatus_list.append(hiatus_)

                                hiatus_index.append(indexes)
                                # for words in words_with_phoneme:
                                    # print(words)
                                
                                phoneme_index_scType[transcriptions] = [indexes_list, scType_list, hiatus_list, hiatus_index, value]
                            else:
                                indexes = index.get('indexes')
                                indexes_list.append(indexes)
                                scType_ = index.get('scType')
                                scType_list.append(scType_)
                                # for words in words_with_phoneme:
                                phoneme_index_scType[transcriptions] = [indexes_list, scType_list,hiatus_list, hiatus_index, value]
                                continue
                            
            
    elif ipaTier == "actual":
        # for id in ids:
        for (id, transcriptions, alignment_id, value) in zip(ids, actual_transcriptions, alignment_actual_transcriptions, alignment_actual_transcriptions.values()):
            if id != alignment_id:
                continue
            else:
                if phoneme in transcriptions:
                    # words_with_phoneme.append(transcriptions)
                        # print(words_with_phoneme)
                    # for id in ids:
                        # print(id)
                    indexes_list = []
                    scType_list = []
                    hiatus_list = []
                    hiatus_index = []
                    for index in root.findall(speaker + str("[@id=" + "'" + id + "'" + "]/") + ipaTier_model + "[@form='" + ipaTier + "']/" + transcription_indices):                        
                        
                        if "hiatus" in index.attrib:
                            indexes = index.get('indexes')
                            indexes_list.append(indexes)
                            scType_ = index.get('scType')
                            scType_list.append(scType_)
                            hiatus_ = index.get('hiatus')
                            hiatus_list.append(hiatus_)

                            hiatus_index.append(indexes)
                            # for words in words_with_phoneme:
                                # print(words)
                            phoneme_index_scType[transcriptions] = [indexes_list, scType_list, hiatus_list, hiatus_index, value]
                        else:
                            indexes = index.get('indexes')
                            indexes_list.append(indexes)
                            scType_ = index.get('scType')
                            scType_list.append(scType_)
                            # for words in words_with_phoneme:
                            phoneme_index_scType[transcriptions] = [indexes_list, scType_list,hiatus_list, hiatus_index, value]
                            continue
                
    else:
        print("Try again.")

    print("Phoneme_index_scType: ", phoneme_index_scType)

    

    # words_indices = {}

    # print(target_transcriptions)

    fixed_word_indices = {}

    if ipaTier == "model":
        if word in phoneme_index_scType:
            if len(word) > len(phoneme_index_scType[word][0]):
                print("Longer")
            # for (id, transcriptions) in zip(ids, target_transcriptions):
            
                # if phoneme in word:
            # for transcriptions in target_transcriptions:
                    # indexes_list = []
                    # for index in root.findall(speaker + str("[@id=" + "'" + id + "'" + "]/") + ipaTier_model + "[@form='" + ipaTier + "']/" + transcription_indices):
                    #     indexes_list.append(index.get('indexes'))

                    # words_indices[word] = indexes_list
        else:
            print("Word is not in model transcriptions.")

    elif ipaTier == "actual":
        if word in phoneme_index_scType:
            if len(word) > len(phoneme_index_scType[word][0]):
                print("Longer")
                
                for (phoneme, indices) in zip(word, phoneme_index_scType[word][0]):
                    print(phoneme, indices)
                    # print(indices)
                    # if len(indices) > len(word):

                        # print("yes")

                #     print(phoneme)
            # for (id, transcriptions) in zip(ids, actual_transcriptions):
            
            # for transcriptions in target_transcriptions:
                # if phoneme in word:
                    # print("Phoneme in transcriptions")
                # indexes_list = []
                # for index in root.findall(speaker + str("[@id=" + "'" + id + "'" + "]/") + ipaTier_model + "[@form='" + ipaTier + "']/" + transcription_indices):
                #     print(index)
                #     indexes = index.get('indexes')
                #     indexes_list.append(indexes)
                    

                # words_indices[word] = indexes_list
        else:
            print("Word is not in actual transcriptions.")

    

    # print(words_indices)

    # word



move_phoneme("ɛlᵖ", "ɛ", 1)




# search_for_phoneme()
# search_for_word()

# get_transcriptions()

# get_transcription_information()

# excel_folder = str('C:\\Users\\alex\\Documents\\Laptop\\Personal\\Combiths Lab\\Original Excel')

# os.chdir(excel_folder)

# def read_csv_file(file_path):
#     with open(file_path, 'r') as f:
#         print(f.read())

# test_csv_file = "1007_PHON.xlsx"

# xls = pd.read_excel(test_csv_file, sheet_name= None)
# print(xls.keys())

# xls = xlrd.open_workbook(r'')

# for i in range(3:10)

#     data_xlsx = pd.read_excel(test_csv_file, sheet_name=i)

#     data_xlsx.to_csv(, encoding='utf-8', index=False)


# n = 0
# wb = openpyxl.load_workbook(excel_folder + "\\" + test_csv_file)
# sheets = wb.sheetnames
# ws = wb[sheets[n]]

# print(ws)
# print(n)

# with open(test_csv_file, 'r') as csvfile:
#     csvreader = csv.reader(csvfile)

#     files = next(csvreader)

#     for row in csvreader:
#         print(row)

# sheet_names_ = []

# for file in os.listdir():
#     if file.endswith('.xlsx') or file.endswith('.csv'):
#         xls = xlrd.open_workbook(str(file))
#         sheet_names_.append(xls.sheet_names())
#         print(xls.sheet_names())
        # read_csv_file(file)
        # file_path = f"{path}\{file}"

        # read_csv_file(file_path)
# print(sheet_names_)

# def get_sheet_details(file_path):
#     sheets = []
#     file_name = os.path.splitext(os.path.split(file_path)[-1])[0]
#     # Make a temporary directory with the file name
#     directory_to_extract_to = os.path.join(file_name)
#     os.mkdir(directory_to_extract_to)

#     # Extract the xlsx file as it is just a zip file
#     zip_ref = zipfile.ZipFile(file_path, 'r')
#     zip_ref.extractall(directory_to_extract_to)
#     zip_ref.close()

#     # Open the workbook.xml which is very light and only has meta data, get sheets from it
#     path_to_workbook = os.path.join(directory_to_extract_to, 'xl', 'workbook.xml')
#     with open(path_to_workbook, 'r') as f:
#         xml = f.read()
#         dictionary = xmltodict.parse(xml)
#         for sheet in dictionary['workbook']['sheets']['sheet']:
#             sheet_details = {
#                 'id': sheet['sheetId'], # can be @sheetId for some versions
#                 'name': sheet['name'] # can be @name
#             }
#             sheets.append(sheet_details)

    # Delete the extracted files directory
#     shutil.rmtree(directory_to_extract_to)
#     return sheets

# get_sheet_details(excel_folder)



stop = timeit.default_timer()

print('Time: ', stop - start) 