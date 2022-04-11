from cgi import test
from cmd import PROMPT
import string
from sys import prefix
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
from numpy import empty
import openpyxl
import xlrd
import re
import unicodedata
from diacritics_list import diacritics_list
# from Diacritic_fixer import Diacritic_fixer

diacritic_fixed = {
    ("8c437a92-64f3-4438-8098-62273be265a7", "ɛlᵖ"): ["0", ["1", "2"]],
    ("6a230285-bd20-4814-bbf5-8c4318fadbcd", "ɡæ"): ["0", "1"],
    ("256e7432-9ab7-47b4-979b-d6ae631f612a", "ɡɑ"): ["0", "1"],
    ("3ba5c886-9580-48df-b94a-4c16c7e330f4", "bɛʊᵗ"): ["0", "1", ["2", "3"]],
    ("f4fd5527-7e06-40a9-ae09-e86fdeac9509", "kɔˀ"): ["0", ["1", "2"]],
    ("25dfd4a7-fa25-4252-a7b7-bf5b16b5acfc", "mɛʊᵗ"): ["0", "1", ["2", "3"]],
    ("c19b5539-109a-4fab-84e1-9b26121f39b2", "oʊ"): ["0", "1"],
    ("8440652d-0d02-47d8-a607-76ad23f1b702", "ɡoʊ"): ["0", "1", "2"],
    ("59ab01d8-81eb-4077-985e-36b02437ef92", "ɡoʊ"): ["0", "1", "2"],
    ("587ff288-ff94-474d-b548-e2489d18ac38", "mɪᶷ"): ["0", ["1", "2"]],
    ("6452471b-7e75-4014-813a-728e115fd322", "ɡɑʔ"): ["0", "1", "2"],
    ("75bb71be-5d4e-4771-82b0-6ba1803d1b91", "ɡɪᶷ"): ["0", ["1", "2"]],
    ("4e683f1b-8841-4603-9bd6-f763e36a2ad2", "ᵇ̵wʊ"): [["0", "1", "2"], "3"],
    ("1f1cb582-53f8-4ca0-8327-5eb1fecf0bd7", "ɡɔ"): ["0", "1"],
    ("eb2251b8-4729-440d-9c46-3e0bc3375c1f", "ɡɛʊ"): ["0", "1", "2"],
    ("73e9306b-9c8d-48e8-9eb3-2a590bd968af", "ɛʊ"): ["0", "1"],
    ("53cc0837-b600-44cc-89fb-c2cbe6435e58", "ᵇ̵wɛˡ"): [["0", "1", "2"], ["3", "4"]],
    ("8e782cd7-7a0a-4458-8b2a-f5e4c6ff3ad2", "fɪʊ"): ["0", "1", "2"],
    ("0cba1702-22fe-4fff-89f3-e4ee17b0ac43", "bʊɹͥ"): ["0", "1", ["2", "3"]],
    ("2fa94cc1-10f6-4761-b97c-78a4c0ddbb2e", "kɑɹˀ"): ["0", "1", ["2", "3"]],
    ("e2b0e238-42f9-4ed1-a75a-eaf17458410b", "ɡʊɹᵗ"): ["0", "1", ["2", "3"]],
    ("6bb9c5d8-5845-478c-b157-e5654a1d4238", "ɡʊɹᶦ"): ["0", "1", ["2", "3"]],
    ("35f0e91a-d996-4fd9-b3e8-928d937e880d", "ᵇ̵wʊɹ"): [["0", "1", "2"], "3", "4"],
    ("7b456ab2-7aae-4d0c-956d-3a10dc72b9a8", "bɑɹ"): ["0", "1", "2"],
    ("205f3ac9-40fe-4a9e-bbbe-5d801c31bf5e", "ɡoɹͥt˺"): [
        "0",
        "1",
        ["2", "3"],
        ["4", "5"],
    ],
    ("36c8b454-69c2-42e9-b787-d51a00058f47", "ɑɹ"): ["0", "1"],
    ("34d97cc3-25fb-4df3-9d9b-4b009947f792", "ɡɑɹ"): ["0", "1", "2"],
    ("cc59b9aa-9078-4d83-b17f-e382c001f6b9", "bʊɹi"): ["0", "1", "2", "3"],
    ("63dfee49-6397-41fc-9144-688cd62dfb1d", "kɑɹᵈ"): ["0", "1", ["2", "3"]],
    ("6a9f2d63-5734-455a-9e4b-c021f2c25f43", "ɑɹ"): ["0", "1"],
    ("0e5dd950-05a9-4393-8f86-390d062b7fc7", "fʊɹˀi"): ["0", "1", ["2", "3"], "4"],
    ("630ca8cf-9b3d-4545-8f21-b48b07ec6c53", "bɑɹᵗ"): ["0", "1", ["2", "3"]],
    ("bba38d56-5b0a-4018-a812-0acc3c7c59db", "bɑɹˀ"): ["0", "1", ["2", "3"]],
    ("f287dc32-a3be-4a69-b2ff-f21262204af0", "aɪbʊɹ"): ["0", "1", "2", "3", "4"],
    ("da596ceb-86f7-4ee6-8b7f-3c1b61188383", "bʊɹ"): ["0", "1", "2"],
    ("92e14294-5705-4e02-b637-e2f4dbc81c00", "eɪbʊɹ"): ["0", "1", "2", "3", "4"],
    ("e736235f-240d-42f0-8121-244345cb2c09", "ɡʊɹ ɡɑɹͮ"): [
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        ["6", "7"],
    ],
    ("ae93e956-453b-46af-8e28-f068688ed38e", "ɡʊɹᶦ"): ["0", "1", ["2", "3"]],
    ("84a545d9-c89e-4784-b086-4d7b9ef3d465", "nɔɪ"): ["0", "1", "2"],
    ("85e3cb02-1570-4e72-816e-2337beebe70c", "ɡʊɹ"): ["0", "1", "2"],
    ("73bd5955-e20b-4e77-92e3-e7ca200ea4d8", "ɡɑɹ"): ["0", "1", "2"],
    ("97eb58f0-69cb-4b9e-bfe6-a5d072a0a570", "ɡɑɹ"): ["0", "1", "2"],
    ("3ab801cb-a65d-4b17-a3cf-c161708a808c", "ˀ̵ɑɹ"): [["0", "1", "2"], "3"],
    ("8e6f7f64-642d-4f04-918d-1aa4b86eadb0", "ʊɹ"): ["0", "1"],
    ("d0cb2dbe-8577-4e6b-88c7-01b430d8c892", "bʊɹᵗ"): ["0", "1", ["2", "3"]],
    ("9008c922-0c3f-497e-8ac6-d49224e21e51", "ɑɹi"): ["0", "1", "2"],
    ("d5bfbfda-072b-4b64-97d6-bd16c0b9e2d0", "pʊɹͥ"): ["0", "1", ["2", "3"]],
    ("c69c862c-3f56-442f-a7e1-6b5dbb8921db", "nɔɪ̃ˀ"): ["0", "1", ["2", "3", "4"]],
    ("5e293b23-9bcb-4a39-ac2a-7fbd5091862d", "ɑɹ"): ["0", "1"],
    ("292e5316-b00d-4215-a4c8-d84b42eccc70", "mɑɹ"): ["0", "1", "2"],
    ("96982489-7d6b-4eb9-aaa7-15a724c6cd0e", "kɑɹ"): ["0", "1", "2"],
    ("c372c37e-ed63-4880-928d-c25bee690588", "ɡʊɹᶦ"): ["0", "1", ["2", "3"]],
    ("a0ad7f9f-e192-4195-a0cd-2d99225d042a", "ɡoɹᶦ"): ["0", "1", ["2", "3"]],
    ("9e46ffac-b478-4a9e-9788-8942c0083686", "bʊɹᵗ"): ["0", "1", ["2", "3"]],
    ("80e7ecac-98f5-4ba4-806d-1dbccb6c0536", "jɑɹ"): ["0", "1", "2"],
    ("bd071d98-9990-4ad4-bbf1-6b82ba3851b4", "ɡʊɹi"): ["0", "1", "2", "3"],
    ("14f6ae4a-73fc-49da-83d5-2974bfa1c1d7", "ɡɑɹ"): ["0", "1", "2"],
    ("ce0202bc-2c0c-4940-b2f2-14e06a7280a7", "ɑ̃ɹ"): [["0", "1"], "2"],
    ("ec738f82-691f-495e-906f-dd31a690714f", "wʊ̃ɹĩ"): [
        "0",
        ["1", "2"],
        "3",
        ["4", "5"],
    ],
    ("da0e7d3c-934e-4da0-aa29-c623ee4baf54", "bʷɑ̃ɹ"): [["0", "1"], ["2", "3"], "4"],
    ("6224609d-3954-4f1a-95b3-8ba2bc9fdebd", "bɑ̃ɹ"): ["0", ["1", "2"], "3"],
    ("60cde12c-4fe3-41a8-8826-5d317ade00a9", "fɹaɪ̃"): ["0", "1", "2", ["3", "4"]],
    ("d49295f8-7676-4af7-b6af-416cdcca9bb1", "õɹĩ"): [["0", "1"], "2", ["3", "4"]],
    ("0a16913a-23a7-49af-960f-7301e4c9a13d", "ɡɑɹ"): ["0", "1", "2"],
    ("9ce8bb92-7a2b-47d1-ad12-32e16cd9636a", "ɡʊɹ"): ["0", "1", "2"],
    ("d4bbee5a-70bd-4e62-9bb0-f6ba6189547f", "fwʊɹ"): ["0", "1", "2", "3"],
    ("d472e080-1f53-43bf-b0cd-1504b2339aa7", "wɑ"): ["0", "1"],
    ("b392514e-6eb8-4969-a9c8-3c56ce789432", "ɡæ"): ["0", "1"],
    ("88cfdd25-3586-414b-9e15-e15a55c722a4", "vɹɑ"): ["0", "1", "2"],
    ("944cd667-7ccc-4a2e-a1ca-7cc0d190811c", "nɛ̃"): ["0", ["1", "2"]],
    ("d02c9227-f41a-41f5-9a93-e58d458c3d2a", "ɡoʊ"): ["0", "1", "2"],
    ("a65463f3-b7f3-4482-8df4-a35e154e43ee", "vɛˀ"): ["0", ["1", "2"]],
    ("d3f36cd2-86c9-4297-8764-7140c72a1037", "mæˀ"): ["0", ["1", "2"]],
    ("da26c533-5ebf-4dee-a239-c5da597c7c6f", "ɡɛ"): ["0", "1"],
    ("33903fa0-1d8a-4924-a6da-f535d386ddba", "æ"): ["0"],
    ("77d76f79-6c6a-409f-a496-b035138ef602", "ɡɛ̃ˀ"): ["0", ["1", "2", "3"]],
    ("aea128f7-3850-4d60-806d-b262ab5872e5", "beɪ̃ᵗ"): ["0", "1", ["2", "3", "4"]],
    ("fd3135b6-0e11-41d3-b9ee-04e802e06aa3", "bɔɪ̃"): ["0", "1", ["2", "3"]],
    ("557b0fd0-04bc-428c-a3f8-f80cf34f19a6", "blɔ"): ["0", "1", "2"],
    ("d03f4244-66f0-4526-9ba3-c7c5d546ee53", "æ̃"): [["0", "1"]],
    ("ad1ee017-9415-427a-b2d9-9460c6c06453", "ɡæ"): ["0", "1"],
    ("22fb9d70-cab3-4b04-81b8-fa955c410206", "naɪ̃"): ["0", "1", ["2", "3"]],
    ("b36e7cac-f31a-469d-8038-7a2a0adde7d3", "ɡɛ̃"): ["0", ["1", "2"]],
    ("0127a163-69ca-452c-828c-8e99595689ae", "mʌ̃"): ["0", ["1", "2"]],
    ("1b3cd75c-4593-499f-bfbe-694ad664faee", "fɹɛ̃"): ["0", "1", ["2", "3"]],
    ("45aac007-d45f-4288-9674-30e9924d787f", "baʊ̃"): ["0", "1", ["2", "3"]],
    ("a4ab7f35-3cac-4e10-8a8d-679792c06224", "ɡæ̃"): ["0", ["1", "2"]],
    ("2f121968-3688-4d52-a768-a75fa9d836ba", "jʌ̃"): ["0", ["1", "2"]],
    ("17fcc64c-4e78-4e26-bbab-40b696b087c0", "bæ̃"): ["0", ["1", "2"]],
    ("2b4f5a03-f38c-41b4-b751-b576021715a0", "bʌ̃"): ["0", ["1", "2"]],
    ("e826ac2f-3f69-4a40-a4b0-b04cc3163ee2", "ɑɹĩ"): ["0", "1", ["2", "3"]],
    ("df8ea6ba-b15c-475f-99ec-6d5c88c41913", "bʌ̃"): ["0", ["1", "2"]],
    ("380f8197-94cd-4929-800e-3cc6d9ae6848", "deɪ̃"): ["0", "1", ["2", "3"]],
    ("1d5a99aa-53ca-4963-8b1b-2d70d34b9a0a", "b̥ĩ"): [["0", "1"], ["2", "3"]],
    ("1fd58152-fbc8-49bd-a31f-92ab8445e5ce", "ɡĩˀ"): ["0", ["1", "2", "3"]],
    ("c4ccdbb4-0e1b-4e97-b557-c9060dc2b763", "wʌ̃"): ["0", ["1", "2"]],
    ("9bf0c440-19f1-4928-8bd6-f81323e59966", "ɡæ̃"): ["0", ["1", "2"]],
    ("e941a365-efe3-447d-a3a1-9c92cf09ce39", "ɡʌ̃ˀ"): ["0", ["1", "2", "3"]],
    ("102893f7-f9a6-4ce4-a72f-3f8e21fc0c6d", "ɡɛ̃ˀ"): ["0", ["1", "2", "3"]],
    ("ef4deacd-3ebf-431d-bd0e-6750aab31ba4", "jɪ"): ["0", "1"],
    ("f10dca5e-bbd9-4bad-b546-a2575f9fa30f", "ɡ̥ɔ"): [["0", "1"], "2"],
    ("e73b9183-62e4-42b2-a580-5100f11b95f4", "bɹæ"): ["0", "1", "2"],
    ("c73f4dd1-251a-436b-8c3d-ace5bd398464", "bɔ"): ["0", "1"],
    ("506a60f4-b6a3-4490-adb8-9f9290d818d3", "ɡɪ"): ["0", "1"],
    ("da363ad8-9b43-4703-8e4f-ec67165d8085", "fɪ"): ["0", "1"],
}
# ('53cc0837-b600-44cc-89fb-c2cbe6435e58', 'ᵇwᵇɛ'): [['0', '1', '2'], ['3']]

