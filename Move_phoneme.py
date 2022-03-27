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

# DO NOT USE YET
# Still being worked on

# Able to move phoneme to another index where there is a single phoneme.
# For example, moving "ɡ" in "ɡæ" to where "æ" is. Output: "æɡ"

# Able to move phoneme with diacritic to another index where there is a single phoneme.
# For example, moving "lᵖ" in "ɛlᵖ" to where "ɛ" is. Output: "lᵖɛ"

# Goal: To be able to move individual phonemes and phonemes with diacritics to different place/index in a transcription
# no matter if the index has a single phoneme or a phoneme with a diacritic.

# Problem: Moving phonemes with diacritics to a place/index where there is a phoneme with a diacritic.
# Problem: How to check if index contains a phoneme with a diacritic?
# Problem: Moving single phoneme to a place/index where there is a phoneme with a diacritic.

media_folder = "C:\\Users\\alex\\Documents\\GitHub\\Combiths Lab\\AutoPATT\\XML Files"

os.chdir(media_folder)

# Get XML files
xml_files = [
    xml_file
    for xml_file in listdir(media_folder)
    if isfile(join(media_folder, xml_file))
]

# while True:

#     intention = input("Would you like to move a phoneme or a phoneme with a diacritic? ")

#     if intention == "phoneme":
#         print("Phoneme")
#         break
    
#     elif intention == "phoneme with a diacritic":
#         print("Phoneme with a diacritic")
#         break

#     else:
#         print("Please select 'phoneme' or 'phoneme with a diacritic'. ")
#         continue

# while True:

#     # phoneme_search = input("What phoneme(s) would you like to search for? ")

#     ipaTier = input("Model (target) or actual transcription? ")

#     if ipaTier == "model":
#         print("Model")
#         break

#     elif ipaTier == "actual":
#         print("Actual")
#         break

#     else:
#         print("Please select either model (target) or actual. ")
#         continue

# while True:
#     word = input("Please put in a word. ")
#     if type(word) == str and len(word) > 1:
#         break
#     else:
#         print("Please put in a word longer than 1 letter. ")
#         continue

# while True:

#     phoneme = input("Please put in a phoneme. ")
#     if type(phoneme) != str:
#         continue
#     elif phoneme not in word:
#         print("Please put in a phoneme from the word. ")
#         continue
#     else:
#         break

# while True:

#     index = int(input("Please put in a number. "))
#     if type(index) != int:
#         # print(type(index))
#         continue
#     elif type(index) == int:
#         if index > len(word):
#             print("Please put in a number less than the length of the word. ")
#             continue
#         elif index == word.index(phoneme):
#             print(
#                 "Please put a different index. You are moving the same phoneme into the same index. "
#             )
#             continue
#         elif len(phoneme) > 1 and index in range(len(phoneme)):
#             print("Please use a different index. ")
#             continue
#         else:
#             break

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

# Test case
transcription_info = {
    ('53cc0837-b600-44cc-89fb-c2cbe6435e58', 'ᵇ̵wɛˡ'): [['0 1 2', 'O'], ['3 4', 'N', 'true']]
}
id = '53cc0837-b600-44cc-89fb-c2cbe6435e58'

# def move_phoneme_with_diacritic(desired_word, desired_phoneme, desired_index):
#     print("desired phoneme length ᵇ̵wɛˡ: ", len(desired_phoneme))
#     for transcription in transcription_info: # ('53cc0837-b600-44cc-89fb-c2cbe6435e58', 'ᵇ̵wɛˡ')
#         print(desired_word in transcription)

#         if desired_word in transcription: 
#             print(desired_word)

#             # Check to see if phoneme at desired index has diacritics
#             for info in transcription_info[id, desired_word]: # ['0 1 2', 'O']
#                 print(info[0]) # 0 1 2

#                 if len(info[0]) > 1 and str(desired_index) in info[0]:

#                     # Convert word sequence to list type.
#                     phoneme_spot = list(map(int, info[0].split()))
#                     print("phoneme spot: ", phoneme_spot)

#                     # index_spot = list(map(int, ))

#                     desired_phoneme = list(desired_phoneme)
#                     print("desired phoneme: ", desired_phoneme)

#                     desired_phoneme_list = list(desired_word)
#                     print("desired phoneme list: ", desired_phoneme_list)

#                     # Get the current index of the target phoneme.
#                     # for (phonemes, moved_phonemes) in zip(desired_phoneme[::-1], phoneme_spot):
#                     for phonemes in desired_phoneme[::-1]:

#                         old_index = desired_phoneme_list.index(phonemes)
#                         # old_moved_index = desired_phoneme_list.index(desired_phoneme_list[])
#                         # print("old moved index: ", old_moved_index)
#                         # print(desired_phoneme_list[old_moved_index])

#                         # Remove the target phoneme from the character list.
#                         desired_phoneme = desired_phoneme_list.pop(old_index)
#                         # desired_moved_phonemes = desired_phoneme_list.pop(old_moved_index)
#                         # print("desired moved phonemes: ", desired_phoneme_list)

#                         # Insert target phoneme at a new location.
#                         desired_phoneme_list.insert(desired_index, desired_phoneme)
#                         # desired_phoneme_list.insert(old_index, )
#                         print(desired_phoneme_list)

#                     # Convert word list back to str type and return.
#                     desired_phoneme_list = "".join(desired_phoneme_list)

