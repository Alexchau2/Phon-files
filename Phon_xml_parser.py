"""Classes for parsing Phon XML session files."""

"""
To Do: Create a class for the aligned_segments attribute of the Transcription class
    Some things: represents a matrix of the alignment for the entire transcription.
    Could also just be a function of Transcription or Record.


To Do: Incroporate Segment and Transcription classes throughout. Incorporate original and aligned indexes in Segment
To Do: Use the aligned_segments and indexes of the Transcription object to edit the record.

To Do: Use phoneme class from Phon

To Do: Add checking for presence of alignments in "session_check"
To Do: Add creation of error/info log

"""

import logging
import os
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field

import pandas as pd

from Diacritic_fixer import Diacritic_fixer

logging.basicConfig(
    filename="Phon_xml_parser.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

ET.register_namespace("","http://phon.ling.mun.ca/ns/phonbank") # Register namespace
ns = {"": "http://phon.ling.mun.ca/ns/phonbank"} # Define namespace dictionary

class Session:
    """
    Class representing a single Phon session XML.

    Attributes:
        source (str or xml.etree.Element): The source data, either a file path or an XML Element.
        ns (dict): Fixed namespace dictionary for XML element search.
        tree (xml.etree.ElementTree.ElementTree): The XML ElementTree object.
        root (xml.etree.ElementTree.Element): The root element of the XML.
        id (str): The session ID attribute.
        corpus (str): The session corpus attribute.
        version (str): The session version attribute.
        date (str): The date extracted from the header element of the session.
        transcribers (list): List of transcriber elements in the session.
        participants (list): List of participant elements in the session.
        records (list): List of records (XML Element)
        labelled_records (dict): Dictionary {record id (str): record number (int)}
    Functions: 
        get_tier_list : Return list of tiers in the session.
        get_transcribers : Return list of strings for transcriber usernames.
        get_records : Return list of Record objects from session Element with ids and numbering.
        check_session : Check each session record with check_record() and create a DataFrame with the results.
    """

    def __init__(self, source):
        self.ns = {"": "http://phon.ling.mun.ca/ns/phonbank"}
        if isinstance(source, str):  # If data is a filepath
            try:
                self.tree = ET.parse(source)
                self.root = self.tree.getroot()
            except ET.ParseError:
                # print("Session source path must be a valid XML")
                logging.error(f"Session source path must be a valid XML: {source}")
                raise Exception("Session source path must be a valid XML.")
        elif isinstance(source, ET.Element):  # If data is an element
            self.tree = ET.ElementTree(source)
            self.root = source
        elif isinstance(source, ET.ElementTree):  # If data is element tree
            self.tree = source
            self.root = self.tree.getroot()
        else:
            raise ValueError(
                "Input must be either a filepath or an XML Element object."
            )
        # Extract session attributes
        self.source = source
        session = self.root
        self.id = session.get("id")
        self.corpus = session.get("corpus")
        self.version = session.get("version")

        # Extract header attributes
        header = session.find("header", self.ns)
        self.date = header.find("date", self.ns).text

        # Extract transcribers
        self.transcribers = session.findall(".//transcribers/transcriber", self.ns)

        # Extract participants
        self.participants = session.findall(".//participants/participant", self.ns)

        # Extract records
        self.records = self.root.findall(".//transcript/u", self.ns)
        self.labelled_records = {record.get("id"):i+1 for i, record in enumerate(self.records)}

    # Len returns number of records
    def __len__(self):
        return len(self.records)
    
    def __str__(self):
        return self.id + self.corpus

    def get_tier_list(self, include="all") -> dict:
        """Return list of tiers in the session.

        Args:
            include (str, optional): Choose from ["all", "userTier", "defaultTiers"].
            Defaults to "all".

        Returns:
            defaultTier_dict: dict[ET.Element, str]
        """
        tier_dict = {}
        userTier_dict = {}
        defaultTier_dict = {}
        for tier in self.root.findall(".//tierOrder/tier", self.ns):
            tier_dict[tier] = tier.get("tierName")
        for tier in self.root.findall(".//userTiers/userTier", self.ns):
            userTier_dict[tier] = tier.get("tierName")
        if include == "all":
            return tier_dict
        if include == "userTier":
            return userTier_dict
        if include == "defaultTiers":
            default_keys = set(tier_dict.keys()).difference(set(userTier_dict.keys()))
            defaultTier_dict = {key: tier_dict[key] for key in default_keys}
            return defaultTier_dict

    def get_transcribers(self):
        """Return list of strings for transcriber usernames.

        Returns:
            list: List of transcriber username strings from session
        """
        transcriber_list = [transcriber.get("id") for transcriber in self.transcribers]
        return transcriber_list


    def get_records(self, exclude_records=True, simple_return=False, element_format=False):
        """Return list of Record objects from session Element, optionally with ids and numbering.

        Args:
            exclude_records (bool): While True excludes records marekd as "exclude from search". 
                Default is True.
            simple_return (bool): When True, returns list of Record objects. When False,
                returns record_list: list[list[int, str, Record]]
        Returns:
            record_list: list[list[int, str, Record]]
            OR
            record_list: list[Record]
        """
        record_counter = 0
        excluded_record_counter = 0
        numbered_record_list = []
        record_list = []
        for record_element in self.records:
            record = Record(record_element, self.root)
            record_counter+=1
            record_num = record_counter
            if exclude_records:
                if record.exclude_from_searches:
                    print("Record", record_num, "excluded.")  # DEBUGGING
                    excluded_record_counter += 1
                    continue
            if simple_return:
                if element_format:
                    record_list.append(record_element)
                elif not element_format:
                    record_list.append(record)

            elif not simple_return:
                if element_format:
                    numbered_record_list.append([record_num, record.id, record_element])
                elif not element_format:
                    numbered_record_list.append([record_num, record.id, record])
        if simple_return:
            return record_list
        elif not simple_return:
            return numbered_record_list

    
    def check_session(self, to_csv=False):
        """
        Check each session record with check_record() and create a DataFrame with the results.

        Parameters:
            to_csv (bool, optional): If True, the result DataFrame will be saved to a CSV file.
                                        Default is False.

        Returns:
            pandas.DataFrame: DataFrame containing the check results, indexed by 'record'.

        Example:
            # Initialize the class instance
            obj = YourClassName()

            # Perform the check on the records and get the results in DataFrame format
            results = obj.check_session(to_csv=True)

        Note:
            - The 'get_records()' method should return an iterable containing records.
            - The 'check_record()' method should return a dictionary representing the check results for each record.
            - The 'record' key will be added to each result dictionary, representing the record's identifier.
        """
        result_list = []
        for record in self.get_records():
            result = record[2].check_record()
            result['record'] = record[0]
            result_list.append(result)
        result_pd = pd.DataFrame(result_list)
        result_pd.set_index('record', inplace=True)
        if to_csv:
            output_name = "check_session.csv"
            result_pd.to_csv(output_name, index=True, encoding="utf-8")
            print(f"{output_name} saved to {os.getcwd()}")
        return result_pd


class Record:
    """
    Record class representing a single record/utterance from a Phon session.

    Attributes:
        element (xml.etree.ElementTree.Element): The XML element representing the record.
        root (Session): The parent Session object of the record.
        speaker (str): The speaker attribute of the record element.
        id (str): The ID attribute of the record element.
        segment (dict): Dictionary keys for record segmentation: "start", "duration", "unit".
        excludeFromSearches (str): The excludeFromSearches attribute of the record element.
        orthography (list of list of str): Embedded list of orthography words within groups.
        flat_tiers (dict): A dictionary of tier names and their corresponding text content.
        model_ipa_tier (xml.etree.ElementTree.Element): The IPA tier with 'model' form.
        actual_ipa_tier (xml.etree.ElementTree.Element): The IPA tier with 'actual' form.
        blind_transcriptions (list): List of blind transcription elements
        alignment_tier (xml.etree.ElementTree.Element): The alignment tier with 'segmental' type.
        
    Functions
        get_transcriptions: Return the aligned transcriptions for the record (dictionary).
        get_blind_transcriptisourceons: Return blind transcriptions for different transcribers in a nested dictionary.
        get_record_num: Return the record number associated with the current session ID.
        check_record: Check the contents of the record for properties that may indicate errors.
    """

    # To Do: Complete try/except handling when an element is empty or not present in the record.
    def __init__(self, element, root):
        self.element = element
        if isinstance(root, Session):  # If data is a Session object
            root = root.root
        elif isinstance(root, str):  # If data is a filepath
            tree = ET.parse(root)
            root = tree.getroot()
        elif isinstance(root, ET.Element):  # If data is an element
            tree = ET.ElementTree(root)
        elif isinstance(root, ET.ElementTree):  # If data is element tree
            tree = root
            root = tree.getroot()
        else:
            raise ValueError(
                "Input must be either a filepath or an XML Element object."
            )
        self.root = Session(root)
        self.root_element = root
        self.session_id = root.get("id") + ", " + root.get("corpus")
        self.speaker = element.get("speaker")
        self.id = element.get("id")
        self.record_num = self.root.labelled_records[self.id]
        self.exclude_from_searches = True if element.get("excludeFromSearches").lower() == "true" else False
        s = element.find(".//segment", ns)
        try:
            self.segment = {"start":s.get("startTime"), 
                            "duration":s.get("duration"), 
                            "unit":s.get("unitType")
            }
        except AttributeError:
            self.segment=None
        self.flat_tiers = {
            tier.get("tierName"): tier.text for tier in element.findall("flatTier", ns)
        }     
        try:
            self.notes = element.find(".//notes", ns).text
        except AttributeError:
            self.notes=None
        try:
            self.orthography = [[w.text for w in g.findall(".//w", ns)] for g in element.findall("orthography/g", ns)]
        except AttributeError:
            self.orthography=None
        self.model_ipa_tier = self.element.find(".//ipaTier[@form='model']", ns)
        self.actual_ipa_tier = self.element.find(".//ipaTier[@form='actual']", ns)
        self.blind_transcriptions = self.element.findall(".//blindTranscription", ns)
        self.alignment_tier = self.element.find(".//alignment[@type='segmental']", ns)

    # Len returns number of segments
    def __len__(self):
        return len(self.alignment_tier.findall(".//phomap", ns))
    
    
    # To Do: Export consistent dictionary format every time, even with empty tiers.
        # May be partially completed
    def extract_transcriptions(self, zip_tiers=True):
        """
        Get the aligned transcriptions for the record.

        Args:
            zip_tiers (bool): When output_class is False, zip aligned tiers. Default is True
            output_class(bool): Return Transcription class object. Default is True.


        Returns:
            aligned_transcriptions: dict[str,list[list[list[str | int]]]]
                When zip_tiers=False
            aligned_segments: list[list[list[list[str, str], list[int, int]]]
                When zip_tiers=True
            char_indexes: list[str,list[list[[[str]]|[str,int]]]]
                When missing tier data prevents alignment.

            Contains parallel aligned model, actual, alignment tier contents.
            When tier missing, returns present tiers with indices and no alignment.
        """
        orthography = self.element.find(".//orthography", ns)
        gs = []
        char_indexes = {}
        for g in orthography.findall(".//g", ns):
            orthography_words_list = [w.text for w in g.findall("w", ns)]
            gs.append(orthography_words_list)
        char_indexes["orthography"] = gs
        # Get zipped list of model characters with sb > pb indexes for each pg
        embedded_indices = Diacritic_fixer(self.element)  # Get embedded indices
        for tier in ["model", "actual"]:
            pgs = []
            tier_element = self.element.find(f".//ipaTier[@form='{tier}']", ns)
            tier_pg_list = tier_element.findall(".//pg", ns)
            try:
                for pg_e, pg_i in zip(tier_pg_list, embedded_indices[tier]):
                    t = " ".join([w.text for w in pg_e.findall("w", ns)])
                    # Iterate embedded indices.
                    # For each iteration, the chunk to extract from the transcription
                    # is determined by the length of the element.
                    temp_t = t
                    alignments = []
                    # Extract transcription characters and group with embedded indexes
                    for i in pg_i["indices"]:
                        if type(i) == int:
                            num_chars = 1
                        else:
                            num_chars = len(i)
                        extract = temp_t[:num_chars]
                        temp_t = temp_t[num_chars:]
                        alignments.append([extract, i])
                    # Could streamline by extracting the embedded indices directly from the ph element
                    pgs.append(alignments)
                char_indexes[tier] = pgs
            except KeyError as error:
                logging.warning(f"Tier missing or errored: {self.root.corpus}>{self.root.id}>{self.record_num},{self.id}")
                continue
        
        def align_transcriptions(self, char_indexes):
            alignment = [
                [
                    [int(x) for x in a_e.get("value").split()]
                    for a_e in ag.findall("phomap", ns)
                ]
                for ag in self.element.findall(".//ag", ns)
            ]
            # Create reindexed char_indexes with non-aligned characters removed
            ignore_chars = ["ˈ", "ˌ", "|", "‖", ".", " "]
            
            rev_char_indexes = char_indexes
            for tier in ["model", "actual"]:
                rev_tier_list = []
                for pg in rev_char_indexes[tier]:
                    rev_pg_list = []
                    # Iterate over reversed list for in-place update of indexing
                    for a_pair in reversed(pg):
                        # Exclude ignored characters and update indexes
                        if a_pair[0] in ignore_chars:
                            for x in reversed(rev_pg_list):
                                try:
                                    x[1] -= 1
                                except (SyntaxError, TypeError):  # Embedded lists
                                    for i, y in enumerate(reversed(x[1])):
                                        x[1][i] -= 1
                            continue
                        else:
                            # Insert from front of new list to reverse order
                            rev_pg_list.insert(0, a_pair)
                    rev_tier_list.append(rev_pg_list)
                rev_char_indexes[tier] = rev_tier_list
            # Align all tiers
            aligned_model = []
            aligned_actual = []
            model_dict = {}  # DEBUGGING
            actual_dict = {}  # DEBUGGING
            for ag_i, ag in enumerate(alignment):
                ag_model = []
                ag_actual = []
                # Iterate alignment pairs
                for a in ag:
                    # Address -1 index for omission
                    if a[0] == -1:
                        ag_model.append(" ")
                    else:
                        # Align model segment
                        m, m_i = rev_char_indexes["model"][ag_i][a[0]-1]  # Deprecated fix attempt
                        m, m_i = rev_char_indexes["model"][ag_i][a[0]]
                        ag_model.append(m)
                        model_dict[m] = m_i  # DEBUGGING

                    # Address -1 index for omission
                    if a[1] == -1:
                        ag_actual.append(" ")
                    else:
                        # Align actual segment
                        # a, a_i = rev_char_indexes["actual"][ag_i][a[1]-1]  # Deprecated fix attempt
                        a, a_i = rev_char_indexes["actual"][ag_i][a[1]]
                        ag_actual.append(a)
                        actual_dict[a] = a_i  # DEBUGGING
                aligned_model.append(ag_model)
                aligned_actual.append(ag_actual)
            # DEBUGGING: Check for equal length of aligned tiers
            assert len(aligned_model) == len(aligned_actual) == len(alignment), (
                "aligned tiers are not equal length\n"
                + f"u id:{id}\n"
                + f"model:{len(aligned_model)}\n+"
                + f"actual:{len(aligned_actual)}\n"
                + f"{len(alignment)}"
            )
            aligned_tiers = {
                "orthography": char_indexes["orthography"],
                "model": aligned_model,
                "actual": aligned_actual,
                "alignment": alignment,
            }
            if zip_tiers:
            # Zip aligned tiers (does not include orthography)
                aligned_segments = []
                for i in range(len(alignment)):
                    group = [
                        list(y)
                        for y in zip(
                            [list(x) for x in zip(aligned_model[i], aligned_actual[i])],
                            alignment[i],
                        )
                    ]
                    aligned_segments.append(group)
                return aligned_segments
            # DEBUGGING
            # for i_g, group in enumerate(aligned_tiers["alignment"]):
            #     print("".join(aligned_model[i_g]))
            #     print("".join(aligned_actual[i_g]))
            return aligned_tiers
        try:
            aligned_transcriptions = align_transcriptions(self, char_indexes)
        except KeyError as error:  # Omit aligned_transcriptions if missing tiers
            logging.warning(f"Tier missing or errored. No aligned transcriptions extracted: {self.root.corpus}>{self.root.id}>{self.record_num},{self.id}")
            return [None, char_indexes, embedded_indices]
        except IndexError as error:  # Omit aligned_transcriptions if missing tiers
            logging.warning(f"Error aligning tier data. No aligned transcriptions extracted: {self.root.corpus}>{self.root.id}>{self.record_num},{self.id}")
            return [None, char_indexes, embedded_indices]
        

        return [aligned_transcriptions, char_indexes, embedded_indices]
    

    def get_transcriptions(self):
        """
        Return a Transcription object.
        This method incorporates extract_transcriptions() generating Transcription object.
        """
        return Transcription(self)
    
    def get_blind_transcriptions(self):
        """
        Return blind transcriptions for different transcribers in a nested dictionary.

        Returns
        -------
        blind_dict : dict
            A nested dictionary containing blind transcriptions for each transcriber 
            and their respective tiers.
        """
        transcribers = self.root.get_transcribers()
        blind_dict: dict[str, dict[str, list[list[str]]]] = {}
        for tr in transcribers:
            blind_dict[tr] = tr_dict = {}
            for tr_tier in self.element.findall(
                f".//blindTranscription[@user='{tr}']", ns
            ):
                bgs: list[list[str]] = [[w.text for w in bg] for bg in tr_tier.findall("bg", ns)]
                tr_dict[tr_tier.get("form")] = bgs
        return blind_dict


    def get_record_num(self):
        """
        Return the record number associated with the current session ID.

        Returns:
            record_num (int): The record number associated with the current session ID.

        Raises:
            Exception: If the session ID is not found in the session record list.
        """
        record_num=0
        for record_list in self.root.get_records():
            if self.id==record_list[1]:
                record_num = record_list[0]
        if record_num==0:
            raise Exception("Record ID not found in session record list.")
        return record_num

    def check_record(self):

        """Check the contents of the record for properties that may indicate errors.

        This method checks the contents of the record and determines several properties related to the presence of specific tiers, 
        equal number of groups across tiers, existence of named transcribers, and validation status. The results are stored in a 
        dictionary and returned.

        Returns:
            dict: A dictionary containing the results of various checks.

        Detailed Description:
        - The `check_list` contains the names of tiers to be checked for presence in the record.
        - The `t` variable is assigned the transcription data from the record by calling the `get_transcription` method.
        - The `check_dict` is initialized as an empty dictionary to store the check results.

        check_tier_content():
            - This inner function checks for the presence of specified tiers in the transcription data.
            - It checks for the presence of 'orthography', 'model', 'actual', and 'alignment' tiers in the `t` data.
            - The results are stored in `check_dict` with keys such as 'orthography_present', 'model_present', etc.
            - If any of the essential tiers ('orthography', 'model', 'actual') are missing, 'transcriptions_present' is set to False.

        check_blind_transcription():
            - This inner function checks for named transcribers in the record.
            - It retrieves the blind transcriptions using the `get_blind_transcriptions` method.
            - It checks for the presence of named transcribers in the root and if they have 'model' and 'actual' transcriptions.
            - The results are stored in `check_dict` with keys like '{transcriber}_model_transcription', '{transcriber}_actual_transcription'.
            - If no blind transcriptions are found, 'blind_transcription_present' is set to False.

        check_validation():
            - This inner function checks the overall validation status based on the presence of blind transcriptions and essential tiers.
            - If both blind transcriptions and essential tiers are present, the record is considered 'validated'.
            - If the 'alignment' tier is also present in addition to validation, the record is considered 'validated_aligned'.

        The `check_dict` dictionary is returned containing the results of all the checks, including:
            - 'not_excluded': True if the record is not excluded from searches, False otherwise.
            - 'orthography_present', 'model_present', 'actual_present', 'alignment_present': True if the respective tier is present, False otherwise.
            - 'transcriptions_present': True if all essential tiers ('orthography', 'model', 'actual') are present, False otherwise.
            - 'equal_num_groups': True if the number of groups is equal across tiers, False otherwise.
            - 'blind_transcription_present': True if there are any blind transcriptions, False otherwise.
            - 'num_transcribers': The number of named transcribers found in the record.
            - 'validated': True if the record is validated (blind transcriptions and essential tiers present), False otherwise.
            - 'validated_aligned': True if the record is validated and also has the 'alignment' tier, False otherwise.
        """

        check_list = ['orthography_present', 
                      'model_present', 
                      'actual_present', 
                      'alignment_present']
        check_dict = {}
        t = self.extract_transcriptions(zip_tiers=False)[0]
        
        check_dict['not_excluded'] = not self.exclude_from_searches

        def check_tier_content():
            """
            Check for presence of tiers and equal number of groups across tiers.

            This inner function iterates through the list of tiers (orthography, model, actual, and alignment) and checks
            their presence in the transcription data `t`. The results are stored in the `check_dict` dictionary with
            keys suffixed by '_present'. If a tier is not present, it is marked as False, and if it is present, it is
            marked as True.

            Additionally, the function checks whether the 'orthography', 'model', and 'actual' tiers are all present. If
            they are, the 'transcriptions_present' key in `check_dict` is set to True, otherwise, it is set to False.

            The function also verifies if the number of groups is equal across the 'model', 'actual', and 'alignment'
            tiers. If they are equal, the 'equal_num_groups' key in `check_dict` is set to True. If not, it is set to
            False, and an error message is printed.
            """

            # Check for presence of tiers
            tier_list = ['orthography', 'model', 'actual', 'alignment']
            for tier in tier_list:
                if tier not in t.keys():
                    check_dict[f"{tier}_present"] = False
                    print(f"{tier} tier empty")
                else:
                    check_dict[f"{tier}_present"] = True
            if check_dict['orthography_present'] and check_dict['model_present'] and check_dict['actual_present']:
                check_dict['transcriptions_present']=True
            else:
                check_dict['transcriptions_present']=False

            # Check for equal number of groups across tiers
            try:
                if len(t['model']) == len(t['actual']) == len(t['alignment']):
                    check_dict['equal_num_groups'] = True
                else:
                    check_dict['equal_num_groups'] = False
                    logging.warning(f"Unequal number of groups across tiers: {self.root.corpus}>{self.root.id}>{self.record_num},{self.id}")
                    print("Unequal number of groups across tiers.")
            except KeyError:
                check_dict['equal_num_groups'] = False
                logging.warning(f"A tier is empty: {self.root.corpus}>{self.root.id}>{self.record_num},{self.id}")
                print("A tier is empty.")
            return
        
        check_tier_content()

        def check_blind_transcription():
            """
            Check the presence of blind transcriptions for different transcribers and tiers.

            This inner function generates a dictionary containing boolean values indicating 
            the presence of each transcriber's blind transcription for both "model" 
            and "actual" tiers, as well as any blind transcription generally.

            Returns:
                dict: A dictionary containing check results for blind transcriptions.
            """
            bts = self.get_blind_transcriptions()
            # Check for named transcribers
            for t in self.root.get_transcribers():
                if t not in bts.keys():
                    check_dict[f"{t}_model_transcription"] = False
                    check_dict[f"{t}_actual_transcription"] = False
                else:
                    for tier in ['model', 'actual']:
                        if tier not in bts[t].keys():
                            check_dict[f"{t}_{tier}_transcription"] = False
                        else:
                            check_dict[f"{t}_{tier}_transcription"] = True
            # Check for presence of any transcription
            try:
                check_dict['num_transcribers'] = len(bts)
                check_dict['blind_transcription_present'] = True
            except TypeError:
                check_dict['num_transcribers'] = 0
                check_dict['blind_transcription_present'] = False
            return
        
        check_blind_transcription()

        def check_validation():
            """
            Check the validation status of the record.

            This function checks whether the record is considered 'validated' based on the presence of blind transcriptions
            and essential tiers ('orthography', 'model', 'actual'). If both are present, the 'validated' key in `check_dict`
            is set to True; otherwise, it is set to False.

            Additionally, if the 'alignment' tier is also present, the 'validated_aligned' key in `check_dict` is set to True;
            otherwise, it is set to False.
            """

            if check_dict['blind_transcription_present'] and check_dict['transcriptions_present']:
                check_dict['validated'] = True
                if check_dict['alignment_present']:
                    check_dict['validated_aligned'] = True
                else:
                    check_dict['validated_aligned'] = False
            else:
                check_dict['validated'] = False
                check_dict['validated_aligned'] = False
            return
        
        check_validation()

        return check_dict
    
    # Working on this. Not sure if function can be within the "Record" class because it
    # calls on the Segment and Transcription classes. I think that's fine.

    def edit_record(self, replace_type:str, form:str, replacement:str, original:str=None, group:int=0, position:int=-2):
        t = Transcription(self)
        if replace_type=="position":  # "position" replace_type
            t.groups[group][position] = t.groups[group][position].replace(replacement, form)
        if replace_type =="search":  # "search" replace_type
            for group in t.groups:
                for s in group:
                    if form=="actual":  # "actual" form
                        if s.actual==original:
                            s = s.replace(replacement, form)
                    elif form=="model":  # "model" form
                        if s.model==original:
                            s = s.replace(replacement, form)
        return t
    
# To Do: Incorporate Phoneme class from other scripts
# To Do: Test error_type attribute / use Phoneme class
# To Do: Add syllable constituency, absolute char indexes
# To Do: Handle input of a raw transcription string with alignment key
class Segment:
    """
    Represent an aligned actual and target/model segment

    This class is used to store information about a segment, including its position
    within the group, aligned model and actual segment, and associated indexes.

    Attributes:
        position (int): The position of the segment within the transcription group.
        model (str): The model transcription of the segment.
        actual (str): The actual transcription of the segment.
        model_align_index (int): The index of the segment in the model tier.
        target_align_index (int): The index of the segment in the target tier.

    Parameters:
        input (list): A list containing two sub-lists, where the first sub-list contains model and actual segments,
                        and the second sub-list contains segment alignment indices.
        index (int): The position of the segment within the prosodic group.
        r (Record): The Record object associated with this segment. Should match align_indexes.
    """

    def __init__(self, input:list, position:int, group_i:int, r:Record): # index is redundant if unerrored.
        self.record = r  # parent record
        self.group_index = group_i  # group index
        self.position = position  # position of segment in list of segments
        self.model = input[0][0]  # model/target segment string
        self.actual = input[0][1]  # actual segment string
        self.model_align_index = input[1][0]  # model/target "phomap" align index
        self.actual_align_index = input[1][1]  # actual "phomap" align index
        self.model_original_index = None  # model/target original string index
        self.actual_original_index = None  # actual original string index
        # instantiate coarse error_type attribute
        if self.actual == self.model:
            self.error_type = "accurate"
        elif self.actual == " ":
            self.error_type = "deletion"
        elif self.model == " ":
            self.error_type = "insertion"
        elif self.actual is not self.model:
            self.error_type = "substitution"
        else:
            raise Exception  # Unknown error_type

        # Debugging
        # if self.model_align_index > -1 and self.actual_align_index > -1:
        #     # assert self.position == self.actual_align_index == self.model_align_index, "Alignment error"
        #     pass
        # if self.model_align_index == -1:
        #     assert self.position == self.actual_align_index, "Alignment error"
        # elif self.actual_align_index == -1:
        #     assert self.position == self.model_align_index, "Alignment error"

    # Len returns number of characters in segment
    def __len__(self):
        return len(self.actual)
    
    # Print returns model and actual strings
    def __str__(self):
        return f"{self.model}<->{self.actual}"

    def get_original_index(self, set_transcription_attrib=True, set_original_index_attrib=True):
        # This is an inherently inefficient method since it creates a Transcription object
        # for the entire record and saves only the calling segment. 
        if set_transcription_attrib:
            transcription = Transcription(r)
            self.transcription = Transcription(r)  # set transcription attribute
        else:
            transcription = Transcription(r)

        # To Do: Handle get_indexes currently has non segment characters (e.g., ˈ) in list.
            # These need to be skipped or not included in the original output.
        for tier in ["actual", "model"]:
            seg = transcription.get_indexes()[self.group_index][tier][self.position]
            if tier == "actual":
                # Alignment index should match unless seg[1]['alignment_index'] == 1
                assert seg[1]['alignment_index'] == self.actual_align_index  or seg[1]['alignment_index'] is None, "Alignment error"  # Debugging
                if set_original_index_attrib:
                    actual_original_index = seg[1]['original_index']
                    self.actual_original_index = seg[1]['original_index']  # Assign original index to attribute
                else:
                    actual_original_index = seg[1]['original_index']
            elif tier == "model":
                # Alignment index should match unless seg[1]['alignment_index'] == 1
                assert seg[1]['alignment_index'] == self.model_align_index or seg[1]['alignment_index'] is None, "Alignment error"  # Debugging
                if set_original_index_attrib:
                    model_original_index = seg[1]['original_index']
                    self.model_original_index = seg[1]['original_index']  # Assign original index to attribute 
                else:
                    model_original_index = seg[1]['original_index']
        return [model_original_index, actual_original_index]





    


    # def change_alignment():

    def replace(self, replacement:str, form:str):
        """
        Replace the content of the specified tier/form with the given replacement.

        This method allows you to replace the content of either the "model" or "actual"
        segment with the provided replacement string.

        Args:
            replacement (str): The string to replace the content with.
            form (str): The form to replace the content in ("model" or "actual").

        Returns:
            None
        """
        
        if form=="model":
            self.model = replacement
        elif form=="actual":
            self.actual = replacement

# class FlatTier:

# Represent transcription of a single prosodic group as string with indices fixed from
# Diacritic_fixer
class TranscriptionGroup:
    """
        Represent a single transcription tier group contents.

        This class organizes output directly from Record.get_transcription()[2]. T
        his class is used by the Transcription class.

        Attributes:
            id (int): The ID of the parent record.
            form (str): The tier/form, of ["actual", "model"].
            group_index (int): The index for the prosodic group in the record.
            transcription (str): The transcription string.
            indexes (list): The list of embedded character indices.

        Parameters:
            input (dict): A dictionary from get_transcription()[2].
                The dictionary should have the following keys:
                    - "id" (int): The ID of the parent record.
                    - "tier" (str): The tier/form, of ["actual", "model"].
                    - "pg" (int): The index for the prosodic group in the record.
                    - "transcriptions" (str): The transcription string.
                    - "indices" (list): The list of embedded character indices.
    """

    def __init__(self, input:dict):
        self.id = input["id"]
        self.form = input["tier"]
        self.group_index = input["pg"]
        self.transcription = input["transcriptions"]
        self.indexes = input["indices"]
        self.words = self.transcription.split(" ")
    

    def __len__(self):
        return len(self.words)

# Combines raw word group strings and aligned segment data
class Transcription:
    """
    Represent a complete transcription of a record.

    This class stores the transcription tiers and aligned segments for a record.

    Attributes:
        record (Record): The record object associated with this transcription.
        aligned_groups (list of list of Segment): A 2D list of Segment objects representing aligned groups
            of phones in the transcription.
        orthography (list of str): A list of groups from Orthography tier
        model (list of TranscriptionGroup): A list of TranscriptionGroup objects representing the model tier.
        actual (list of TranscriptionGroup): A list of TranscriptionGroup objects representing the actual tier.
        segment (dict of str): Dictionary keys for record segmentation: "start", "duration", "unit".
    Parameters:
        r (Record): a Record object. Created with Record().
    """
    # Handle when missing tiers
    def __init__(self, r:Record):
        self.record = r
        self.t = r.extract_transcriptions()
        self.t_segs = self.t[0]  # Zipped and Split Aligned Segments
        self.t_tiers = self.t[1]  # Character Alignment Indexes (by Tier/form)
        self.t_orig = self.t[2]  # Transcription strings with original character indexes
        self.orthography = r.orthography
        self.segment = r.segment
        self.notes = r.notes
        try:
            self.aligned_segments = [[Segment(phone, position, group_i, self.record) for position, phone in enumerate(group)] for group_i, group in enumerate(self.t_segs)]
        except TypeError:
            self.aligned_segments = None
        for tier in self.t_orig:
            # Model Tier
            if tier == "model":
                self.model = []
                for group in self.t_orig[tier]:
                    self.model.append(TranscriptionGroup(group))
            # Actual Tier
            elif tier == "actual":
                self.actual = []
                for group in self.t_orig[tier]:
                    self.actual.append(TranscriptionGroup(group))

    # Check that this deals appropriately with " " (used for omission and word space)
    # Check that this works when tiers missing.
    # Match segments with alignment and character indexess
    def get_indexes(self, segments_only=False):
        """
        Return a list of groups with indexed characters for "actual" and "model" tiers.

        Each group contains a dictionary with "actual" and "model" keys, where the values
        are lists of indexed characters. Each indexed character is represented as a list
        containing a phone segment string and a dictionary with "original_index" and
        "alignment_index" keys for mapping segments to the original transcription
        string.

        Returns:
            list: A list of groups, each containing indexed characters for both tiers.
        """
        groups = []  # Create a list to store groups
        try:
            self.t_orig['model']
            self.t_orig['actual']
        # Return list with empty dictionary(s) when missing tiers prevent indexing.
        except KeyError:
            logging.warning(f"Unable to get indexes for records with missing tiers: {self.record.root.corpus}>{self.record.root.id}>{self.record.record_num},{self.record.id}")
            return [{"actual":[""], "model":[""]} for x in self.orthography]
            raise Exception("Unable to get indexes for records with missing tiers.")
        

        for form in ["actual", "model"]:
            for g_i, group in enumerate(self.t_orig[form]):
                # Get original string for each group in the tier
                o = group["transcriptions"]
                # Get split list of original string chars for each group in the tier
                o_split = [c for c in o]
                # Get original character indexes for each group in the tier
                o_is = group["indices"]

                # No output when alignment is missing
                if len(o_is)==0:
                    logging.warning(f"Alignment missing: {form}, {self.record.root.corpus}>{self.record.root.id}>{self.record.record_num},{self.record.id}")
                    print(f"Alignment missing for this {form} tier")
                    return groups
                    # raise Exception("Alignment missing for this tier")  # Debugging

                # Get split list of aligned segments for each group
                a_split = self.t_segs
                # Use form for indexing
                if form == "model":
                    f = 0
                elif form == "actual":
                    f = 1
                o_c = 0  # counter for original chars list
                o_i_c = 0  # counter for original chars list
                a_c = 0  # counter for aligned segments list
                o_skip_counter = 0
                indexed_chars = []
                for o_char in o_split:  # original chars
                    # Advance in original chars list for multi-indexes
                    if o_skip_counter > 0:
                        o_skip_counter -= 1
                        continue
                    o_i = o_is[o_i_c]  # original segment index(es)
                    a_seg = a_split[g_i][a_c][0][f]  # aligned segment string
                    a_i = a_split[g_i][a_c][1][f] # aligned segment index

                    # Append an extra item for deletions and insertions. 
                    if a_i == -1:  # deletion (actual) or insertion (model)
                        assert a_seg == " "  # Debugging
                        indexed_chars.append([" ", {"original_index":o_i, "alignment_index":a_i}])
                        a_c += 1
                        # Re-extract variables due to counter update
                        a_seg = a_split[g_i][a_c][0][f]  # aligned segment string
                        a_i = a_split[g_i][a_c][1][f] # aligned segment index
                    if o_char != " " and o_char == a_seg and isinstance(o_i, int):  # If match and single index
                        # indexed_char = [o_char, o_i, a_i]  # Debugging
                        # indexed_chars.append(indexed_char)  # Debugging
                        indexed_chars.append([o_char, {"original_index":o_i, "alignment_index":a_i}])
                        o_c += 1  # Advance in original and align lists
                        o_i_c += 1
                        a_c += 1
                    elif o_char != a_seg and isinstance(o_i, list): # If not match and multi index
                        # Match with multi-index
                        span = len(o_i)
                        # Add subsequenct chars via span (2 = 1 additional)
                        for num in range(span-1):
                            o_c += 1  # Advance in original list for each extra char
                            o_char+=o_split[o_c]
                            o_skip_counter = span-1
                        indexed_chars.append([o_char, {"original_index":o_i, "alignment_index":a_i}])
                        # o_c += 1  # Advance in original and align lists
                        o_c += 1
                        o_i_c += 1
                        a_c += 1                 
                    # Non-segment characters to skip. Check that nothing else applies here.
                    elif o_char != a_seg and isinstance(o_i, int):  # If not match and single index
                        # Nonmatch
                        indexed_chars.append([o_char, {"original_index":o_i, "alignment_index":None}])
                        o_c += 1  # Advance only in original list
                        o_i_c += 1
                    # Does this condition ever get accessed?
                    elif o_char == a_seg == " ":  # If o_char is a space and matches an insertion
                        indexed_chars.append([o_char, {"original_index":o_i, "alignment_index":None}])
                        indexed_chars.append([o_char, {"original_index":o_i, "alignment_index":a_i}])
                        o_c += 1  # Advance only in original list
                        o_i_c += 1
                # Instantiate empty dictionary for each group
                try:
                    groups[g_i]
                except IndexError:
                    groups.append({})
                groups[g_i][form] = indexed_chars 
        return groups

    # Len returns number of groups
    def __len__(self):
        return len(self.t_segs)
    
    
    def get_flat_segments(self):
        """
        Return a list of all Segment objects without group boundaries.

        This method flattens the list of aligned segment objects by concatenating the segment
        objects from each group without considering the group boundaries. It returns a list of
        all the individual segment objects.

        Returns:
            list: A list containing all Segment objects without group boundaries.
        """
        flat_segments = []
        for group_segments in self.aligned_segments:
            flat_segments += group_segments
        return flat_segments
    

    def get_flat_transcriptions(self):
        """
        Return a list of original transcription strings without group boundaries.

        This method flattens the original transcriptions by concatenating the transcriptions
        from each group without the group boundaries. It returns a dictionary containing
        flattened transcriptions for "model" and "actual" forms.

        Returns:
            dict: A dictionary containing flattened transcriptions for "model" and 
                "actual" forms.
        """
        flat_orig = self.t_orig
        for form in ["model","actual"]:
            flat_orig_transcriptions = ""
            for group_orig in self.t_orig[form]:
                flat_orig_transcriptions += " " + group_orig["transcriptions"]
            flat_orig[form] = flat_orig_transcriptions
        return flat_orig  
    
    # Needs to send back to entire word string use get_indexes
    # To Implement:
    def to_xml(self):
        root = self.record.root.root
        record_ele = root.find(f".//u[@id='{self.record.id}']", ns)
        model = record_ele.find(f".//ipaTier[@form='model']", ns)
        actual = record_ele.find(f".//ipaTier[@form='actual']", ns)
        return ""


def get_element_contents(element: ET.Element) -> dict:
    """
    Extract and print attributes and child elements from an XML element.

    Args:
        element (xml.etree.ElementTree.Element): The XML element to analyze.

    Returns:
        dict: A dictionary with attributes and child elements.

    """
    key = r'{http://phon.ling.mun.ca/ns/phonbank}'
    attributes = element.attrib
    print("**************************")
    print("Element Attributes:")
    print("\t", attributes)
    child_elements = {}
    counter = 0
    for child in element.iter():
        child_str = re.search(r"(?<=}).+(?=')", str(child)).group()
        child_elements[child_str] = child
        print("\t", child_str, child.text.strip())
        if counter == 0:
            print("Child Elements:")
        counter += 1
    print("**************************")
    return {"attributes":attributes, "children":child_elements}


def write_xml_to_file(xml_tree:ET.ElementTree, output_file):
    """
    Write an XML ElementTree to a file.

    Args:
        xml_tree (xml.etree.ElementTree.ElementTree): The XML ElementTree object 
            to be written.
        output_file (str): The file path of the output file.

    Returns:
        None
    """
    try:
        with open(output_file, "wb") as file:
            xml_tree.write(file, encoding="utf-8", xml_declaration=True)  # Works without default_namespace
        print("XML tree successfully written to", output_file)
    except Exception as e:
        logging.warning(f"Error writing XML tree to file: {output_file}, {e}")
        print("Error writing XML tree to file:", e)

def check_sessions(directory, to_csv=True, ignore_autosave=True):
    """
    Perform a check on sessions in the given directory, identifying records with issues.

    Args:
        directory (str): The directory containing session files.
        to_csv (bool, optional): Whether to save the check results to a CSV file. 
            Default is True.
        ignore_autosave (bool, optional): Whether to ignore autosave files during the 
            check. Default is True.

    Returns:
        list: A list of dictionaries containing check results for each session.
    """
    
    file_list = []
    for dirpath, folders, files in os.walk(directory):
        for file in files:
            if file.endswith('.xml'):
                if ignore_autosave and "_autosave_" in file:
                    continue
                s = Session(os.path.join(dirpath, file))
                rs = s.get_records()
                check_col_labels = rs[0][2].check_record().keys()
                s_dict = {}
                s_dict['filename'] = file
                s_dict['session'] = s.id
                s_dict['corpus'] = s.corpus
                s_dict['transcribers'] = s.get_transcribers()
                s_dict['num_records'] = len(s)
                for col in check_col_labels:
                    s_dict[col] = []
                for r in rs:
                    result = r[2].check_record()
                    for col in check_col_labels:
                        if result[col]:
                            continue
                        else:
                            s_dict[col].append(r[0])
                file_list.append(s_dict)
    all_session_check = pd.DataFrame(file_list)
    all_session_check.set_index(['corpus', 'session'], inplace=True)
    if to_csv:
        output_filename = "all_session_check.csv"
        all_session_check.to_csv(output_filename, index=True, encoding='utf-8')
    return file_list


# Test
if __name__ == "__main__":

    # Test 1: Single tutorial session. First record.

    # test_path = "/Users/pcombiths/Documents/GitHub/Phon-files/XML Test/groups-words/Anne_Pre_PC.xml"
    # s = Session(test_path)

    # Test 2: Single tutorial session. Multiple records

    # test_path = "/Users/pcombiths/Documents/GitHub/Phon-files/XML Test/groups-words/Anne_Pre_PC.xml"
    # s = Session(test_path)

    # Test 3: 7 DPA sessions.

    # test_dir_path = os.path.abspath("XML Test/dpa")
    # t3_sessions = []
    # for file in os.listdir(test_dir_path):
    #     s = Session(os.path.join(test_dir_path, file))
    #     print("Session:", s.id)  # DEBUGGING
    #     records = s.get_records(simple_return=True, element_format=True)
    #     t3 = [Record(record, s. root) for record in records]
    #     t3_transcriptions = [record.get_transcription() for record in t3]
    #     t3_sessions.append(t3_transcriptions)

    # Test 4: A session with excluded records
    
    test_path = r"C:\Users\Philip\Documents\github\Phon-files\XML Files\1007_PKP_PKP Pre.xml"
    test_path = "/Users/pcombiths/Documents/GitHub/Phon-files/XML Files/1007_PKP_PKP Pre.xml"
    test_path = "/Users/pcombiths/Documents/GitHub/Phon-files/XML Test/groups-words/C401_words.xml"

    s = Session(test_path)
    r_list = s.records
    r = Record(r_list[0], s.root)
    # records = s.get_records(exclude_records=True)
    t1 = r.extract_transcriptions()
    t2 = Transcription(r)
    seg1 = t2.aligned_segments[0][0]
    # seg2 = t2.aligned_segments[0][1]
    # seg5 = t2.aligned_segments[0][4]
    # Test 5: Write to file

    # test_path = "/Users/pcombiths/Documents/GitHub/Phon-files/XML Files/2275_PKP_PKP Pre.xml"
    # s = Session(test_path)
    # rs = s.get_records()
    # r = rs[0][2]
    # t = r.get_transcription()
    # write_xml_to_file(s.tree, "output_file_A.xml")
    result = []
    for file in os.listdir("XML Files"):
        if file.endswith(".xml"):
            s = Session(os.path.join("XML Files", file))
            r_test = s.get_records(simple_return=True)
            test_list = [Transcription(r).get_indexes() for r in r_test]
            result.append(test_list)
            pass
    pass