# phonemes =


test_word = "ᵇwᵇ̵ɛ"

test_word_2 = "ᵇ̵w"

# for phoneme in test_word_2:
# print(phoneme)

def transcription_prefix(word):
    
    prefix_list = []

    for (keys, indexes_list) in zip(word, word.values()):

        print(keys, indexes_list)
        phoneme_combination = {}
        list_of_phonemes = []
        prefixes = []
        suffixes = []
        phoneme_with_prefix = []
        index_holder = []
        keys_index = []
        for indexes in indexes_list:
            
            # Check if indexes has diacritic
            if len(indexes) > 1:

                # for index, phoneme in enumerate(keys[1][:]):
                #     print(index, phoneme)
                index_holder.append(indexes)

                for lists in index_holder:
                    for index in lists:

                        keys_index.append(keys[1][int(index)])

                        index_holder = []

                    phoneme_with_prefix.append(keys_index) 

                    keys_index = []

                print("Test: ", phoneme_with_prefix)

                for phoneme_lists in phoneme_with_prefix:
                    
                    for phoneme_diacritic in phoneme_lists:

                        if phoneme_diacritic not in diacritics_list:

                            if phoneme_diacritic in list_of_phonemes:
                                pass
                            else:
                                list_of_phonemes.append(phoneme_diacritic)
                                print("Not diacritics: ", list_of_phonemes)
                # for i in range(len(phoneme_lists)):

                #     if keys[1].index(phoneme_diacritic) > keys[1].index(not_diacritic):

                #         # if 
                #         suffixes.append(phoneme_diacritic)
                #         print("suffixes: ", suffixes)
                #     elif keys[1].index(phoneme_diacritic) < keys[1].index(not_diacritic):
                #         prefixes.append(phoneme_diacritic)
                #         print("prefixes: ", prefixes)
                    # print("index: ", index)
                    # print(keys[1][int(index)])
                    # print(keys[1].index(keys[1][int(index)]))
                    # if keys[1][int(index)] not in diacritics_list:
                    #     # phoneme_with_suffix.append(keys[1][int(index)])
                    #     # print("letter index: ", index)
                    #     letter_index = keys[1].index( keys[1][int(index)] )
                    #     if keys[1][int(index)] in phoneme_with_prefix:
                    #         pass
                    #     else:
                    #         phoneme_with_prefix.append(keys[1][int(index)])
                    #         for i in indexes:
                    #             if keys[1][int(i)] in diacritics_list and int(i) < letter_index:
                        
                    #             # print("diacritic: ", keys[1][int(i)])
                    #                 if keys[1][int(i)] in prefixes:
                    #                     pass
                    #                 else:
                    #                     prefixes.append(keys[1][int(i)])
                    #     # print(prefixes)
                    #     # print(phoneme_with_prefix)
                    #         if len(prefixes) == 0:
                    #             pass
                    #         else:
                    #             prefixes_phoneme[keys[1]] = [phoneme_with_prefix, prefixes]
                    #             print(prefixes_phoneme)
                    #             if prefixes_phoneme not in prefix_list:
                    #                 prefix_list.append(prefixes_phoneme)
                    #             else:
                    #                 pass
    print(prefix_list)