#                     print(desired_phoneme_list)

#                     return "".join(desired_phoneme_list)
#                 else:
#                     continue

#             else:
#                 print("Put in a phoneme with a diacritic.")

# move_phoneme_with_diacritic("ᵇ̵wɛˡ", "ᵇ̵w", 3)


def move_phoneme_with_diacritic(desired_word, desired_phoneme, desired_index):
    # print(len(desired_phoneme))
    # if desired_word in transcription_info:

    # Able to move phoneme with diacritic(s) to index where there is a single phoneme

    # Check if input is a diacritic by seeing if there is more than 1 phoneme/character
    if len(desired_phoneme) > 1:

        # Check to see if phoneme at desired index is only a phoneme
        if len(desired_word[desired_index]) == 1:

            # Convert word sequence to list type.
            desired_phoneme = list(desired_phoneme)
            desired_phoneme_list = list(desired_word)

            # Get the current index of the target phoneme.
            for phonemes in desired_phoneme[::-1]:

                old_index = desired_phoneme_list.index(phonemes)

                # Remove the target phoneme from the character list.
                desired_phoneme = desired_phoneme_list.pop(old_index)

                # Insert target phoneme at a new location.
                desired_phoneme_list.insert(desired_index, desired_phoneme)

            # Convert word list back to str type and return.
            desired_phoneme_list = "".join(desired_phoneme_list)

            print(desired_phoneme_list)

            return "".join(desired_phoneme_list)

        # # Check to see if phoneme at desired index has diacritics
        # elif len(transcription_info[desired_word]) > 1:

        #     # Convert word sequence to list type.
        #     desired_phoneme = list(desired_phoneme)

        #     desired_phoneme_list = list(desired_word)

        #     # Get the current index of the target phoneme.
        #     for phonemes in desired_phoneme[::-1]:

        #         old_index = desired_phoneme_list.index(phonemes)

        #         # Remove the target phoneme from the character list.
        #         desired_phoneme = desired_phoneme_list.pop(old_index)

        #         # Insert target phoneme at a new location.
        #         desired_phoneme_list.insert(desired_index, desired_phoneme)

        #     # Convert word list back to str type and return.
        #     desired_phoneme_list = "".join(desired_phoneme_list)

        #     print(desired_phoneme_list)

        #     return "".join(desired_phoneme_list)

    else:
        print("Put in a phoneme with a diacritic.")

move_phoneme_with_diacritic ("ᵇ̵wʊ", "ᵇ̵w", 3)
# move_phoneme_with_diacritic("ɛlᵖ", "lᵖ", 0)
# move_phoneme_with_diacritic("ᵇ̵wɛˡ", "ᵇ̵w", 3)

# Able to move individual phonemes to an index where there is an individual phoneme
def move_phoneme(desired_word, desired_phoneme, desired_index):
    # Convert word sequence to list type.
    desired_phoneme_list = list(desired_word)

    # Get the current index of the target phoneme.
    old_index = desired_phoneme_list.index(desired_phoneme)

    # Remove the target phoneme from the character list.
    desired_phoneme = desired_phoneme_list.pop(old_index)

    # Insert target phoneme at a new location.
    desired_phoneme_list.insert(desired_index, desired_phoneme)

    # Convert word list back to str type and return.
    desired_phoneme_list = "".join(desired_phoneme_list)

    print(desired_phoneme_list)
    return "".join(desired_phoneme_list)




# for files in xml_files:

#     tree = ET.parse(files)
#     root = tree.getroot()

#     def phoneme_mover():

#         # Get ids

#         ids = [id.attrib["id"] for id in root.findall(speaker)]

#         # Get transcriptions

#         id_transcriptions = [
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
#             if transcription.tag != str(phon_link + "sb")  # Exclude sb tag
#             and transcription.text is not None
#         ]

#         alignment_values = {
#             (id, transcriptions): [
#                 list(map(int, alignment.get("value").split()))[0]
#                 if alignment.get("value") is not None and ipaTier == "model"
#                 else list(map(int, alignment.get("value").split()))[1]
#                 for alignment in root.findall(
#                     speaker
#                     + str("[@id=" + "'" + id + "'" + "]/")
#                     + alignment_segmental
#                     + "[@type='segmental']/"
#                     + transcription_length
#                 )
#             ]
#             for (id, transcriptions) in zip(ids, id_transcriptions)
#         }

#         if intention == "phoneme":
#             if word in id_transcriptions:
#                 print(word)
#                 move_phoneme(word, phoneme, index)

#         elif intention == "phoneme with a diacritic":
#             if word in id_transcriptions:
#                 print(word)
#                 move_phoneme_with_diacritic(word, phoneme, index)

#     phoneme_mover()
# print(alignment_values)


# def swap_phoneme(desired_word, desired_phoneme, desired_index):
#     desired_word = list(desired_word)
#     desired_word[desired_word.index(desired_phoneme)], desired_word[desired_index] = (
#         desired_word[desired_index],
#         desired_word[desired_word.index(desired_phoneme)],
#     )
#     desired_word = "".join(desired_word)
#     print(desired_word)

# move_phoneme(word, phoneme, index)

# swap_phoneme(word, phoneme, index)

# move_phoneme()

stop = timeit.default_timer()

print("Time: ", stop - start)
