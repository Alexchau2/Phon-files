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
from diacritics_list import vowels_dip

# Example
# ɛlᵖ has 3 characters in the string
# ɛ is index 0
# l is index 1
# ᵖ is index 2
# However, Phon treats lᵖ as one index rather than two separate ones due to diacritic
# If you were to get the indexes without fixing, the output would be something like ['0', '1 2']
# where '0' corresponds to ɛ and '1 2' corresponds to lᵖ
# This function treats lᵖ as one index, but you are able to index the phoneme and diacritic separately
# Output: {('8c437a92-64f3-4438-8098-62273be265a7', 'ɛlᵖ'): ['0', ['1', '2']]}


def substitution_fixer():
    # media_folder = "C:\\Users\\alex\\Documents\\GitHub\\Combiths Lab\\Phon\\XML Files"

    media_folder = "C:\\Users\\alex\\Documents\\GitHub\\Combiths Lab\\Phon\\Test XML files"
    os.chdir(media_folder)

    # Get XML files
    xml_files = [
        xml_file
        for xml_file in listdir(media_folder)
        if isfile(join(media_folder, xml_file))
    ]

    # while True:

    #     # Ask for model/target or actual transcription information
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

    # Go through all XML files in the directory
    for files in xml_files:

        tree = ET.parse(files)
        root = tree.getroot()

        def get_transcription_information():

            # Get ids

            ids = [id.attrib["id"] for id in root.findall(speaker)]

            # Get transcriptions for each unique id into a list

            model_transcriptions = []
            actual_transcriptions = []

            # Iterate over ids
            for id in ids:
                transcriptions = []

                # Get transcription for each unique id
                for transcription in root.findall(
                    speaker
                    + str("[@id=" + "'" + id + "'" + "]/")
                    + ipaTier_model
                    + "[@form='"
                    + "model"
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
                model_transcriptions.append(transcriptions)

            # Iterate over ids
            for id in ids:
                transcriptions = []

                # Get transcription for each unique id
                for transcription in root.findall(
                    speaker
                    + str("[@id=" + "'" + id + "'" + "]/")
                    + ipaTier_model
                    + "[@form='"
                    + "actual"
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
                actual_transcriptions.append(transcriptions)

            # print(id_transcriptions)

            model_alignment_values = {
                (id, transcriptions): [
                    # Get target alignment values
                    list(map(int, alignment.get("value").split()))[
                        0
                    ]  # Get actual alignment values
                    for alignment in root.findall(  # Go to alignment tag in XML file
                        speaker
                        + str("[@id=" + "'" + id + "'" + "]/")
                        + alignment_segmental
                        + "[@type='segmental']/"
                        + transcription_length
                    )
                ]
                for (id, transcriptions) in zip(
                    ids, model_transcriptions
                )  # Iterate over ids and transcriptions
            }
            # print("\n Model alignment: ", model_alignment_values)

            actual_alignment_values = {
                (id, transcriptions): [
                    # Get target alignment values
                    list(map(int, alignment.get("value").split()))[
                        1
                    ]  # Get actual alignment values
                    for alignment in root.findall(  # Go to alignment tag in XML file
                        speaker
                        + str("[@id=" + "'" + id + "'" + "]/")
                        + alignment_segmental
                        + "[@type='segmental']/"
                        + transcription_length
                    )
                ]
                for (id, transcriptions) in zip(
                    ids, actual_transcriptions
                )  # Iterate over ids and transcriptions
            }
            # print("\n Actual alignment: ", actual_alignment_values)

            model_info = {
                (id, transcriptions): [
                    [
                        index.get("indexes"),
                        index.get("scType"),
                        index.get("hiatus"),
                    ]  # Get info for transcription
                    if "hiatus" in index.attrib  # Check if hiatus exists
                    else [
                        index.get("indexes"),
                        index.get("scType"),
                    ]  # If hiatus does not exist, then only get indexes and scType
                    for index in root.findall(  # Go to tag where info is (<sb>)
                        speaker
                        + str("[@id=" + "'" + id + "'" + "]/")
                        + ipaTier_model
                        + "[@form='"
                        + "model"
                        + "']/"
                        + transcription_indices
                    )
                ]
                for (id, transcriptions) in zip(
                    ids, model_transcriptions
                )  # Iterate over ids and transcriptions
            }

            # print("\n Model info: ", model_info)

            actual_info = {
                (id, transcriptions): [
                    [
                        index.get("indexes"),
                        index.get("scType"),
                        index.get("hiatus"),
                    ]  # Get info for transcription
                    if "hiatus" in index.attrib  # Check if hiatus exists
                    else [
                        index.get("indexes"),
                        index.get("scType"),
                    ]  # If hiatus does not exist, then only get indexes and scType
                    for index in root.findall(  # Go to tag where info is (<sb>)
                        speaker
                        + str("[@id=" + "'" + id + "'" + "]/")
                        + ipaTier_model
                        + "[@form='"
                        + "actual"
                        + "']/"
                        + transcription_indices
                    )
                ]
                for (id, transcriptions) in zip(
                    ids, actual_transcriptions
                )  # Iterate over ids and transcriptions
            }

            # print("\n Actual info: ", actual_info)
            return (model_alignment_values, actual_alignment_values)
            # return(actual_info)

    # get_transcription_information()

    model_alignment_values, actual_alignment_values = get_transcription_information()

    need_to_fix = []

    # Try to fix alignments

    for (model_align, actual_align, model_key, actual_key) in zip(
        model_alignment_values.values(),
        actual_alignment_values.values(),
        model_alignment_values,
        actual_alignment_values,
    ):

        # for (model_align_values, actual_align_values) in zip(model_align, actual_align):

        for vowel in vowels_dip:

            if len(vowel) > 1:

                skip

            else:

                for (model_align_values, actual_align_values) in zip(
                    model_align, actual_align
                ):

                    if vowel in actual_key[1]:

                        if ("l" in model_key[1]) or ("r" in model_key[1]):

                            # for (model_phoneme, actual_phoneme) in zip(model_keys[1], actual_keys[1]):
                            if (
                                (-1 == model_align_values)
                                and (
                                    (actual_align_values != -1)
                                    and (
                                        list(actual_key[1])[int(actual_align_values)]
                                        == vowel
                                    )
                                )
                            ) and (
                                (
                                    list(model_key[1])[int(model_align_values)] == "l"
                                    and -1 == actual_align_values
                                )
                                or (
                                    list(model_key[1])[int(model_align_values)] == "r"
                                    and -1 == actual_align_values
                                )
                            ):

                                # pass

                                # print(model_key[1], actual_key[1])
                                test = [model_key[1], actual_key[1]]
                                print(test, files)
                                if test in need_to_fix:
                                    pass
                                else:
                                    need_to_fix.append(test)

    print(need_to_fix)

    stop = timeit.default_timer()

    print("Time: ", stop - start)


substitution_fixer()