# def transcription_prefix(word):
    
#     prefix_list = []

#     for (keys, indexes_list) in zip(word, word.values()):

#         print(keys, indexes_list)
#         prefixes_phoneme = {}
#         prefixes = []
#         phoneme_with_prefix = []

#         for indexes in indexes_list:
            
#             if len(indexes) > 1:

#                 for index in indexes:
#                     # print("index: ", index)
#                     # print(keys[1][int(index)])
#                     # print(keys[1].index(keys[1][int(index)]))
#                     if keys[1][int(index)] not in diacritics_list:
#                         # phoneme_with_suffix.append(keys[1][int(index)])
#                         # print("letter index: ", index)
#                         letter_index = keys[1].index( keys[1][int(index)] )
#                         if keys[1][int(index)] in phoneme_with_prefix:
#                             pass
#                         else:
#                             phoneme_with_prefix.append(keys[1][int(index)])
#                             for i in indexes:
#                                 if keys[1][int(i)] in diacritics_list and int(i) < letter_index:
                        
#                                 # print("diacritic: ", keys[1][int(i)])
#                                     if keys[1][int(i)] in prefixes:
#                                         pass
#                                     else:
#                                         prefixes.append(keys[1][int(i)])
#                         # print(prefixes)
#                         # print(phoneme_with_prefix)
#                             if len(prefixes) == 0:
#                                 pass
#                             else:
#                                 prefixes_phoneme[keys[1]] = [phoneme_with_prefix, prefixes]
#                                 print(prefixes_phoneme)
#                                 if prefixes_phoneme not in prefix_list:
#                                     prefix_list.append(prefixes_phoneme)
#                                 else:
#                                     pass
#     print(prefix_list)
# def transcription_prefix(word):

