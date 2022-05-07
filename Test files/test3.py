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

# xml_file = "1007_CCP_CCP Pre.xml"

# Go through all XML files in the directory
diacritics = set()
not_diacritics = set()
suffixes_ = set()
prefixes_ = set()
phonemes_ = set()
extIPA_ = set()
suprasegs_ = set()
tones_ = set()
neither_suff_pre = set()

# for files in xml_files:
#     # print(files)
#     # Parse through files

#     tree = ET.parse(files)
#     root = tree.getroot()

#     def get_transcriptions():

#         # Get ids

#         ids = [id.attrib["id"] for id in root.findall(speaker)]

#         # Get transcriptions for each unique id into a list

#         id_transcriptions = []

#         # Iterate over ids
#         for id in ids:
#             transcriptions = []

#             # Get transcription for each unique id
#             for transcription in root.findall(
#                 speaker
#                 + str("[@id=" + "'" + id + "'" + "]/")
#                 + ipaTier_model
#                 + "[@form='"
#                 + ipaTier
#                 + "']/"
#                 + transcription_pg
#             ):
#                 # Exclude sb tag and if there is no text
#                 if (
#                     transcription.tag != str(phon_link + "sb")
#                     and transcription.text is not None
#                 ):

#                     transcriptions.append(transcription.text)
#             transcriptions = " ".join(transcriptions)
#             id_transcriptions.append(transcriptions)

#         # print(id_transcriptions)
        
        

#         return id_transcriptions
#     for transcription in get_transcriptions():
#         for letter in transcription:
#             if letter in suffixes:
#                 suffixes_.add(letter)
#                 # diacritics.add(letter)
#                 # print(letter, "in diacritic list.")
#             elif letter in prefixes:
#                 prefixes_.add(letter)
#             elif letter in vowels or letter in consonants:
#                 # print(letter)
#                 phonemes_.add(letter)
#             elif letter in suprasegmentals:
#                 suprasegs_.add(letter)
#             elif letter in tones:
#                 tones_.add(letter)
#             elif letter in extIPA:
#                 extIPA_.add(letter)
#             else:
#                 # print(letter)
#                 neither_suff_pre.add(letter)

    
        
#     get_transcriptions()

print("Suffixes: ", suffixes_)
print("Prefixes: ", prefixes_)
print("Neither: ", neither_suff_pre)
print("Phonemes: ", phonemes_)    
print("extIPA: ", extIPA_)
print("Supraseg: ", suprasegs_)
print("Tones: ", tones_)

# vowels = {"ʊ", "o", "ə", "oʊ"}
# alveolars = {"l", "ɹ"}

# test_xml = "C:\\Users\\alex\\Documents\\GitHub\\Combiths Lab\\Phon\\Test files\\test copy.xml"

# for files in xml_files:

#     # tree = ET.parse(test_xml)
#     tree = ET.parse(files)
#     root = tree.getroot()

#     def fix_substitution():
#         # Get ids

#         ids = [id.attrib["id"] for id in root.findall(speaker)]

#         # Get transcriptions for each unique id into a list

#         actual_transcriptions = []
#         model_transcriptions = []

#         # Iterate over ids
#         for id in ids:
#             transcriptions = []

#             # Get actual transcription for each unique id
#             for transcription in root.findall(
#                 speaker
#                 + str("[@id=" + "'" + id + "'" + "]/")
#                 + ipaTier_model
#                 + "[@form='"
#                 + "actual"
#                 + "']/"
#                 + transcription_pg
#             ):
#                 # Exclude sb tag and if there is no text
#                 if (
#                     transcription.tag != str(phon_link + "sb")
#                     and transcription.text is not None
#                 ):

#                     transcriptions.append(transcription.text)
#             transcriptions = " ".join(transcriptions)
#             actual_transcriptions.append(transcriptions)

#             # Iterate over ids
#         for id in ids:
#             transcriptions = []

#             # Get model transcription for each unique id
#             for transcription in root.findall(
#                 speaker
#                 + str("[@id=" + "'" + id + "'" + "]/")
#                 + ipaTier_model
#                 + "[@form='"
#                 + "model"
#                 + "']/"
#                 + transcription_pg
#             ):
#                 # Exclude sb tag and if there is no text
#                 if (
#                     transcription.tag != str(phon_link + "sb")
#                     and transcription.text is not None
#                 ):

#                     transcriptions.append(transcription.text)
#             transcriptions = " ".join(transcriptions)
#             model_transcriptions.append(transcriptions)

