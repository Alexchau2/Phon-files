# from diacritics_list import suffixes, prefixes, extIPA, suprasegmentals, tones, consonants, vowels
from diacritics_list import prefix_diacritics, suffix_diacritics, consonants, vowels, diacritic_switcher, all_diacritics
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
import json
import io
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
orthography_w = str((".//" + phon_link + "g/*"))
transcription_indices = str((".//" + phon_link + "sb/*"))
alignment_segmental = str((".//" + phon_link + "alignment"))
transcription_length = str((".//" + phon_link + "ag/*"))

start = timeit.default_timer()

diacritics = set()
not_diacritics = set()
suffixes_ = set()
prefixes_ = set()
phonemes_ = set()
extIPA_ = set()
suprasegs_ = set()
tones_ = set()
neither_suff_pre = set()

print("Suffixes: ", suffixes_)
print("Prefixes: ", prefixes_)
print("Neither: ", neither_suff_pre)
print("Phonemes: ", phonemes_)    
print("extIPA: ", extIPA_)
print("Supraseg: ", suprasegs_)
print("Tones: ", tones_)

phon_link = "{http://phon.ling.mun.ca/ns/phonbank}"
ipaTier_model = str((".//" + phon_link + "ipaTier"))
transcription = str((".//" + phon_link + "w"))
transcription_pg = str((".//" + phon_link + "pg/*"))
speaker = str((".//" + phon_link + "u"))
orthography_w = str((".//" + phon_link + "g/*"))
transcription_indices = str((".//" + phon_link + "sb/*"))
alignment_segmental = str((".//" + phon_link + "alignment"))
transcription_length = str((".//" + phon_link + "ag/*"))

# Go through all XML files in the directory
for files in xml_files:

    tree = ET.parse(files)
    root = tree.getroot()

    def get_transcription_information():

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

        diacritic_fix = {
            (id, transcriptions): [  # Dictionary with id and transcription as keys
            
                list(
                    map(str, index.get("indexes").split())
                )  # Get indexes for phoneme with diacritics

                if len(index.get("indexes"))
                > 1  # Check if diacritic exists in indexes

                else index.get(
                    "indexes"
                )  # If there is no diacritic, then just get indexes

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
            for (id, transcriptions) in zip(
                ids, id_transcriptions
            )  # Iterate over ids and transcriptions
        }
        return(diacritic_fix)

    get_transcription_information()

    # Example:

    # Ideal output(s): {'ɛlᵖ': [['l'], ['ᵖ']]}, {'ᵇ̵wɛˡ': [['ɛ'], ['ˡ']]}, {'õɹĩ': [['o', 'i'], ['̃', '̃']]}
    # Gives transcription and its phonemes with diacritic(s) after them.

    def transcription_suffix(word):
        
        suffix_list = []

        for (keys, indexes_list) in zip(word, word.values()):

            # print(keys, indexes_list)
            suffixes_phoneme = {}
            suffixes = []
            phoneme_with_suffix = []
            letter_indices = []
            suffix_indices = []

            for indexes in indexes_list:
                
                if len(indexes) > 1:

                    for index in indexes:

                        # Check if index is phoneme.
                        if keys[1][int(index)] in vowels or keys[1][int(index)] in consonants:

                            # Temporarily get index of phoneme
                            letter_index = keys[1].index( keys[1][int(index)] )
                            
                            # If phoneme already in list, skip.
                            if keys[1][int(index)] in phoneme_with_suffix:
                                continue
                            else:

                                # Else, append phoneme into list.

                                # Iterate over indices
                                for i in indexes:

                                    # Check if diacritic
                                    if keys[1][int(i)] in all_diacritics:

                                        # Check if diacritic index is larger than phoneme index
                                        # Basically, checking if diacritic is after phoneme
                                        if int(i) > letter_index:
                                        
                                            # Append diacritic into list
                                            suffix_index = int(i)
                                            suffix_indices.append(suffix_index)
                                            suffixes.append(keys[1][int(i)])
                                            if letter_index in letter_indices:
                                                skip
                                            else:
                                                phoneme_with_suffix.append(keys[1][int(index)])
                                                letter_indices.append(letter_index)
                                        else:
                                            pass
                                    else:
                                        pass

                                    if len(suffixes) == 0:
                                        continue

                                    else:
                                        # Create dictionary entry with transcription as key
                                        # Values are phonemes with suffixes and the diacritics
                                        suffixes_phoneme[keys[1]] = [phoneme_with_suffix, suffixes, letter_indices, suffix_indices]

                                        # Check if dictionary entry is in list
                                        if suffixes_phoneme not in suffix_list:

                                            # Append entry into list
                                            suffix_list.append(suffixes_phoneme)
                                        else:
                                            continue
        if len(suffix_list) == 0:
            skip
        else:
            print("\n Suffix list: ", suffix_list)

    transcription_suffix(get_transcription_information())

stop = timeit.default_timer()

print("Time: ", stop - start)