#     # print(word)
#     # all_prefixes = []
    
#     for (keys, indexes_list) in zip(word, word.values()):
#         prefixes = []
#         # suffixes = []
#         print(keys, indexes_list)

#         # if keys[1] == word:
#         # for phoneme in keys[1]:
#         for indexes in indexes_list:
#             if len(indexes) > 1:
#                 for index in indexes:
#                     if keys[1][int(index)] not in diacritics_list:
#                         try:
#                             for i in indexes[::int(index)-1]:
#                                 if keys[1][int(i)] in diacritics_list and int(i) < int(index):
#                                     print("diacritic: ", keys[1][int(index)], i, keys[1][int(i)]) 
#                                     prefixes.append(keys[1][int(i)])
#                                     print("prefixes: ", prefixes)
#                                 # elif keys[1][int(i)] in diacritics_list and int(i) > int(index):
#                                 #     suffixes.append(keys[1][int(i)])
#                                 #     print("suffixes :", suffixes)
#                         except:
#                             skip
                    # print(index)
                    # if keys[1][int(index)] in diacritics_list:
                    #     print("diacritic", keys[1][int(index)], index)
                    # else:
                    #     print("phoneme", keys[1][int(index)], index)

        # for index, phoneme in enumerate(keys[1][:-1]):
        #     print(index, phoneme)
        #         # for (phoneme, phoneme_backward, index) in zip(keys[1], keys[1:], indexes):
        #             # print(phoneme, phoneme_backward, index)
                    
        #             # for iterate in range(len(word) - 1):
        #                 # print("iterate: ", keys[1][iterate + 1])
        #     # print("test: ", keys[1][:keys[1].index(phoneme)])
        #     if (
        #         phoneme not in diacritics_list
        #         and keys[1][index + 1] in diacritics_list
        #         # keys[1][:keys[1].index(phoneme)] in diacritics_list
        #         # phoneme in diacritics_list
        #         # and keys[1][index + 1] not in diacritics_list
        #         # and keys[1][index] in diacritics_list
        #     ):
        #         skip
        #     elif phoneme not in diacritics_list:

        #         print("phoneme: ", phoneme)
        #         for i in keys[1][:keys[1].index(phoneme)]:

        #             # print(i)
        #             if i in diacritics_list:
        #                 print("in diacritics list: ", i)
                # prefixes.append(keys[1].split(phoneme))
                # print(prefixes)
                # for i in prefixes:
                #     for j in i:
                #         if len(j) == 1:
                #             for k in j:
                #                 # print(diacritic, k)
                #                 if k in diacritics_list:
                #                     print("diacritic in list: ", k)
                #         elif len(j) > 1:
                #             for k in j:
                #                 for l in k:
                #                     if l in diacritics_list:
                #                         print("diacritics in list: ", l)
                            
                # prefixes.append([keys[1], phoneme, index])
                # prefixes[(keys[1], phoneme)] = index
        
        # all_prefixes.append(prefixes)
                
    # print(all_prefixes)
            # elif len(indexes) == 3:
            #     for (phoneme, index) in zip(keys[1], indexes):
            #         print(phoneme, index)
            #         if phoneme in diacritics_list:
            #             prefixes.append(index)
            #         else:
            #             break

    # print(prefixes)