#         actual_alignment_values = {
#                 (id, transcriptions): [
#                     list(map(int, alignment.get("value").split()))[
#                     1
#                     ]  # Get actual alignment values
#                     for alignment in root.findall(  # Go to alignment tag in XML file
#                         speaker
#                         + str("[@id=" + "'" + id + "'" + "]/")
#                         + alignment_segmental
#                         + "[@type='segmental']/"
#                         + transcription_length
#                     )
#                 ]
#                 for (id, transcriptions) in zip(
#                     ids, actual_transcriptions
#                 )  # Iterate over ids and transcriptions
#             }

#         model_alignment_values = {
#                 (id, transcriptions): [
#                     list(map(int, alignment.get("value").split()))[
#                     0
#                     ]  # Get actual alignment values
#                     for alignment in root.findall(  # Go to alignment tag in XML file
#                         speaker
#                         + str("[@id=" + "'" + id + "'" + "]/")
#                         + alignment_segmental
#                         + "[@type='segmental']/"
#                         + transcription_length
#                     )
#                 ]
#                 for (id, transcriptions) in zip(
#                     ids, model_transcriptions
#                 )  # Iterate over ids and transcriptions
#             }

#         # print("Actual Alignment: ", actual_alignment_values)
#         # print("Model Alignment: ", model_alignment_values)
#         # print("Actual: ", actual_transcriptions)
#         # print("Model: ", model_transcriptions)
        
        

#         def fix_model_length(model_transcriptions_):
            
#             fixed_transcriptions = []

#             for transcription in model_transcriptions:
#                 if "ˈ" in transcription:
#                     fixed_transcription = transcription.replace("ˈ", "")
#                     fixed_transcriptions.append(fixed_transcription)
#             return(fixed_transcriptions)

#         # fix_model_length(model_transcriptions)

#         for (actual_transcription, model_transcription, actual_alignment, model_alignment) in zip(actual_alignment_values, fix_model_length(model_transcriptions), actual_alignment_values.values(), model_alignment_values.values()):
#             # print(type(actual_transcription[1]))
#             # if len(actual_transcription[1]) == len(model_transcription[1]):
#                 # print(len(actual_transcription[1]), len(model_transcription[1]))
#             for (actual_phoneme, model_phoneme) in zip(actual_transcription[1], model_transcription):
#                 # print(actual_phoneme, model_phoneme)
#                 if (model_phoneme in vowels and actual_phoneme in alveolars):
#                     # print(actual_phoneme)
#                     # print(model_phoneme)
#                     if actual_transcription[1].index(actual_phoneme) == model_transcription.index(model_phoneme):
#                         if actual_phoneme != model_phoneme:
#                             print(files)
#                             print(actual_transcription[1], model_transcription)
#                             print("Actual: ", actual_phoneme)
#                             print("Model: ", model_phoneme)
#                             print(actual_alignment)
#                             print(model_alignment)

#     # for transcriptions in actual_alignment_values:
#     #     print(transcriptions[1])
#     #     for phoneme in transcriptions[1]:
#     #         if phoneme in vowels:
#     #             actual_vowel_index = transcriptions[1].index(phoneme)
#     #             print("Actual Vowel index: ", actual_vowel_index)
#     #         if phoneme in alveolars:
#     #             actual_alveolar_index = transcriptions[1].index(phoneme)
#     #             print("Actual Alveolar index: ", actual_alveolar_index)

#     # for transcriptions in model_alignment_values:
#     #     print(transcriptions[1])
#     #     for phoneme in transcriptions[1]:
#     #         if phoneme in vowels:
#     #             model_vowel_index = transcriptions[1].index(phoneme)
#     #             print("Model Vowel index: ", model_vowel_index)
#     #         if phoneme in alveolars:
#     #             model_alveolar_index = transcriptions[1].index(phoneme)
#     #             print("Model Alveolar index: ", model_alveolar_index)


#     fix_substitution()



# def Diacritic_fixer():

#     media_folder = "C:\\Users\\alex\\Documents\\GitHub\\Combiths Lab\\Phon\\XML Files"

#     os.chdir(media_folder)

#     # Get XML files
#     xml_files = [
#         xml_file
#         for xml_file in listdir(media_folder)
#         if isfile(join(media_folder, xml_file))
#     ]

#     while True:

#         # Ask for model/target or actual transcription information
#         ipaTier = input("Model (target) or actual transcription? ")

#         if ipaTier == "model":
#             print("Model")
#             break

#         elif ipaTier == "actual":
#             print("Actual")
#             break

#         else:
#             print("Please select either model (target) or actual. ")
#             continue