def transcription_suffix(word):
    
    suffix_list = []

    for (keys, indexes_list) in zip(word, word.values()):

        # print(keys, indexes_list)
        suffixes_phoneme = {}
        suffixes = []
        phoneme_with_suffix = []

        for indexes in indexes_list:
            
            if len(indexes) > 1:

                for index in indexes:
                    # print("index: ", index)
                    # print(keys[1][int(index)])
                    # print(keys[1].index(keys[1][int(index)]))
                    if keys[1][int(index)] not in diacritics_list:
                        # phoneme_with_suffix.append(keys[1][int(index)])
                        # print("letter index: ", index)
                        letter_index = keys[1].index( keys[1][int(index)] )
                        
                        # print(phoneme_with_suffix)
                        if keys[1][int(index)] in phoneme_with_suffix:
                            pass
                        else:
                            phoneme_with_suffix.append(keys[1][int(index)])
                            for i in indexes:
                                
                                if keys[1][int(i)] in diacritics_list:

                                    if int(i) > letter_index:
                                    
                                    # print("diacritic: ", keys[1][int(i)])
                                        suffixes.append(keys[1][int(i)])
                                        # phoneme_with_suffix.append(keys[1][int(index)])
                                if len(suffixes) == 0:
                                    pass
                                else:
                                    suffixes_phoneme[keys[1]] = [phoneme_with_suffix, suffixes]
                                    print(suffixes_phoneme)
                                    if suffixes_phoneme not in suffix_list:
                                        suffix_list.append(suffixes_phoneme)
                                    else:
                                        pass
    print(suffix_list)
                        # print(suffixes)
                        # print(phoneme_with_suffix)
                        # suffixes_phoneme[keys[1]] = [phoneme_with_suffix, suffixes]
                        # [print(suffixes_phoneme)]
                    # elif keys[1][int(index)] in diacritics_list and index > keys[1].index():
                        # print("diacritic index: ", index)
                        # suffixes.append(keys[1][int(index)])
                # print(phoneme_with_suffix)
                # print(suffixes)
                # suffixes_phoneme[] = suffixes
                # print(suffixes_phoneme)
                        # print("not diacritic: ", keys[1][int(index)])
                        # # print("letter index: ", keys[1].index( keys[1][int(index)] ))
                        # letter_index = keys[1].index( keys[1][int(index)] )
                        # print("letter index: ", letter_index)
                        # print(indexes.index(str(letter_index)))
                            # print(i)
                        # for i in indexes:
                        # for i in keys[1][keys[1].index( keys[1][int(index)] ):]:
                            # if int(i) in diacritics_list:
                        # for i in indexes.index(str(keys[1].index( keys[1][int(index)] ))):
                                # print("diacritics: ", i)
                        # for i in indexes [ keys[1].index( keys[1][int(index)] ) ]
                        # for i in indexes[ keys[1].index(keys[1][int(index)]) :] :
                            # print("i: ", i)
                        # suffixes = []

                        # for i in indexes[ keys[1].index( keys[1][int(index)] ) :]:
                            # print(keys[1][int(i)])
                        # for i in indexes[keys[1].index(keys[1][int(index)])]:
                        # print("not diacritic: ", keys[1][int(index)])
                        # print("index: ", keys[1].index( keys[1][int(index)] ))
                        # print("test: ", indexes[ keys[1].index( keys[1][int(index)] ) : ] )
                            
                        #     if keys[1][int(i)] in diacritics_list:
                                
                        #         suffixes.append(keys[1][int(i)])

                        #     print(suffixes)
                        #     suffixes_phoneme[keys[1][int(index)]] = suffixes
                            
                        # print(suffixes_phoneme)

# def transcription_suffix(word):
    
#     for (keys, indexes_list) in zip(word, word.values()):

#         print(keys, indexes_list)
#         suffixes_phoneme = {}

#         for indexes in indexes_list:

#             if len(indexes) > 1:

#                 for index in indexes:

#                     if keys[1][int(index)] not in diacritics_list:
#                         suffixes = []

#                         for i in indexes:
                            
#                             if keys[1][int(i)] in diacritics_list:
                                
#                                 suffixes.append(keys[1][int(i)])

#                             print(suffixes)
#                             suffixes_phoneme[keys[1][int(index)]] = suffixes
                            
#                         print(suffixes_phoneme)
                                # print(keys[1][int(i)])
                        # for i in keys[1][int(index):]:
                            
                        #     if i in diacritics_list: 
                        #         print(i)
                        #         suffixes.append(i)
                        #         # print(suffixes)
                        #         suffixes_phoneme[keys[1][int(index)]] = suffixes
                        # print(suffixes_phoneme)
                        # print(keys[1][int(index)+1:])
                        # print("i: ", i)
                            # print(index[int(index)])
                            # if keys[1][int(i)] in diacritics_list and int(i) > int(index):
                                # print("diacritic: ", keys[1][int(index)], i, keys[1][int(i)]) 
                                # suffixes.append(keys[1][int(i)])
                                # print("suffixes: ", suffixes)
                                # elif keys[1][int(i)] in diacritics_list and int(i) > int(index):
                                #     suffixes.append(keys[1][int(i)])
                                #     print("suffixes :", suffixes)
                        # except:
                            # skip