phon_link = "{http://phon.ling.mun.ca/ns/phonbank}"
ipaTier_model = str((".//" + phon_link + "ipaTier"))
transcription = str((".//" + phon_link + "w"))
transcription_pg = str((".//" + phon_link + "pg/*"))
speaker = str((".//" + phon_link + "u"))
orthography_w = str((".//" + phon_link + "g/*"))
transcription_indices = str((".//" + phon_link + "sb/*"))
alignment_segmental = str((".//" + phon_link + "alignment"))
transcription_length = str((".//" + phon_link + "ag/*"))

# start = timeit.default_timer()

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
        # print(diacritic_fix, files)
        # time.sleep(2)
        return(diacritic_fix)

    # get_transcription_information()

    # stop = timeit.default_timer()

    # print("Time: ", stop - start)


# Diacritic_fixer()

# In testing. Do not use. Use transcription_suffix_prefix for now.
# Example:

# Ideal output(s): {'ɛlᵖ': [['l'], ['ᵖ']]}, {'ᵇ̵wɛˡ': [['ɛ'], ['ˡ']]}, {'õɹĩ': [['o', 'i'], ['̃', '̃']]}
# Gives transcription and its phonemes with diacritic(s) after them.

# Current output(s): {'ɛlᵖ': [['l'], ['ᵖ']]}, {'ᵇ̵wɛˡ': [['w', 'ɛ'], ['ˡ']]}, {'õɹĩ': [['o', 'i'], ['̃', '̃']]}
# See second output. "w" should not be in there. It has diacritics before it, but not after.
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
                        # print("index: ", index)
                        # print(keys[1][int(index)])
                        # print(keys[1].index(keys[1][int(index)]))

                        # Check if index is phoneme.
                        if keys[1][int(index)] in vowels or keys[1][int(index)] in consonants:
                            # phoneme_with_suffix.append(keys[1][int(index)])
                            # print("letter index: ", index)

                            # Temporarily get index of phoneme
                            letter_index = keys[1].index( keys[1][int(index)] )
                            
                            # print(phoneme_with_suffix)

                            # If phoneme already in list, skip.
                            if keys[1][int(index)] in phoneme_with_suffix:
                                continue
                            else:

                                # Else, append phoneme into list.
                                # phoneme_with_suffix.append(keys[1][int(index)])
                                # print(phoneme_with_suffix)
                                # Iterate over indices
                                for i in indexes:
                                    # print(keys[1][int(i)])
                                    # Check if diacritic
                                    if keys[1][int(i)] in all_diacritics:

                                        # Check if diacritic index is larger than phoneme index
                                        # Basically, checking if diacritic is after phoneme
                                        if int(i) > letter_index:
                                        
                                        # print("diacritic: ", keys[1][int(i)])

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
                                        # print("Suffixes_phoneme: ", suffixes_phoneme)

                                        # Check if dictionary entry is in list
                                        if suffixes_phoneme not in suffix_list:

                                            # Append entry into list
                                            suffix_list.append(suffixes_phoneme)
                                            # suffix_list.append(letter_index)
                                        else:
                                            continue
        if len(suffix_list) == 0:
            skip
        else:
            print("\n Suffix list: ", suffix_list)
    # def transcription_suffix(word):
        
    #     suffix_list = []

    #     for (keys, indexes_list) in zip(word, word.values()):

    #         # print(keys, indexes_list)
    #         suffixes_phoneme = {}
    #         suffixes = []
    #         phoneme_with_suffix = []
    #         letter_indices = []
    #         suffix_indices = []

    #         for indexes in indexes_list:
                
    #             if len(indexes) > 1:

    #                 for index in indexes:
    #                     # print("index: ", index)
    #                     # print(keys[1][int(index)])
    #                     # print(keys[1].index(keys[1][int(index)]))

    #                     # Check if index is phoneme.
    #                     if keys[1][int(index)] not in suffix_diacritics:
    #                         # phoneme_with_suffix.append(keys[1][int(index)])
    #                         # print("letter index: ", index)

    #                         # Temporarily get index of phoneme
    #                         letter_index = keys[1].index( keys[1][int(index)] )
                            
    #                         # print(phoneme_with_suffix)

    #                         # If phoneme already in list, skip.
    #                         if keys[1][int(index)] in phoneme_with_suffix:
    #                             pass
    #                         else:

    #                             # Else, append phoneme into list.
    #                             phoneme_with_suffix.append(keys[1][int(index)])
    #                             # print(phoneme_with_suffix)
    #                             # Iterate over indices
    #                             for i in indexes:
    #                                 # print(keys[1][int(i)])
    #                                 # Check if diacritic
    #                                 if keys[1][int(i)] in suffix_diacritics:

    #                                     # Check if diacritic index is larger than phoneme index
    #                                     # Basically, checking if diacritic is after phoneme
    #                                     if int(i) > letter_index:
                                        
    #                                     # print("diacritic: ", keys[1][int(i)])

    #                                         # Append diacritic into list
    #                                         suffix_index = int(i)
    #                                         suffix_indices.append(suffix_index)
    #                                         suffixes.append(keys[1][int(i)])
    #                                         letter_indices.append(letter_index)

    #                                         # phoneme_with_suffix.append(keys[1][int(index)])
    #                                     else:
    #                                         try:
    #                                             phoneme_with_suffix.remove(keys[1][int(index)])
    #                                         except:
    #                                             skip
    #                                 # Check if suffixes list is empty
    #                                 if len(suffixes) == 0:
    #                                     pass

    #                                 else:

    #                                     # Create dictionary entry with transcription as key
    #                                     # Values are phonemes with suffixes and the diacritics
    #                                     suffixes_phoneme[keys[1]] = [phoneme_with_suffix, suffixes, letter_indices, suffix_indices]
    #                                     # print("Suffixes_phoneme: ", suffixes_phoneme)

    #                                     # Check if dictionary entry is in list
    #                                     if suffixes_phoneme not in suffix_list:

    #                                         # Append entry into list
    #                                         suffix_list.append(suffixes_phoneme)
    #                                         # suffix_list.append(letter_index)
    #                                     else:
    #                                         pass
    #     print("\n Suffix list: ", suffix_list)
        # f = io.open("readme2.txt", mode='a', encoding='utf-8')
        # with io.open('readme4.txt', mode='a', encoding='utf8', newline='\r\n') as f:
            # f.writelines(json.dumps(suffix_list))

    transcription_suffix(get_transcription_information())


    # Example output: [{'ᵇ̵wʊ': [['w'], ['ᵇ', '̵'], [2], [0, 1]]}]
    # Values:
    # Index 1: Which phonemes have prefixes
    # Index 2: Which diacritics are prefixes
    # Index 3: Indices of phonemes w/ prefix
    # Index 4: Indices of diacritics which are prefixes
    def transcription_prefix(word):
        
        prefix_list = []

        for (keys, indexes_list) in zip(word, word.values()):
            # if diacritic_switcher in keys[1]:
                # print(keys[1].index(diacritic_switcher))
            # print(keys[1].index(diacritic_switcher))
            # print(diacritic_switcher, keys[1])
            prefixes_phoneme = {}
            prefixes = []
            phoneme_with_prefix = []
            letter_indices = []
            prefix_indices = []

            for indexes in indexes_list:
                # print(keys[1])
                # print('2' in indexes)
                if len(indexes) > 1:

                    for index in indexes:

                        # Check if index is phoneme.
                        if keys[1][int(index)] in vowels or keys[1][int(index)] in consonants:

                            # Temporarily get index of phoneme
                            letter_index = keys[1].index( keys[1][int(index)] )
                            
                            # Check if phoneme already in list, then skip.
                            if keys[1][int(index)] in phoneme_with_prefix:
                                continue
                            else:

                                # Iterate over indices
                                for i in indexes:


                                    # Check if diacritic
                                    if keys[1][int(i)] in all_diacritics:

                                        # Check if diacritic index is smaller than phoneme index
                                        # Basically, checking if diacritic is before phoneme
                                        if int(i) < letter_index:
                                        
                                            # Append diacritic into list
                                            prefix_index = int(i)
                                            prefix_indices.append(prefix_index)
                                            prefixes.append(keys[1][int(i)])
                                            if letter_index in letter_indices:
                                                skip
                                            else:
                                                phoneme_with_prefix.append(keys[1][int(index)])
                                                letter_indices.append(letter_index)

                                        # elif keys[1][int(i)] in prefix_diacritics and keys[1][int(i)] == diacritic_switcher:
                                            
                                        else:
                                            pass

                                    else:
                                        pass

                                    # Check if suffixes list is empty
                                    if len(prefixes) == 0:
                                        continue

                                    else:

                                        # Create dictionary entry with transcription as key
                                        # Values are phonemes with suffixes and the diacritics and their respective indices.
                                        # if len(phoneme_with_prefix) > 1:
                                        prefixes_phoneme[keys[1]] = [phoneme_with_prefix, prefixes, letter_indices, prefix_indices]
                                        # else:
                                            # skip
                                        # Check if dictionary entry is in list
                                        if prefixes_phoneme not in prefix_list:

                                            # Append entry into list
                                            prefix_list.append(prefixes_phoneme)
                                        else:
                                            continue
        if len(prefix_list) == 0:
            skip
        else:
            print("\n Prefix list: ", prefix_list, files)

    # transcription_prefix(get_transcription_information())
    # def transcription_prefix(word):
        
    #     prefix_list = []

        

    #     for (keys, indexes_list) in zip(word, word.values()):
    #         # if diacritic_switcher in keys[1]:
    #             # print(keys[1].index(diacritic_switcher))
    #         # print(keys[1].index(diacritic_switcher))
    #         # print(diacritic_switcher, keys[1])
    #         diacritic_switcher_index = []
    #         prefixes_phoneme = {}
    #         prefixes = []
    #         phoneme_with_prefix = []
    #         letter_indices = []
    #         prefix_indices = []

    #         for indexes in indexes_list:
    #             # print(keys[1])
    #             # print('2' in indexes)
    #             if len(indexes) > 1:

    #                 for index in indexes:

    #                     # Check if index is phoneme.
    #                     if keys[1][int(index)] in vowels or keys[1][int(index)] in consonants:

    #                         # Temporarily get index of phoneme
    #                         letter_index = keys[1].index( keys[1][int(index)] )
                            
    #                         # Check if phoneme already in list, then skip.
    #                         if keys[1][int(index)] in phoneme_with_prefix:
    #                             continue
    #                         else:

    #                             # Iterate over indices
    #                             for i in indexes:


    #                                 # Check if diacritic is prefix
    #                                 if keys[1][int(i)] in prefix_diacritics:

    #                                     # Check if diacritic index is smaller than phoneme index
    #                                     # Basically, checking if diacritic is before phoneme
    #                                     if int(i) < letter_index:
                                        
    #                                         # Append diacritic into list
    #                                         prefix_index = keys[1].index(keys[1][int(i)])
    #                                         prefix_indices.append(prefix_index)
    #                                         prefixes.append(keys[1][int(i)])
    #                                         if letter_index in letter_indices:
    #                                             skip
    #                                         else:
    #                                             phoneme_with_prefix.append(keys[1][int(index)])
    #                                             letter_indices.append(letter_index)

    #                                     # elif keys[1][int(i)] in prefix_diacritics and keys[1][int(i)] == diacritic_switcher:
                                            
    #                                     else:
    #                                         pass
                                    
    #                                 elif (keys[1][int(i)] in suffix_diacritics) or (keys[1][int(i)] == diacritic_switcher):
                                        
    #                                     if str(keys[1].find(diacritic_switcher)) in indexes:
    #                                     # Check if diacritic index is smaller than phoneme index
    #                                     # Basically, checking if diacritic is before phoneme
    #                                         if int(i) < letter_index:
                                            
    #                                             # Append diacritic into list
    #                                             prefix_index = keys[1].index(keys[1][int(i)])
    #                                             prefix_indices.append(prefix_index)
    #                                             prefixes.append(keys[1][int(i)])
    #                                             if letter_index in letter_indices:
    #                                                 skip
    #                                             else:
    #                                                 phoneme_with_prefix.append(keys[1][int(index)])
    #                                                 letter_indices.append(letter_index)


    #                                 else:
    #                                     pass

    #                                 # Check if suffixes list is empty
    #                                 if len(prefixes) == 0:
    #                                     continue

    #                                 else:

    #                                     # Create dictionary entry with transcription as key
    #                                     # Values are phonemes with suffixes and the diacritics and their respective indices.
    #                                     # if len(phoneme_with_prefix) > 1:
    #                                     prefixes_phoneme[keys[1]] = [phoneme_with_prefix, prefixes, letter_indices, prefix_indices]
    #                                     # else:
    #                                         # skip
    #                                     # Check if dictionary entry is in list
    #                                     if prefixes_phoneme not in prefix_list:

    #                                         # Append entry into list
    #                                         prefix_list.append(prefixes_phoneme)
    #                                     else:
    #                                         continue
    #     if len(prefix_list) == 0:
    #         skip
    #     else:
    #         print("\n Prefix list: ", prefix_list, files)

    # transcription_prefix(get_transcription_information())

stop = timeit.default_timer()

print("Time: ", stop - start)

# Old

# id_transcriptions = [
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
#             if transcription.tag != str(phon_link + "sb")  # Exclude sb tag and if there is no text
#             and transcription.text is not None
#         ]

# for transcription in id_transcriptions:
#     for letter in transcription:
#         if letter in diacritics_list:
#             diacritics.add(letter)
#             # print(letter, "in diacritic list.")
#         else:
#             not_diacritics.add(letter)
# print(letter, " not in diacritic list.")

# print("diacritics: ", diacritics)
# print("not diacritics: ", not_diacritics)