transcription_prefix(diacritic_fixed)
# transcription_suffix(diacritic_fixed)
# transcription_prefix(test_word)
# transcription_prefix(test_word_2)
# transcription_prefix(Diacritic_fixer())

# for word in diacritic_fixed:
#     print(word)
#     print(test_word in word)
#     for list_index in diacritic_fixed.values():
#         for indexes in list_index:

#             for index in indexes:
#                 if len(indexes) == 3:


def shift_phoneme(word, phoneme, spaces):

    print(abs(spaces))

    if (
        abs(spaces) > len(word)
        or abs(spaces) == len(word)
        or (word.index(phoneme) + spaces > len(word) - 1)
        or spaces == 0
        or test_word in diacritic_fixed
    ):
        #     or (
        #         word[word.index(phoneme) + spaces] not in diacritics_list
        #         and word[(word.index(phoneme) + spaces) - 1] in diacritics_list
        #     )
        #     or (
        #         word[word.index(phoneme) + spaces] not in diacritics_list
        #         and word[(word.index(phoneme) + spaces) - 1] in diacritics_list
        #         and word[(word.index(phoneme) + spaces) + 1] in diacritics_list
        #     )
        #     or (
        #         word[word.index(phoneme) + spaces] in diacritics_list
        #         and word[(word.index(phoneme) + spaces) - 1] in diacritics_list
        #     )
        #     or (
        #         spaces == -1 and word[word.index(phoneme) + spaces] in diacritics_list
        #     )
        #     or (
        #         word[word.index(phoneme) + spaces] in diacritics_list
        #         and word[(word.index(phoneme) + spaces) - 1] not in diacritics_list
        #         and word[(word.index(phoneme) + spaces) + 1] in diacritics_list
        #     )
        # ):

        print("Please put in a different number in spaces.")
        return word

    else:

        # Single phoneme and not a diacritic
        if len(phoneme) == 1 and phoneme not in diacritics_list:

            # Convert word sequence to list type.
            phoneme_list = list(word)

            # Get the current index of the target phoneme.
            old_index = phoneme_list.index(phoneme)

            # Remove the target phoneme from the character list.
            phoneme = phoneme_list.pop(old_index)

            # Insert target phoneme at a new location.
            print(word[old_index + spaces])

            if (
                word[old_index + spaces] not in diacritics_list
                and word[old_index + spaces + 1] in diacritics_list
            ):  # 'ᵇ̵wɛ
                phoneme_list.insert(
                    old_index + spaces, phoneme
                )  # Shift phoneme back certain spaces
                print(old_index + spaces, phoneme_list)

            else:
                phoneme_list.insert(
                    old_index + spaces, phoneme
                )  # Shift phoneme back certain spaces
                print(old_index + spaces, phoneme_list)

            # Convert word list back to str type and return.
            phoneme_list = "".join(phoneme_list)

            print(phoneme_list)

            return "".join(phoneme_list)

        # Phoneme with diacritic(s)
        elif len(phoneme) > 1:

            # Convert word sequence to list type.
            phoneme = list(phoneme)
            phoneme_list = list(word)

            # Get the current index of the target phoneme.
            for phonemes in phoneme[::-1]:

                old_index = phoneme_list.index(phonemes)

                # Remove the target phoneme from the character list.
                phoneme = phoneme_list.pop(old_index)

                # Insert target phoneme at a new location.
                phoneme_list.insert(spaces, phoneme)

            # Convert word list back to str type and return.
            phoneme_list = "".join(phoneme_list)

            print(phoneme_list)

            return "".join(phoneme_list)

            # pass
