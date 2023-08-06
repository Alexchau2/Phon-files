"""Classes for parsing Phon XML session files."""

import os
import re
import xml.etree.ElementTree as ET

import pandas as pd

from Diacritic_fixer import Diacritic_fixer

ns = {"": "http://phon.ling.mun.ca/ns/phonbank"}

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
            self.tree = ET.parse(source)
            self.root = self.tree.getroot()
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
                return record_list
            elif not simple_return:
                if element_format:
                    numbered_record_list.append([record_num, record.id, record_element])
                elif not element_format:
                    numbered_record_list.append([record_num, record.id, record])
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
        segment
        excludeFromSearches (str): The excludeFromSearches attribute of the record element.
        orthography (str): The orthography text extracted from the record.
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

    # To Do: Check handling when an element is empty or not present in the record.
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
        self.segment = element.get("segment")
        # self.exclude_from_searches = element.get("excludeFromSearches")
        # if element.get("excludeFromSearches").lower()=="true":
        #     self.exclude_from_searches = True
        # else:
        #     self.exclude_from_searches = False
        self.exclude_from_searches = True if element.get("excludeFromSearches").lower() == "true" else False
        try:
            self.orthography = element.find("orthography/g/w", ns).text
        except AttributeError:
            self.orthography=None
        
        self.flat_tiers = {
            tier.get("tierName"): tier.text for tier in element.findall("flatTier", ns)
        }
        self.model_ipa_tier = self.element.find(".//ipaTier[@form='model']", ns)
        self.actual_ipa_tier = self.element.find(".//ipaTier[@form='actual']", ns)
        self.blind_transcriptions = self.element.findall(".//blindTranscription", ns)
        self.alignment_tier = self.element.find(".//alignment[@type='segmental']", ns)

    def __len__(self):
        return len(self.alignment_tier.findall(".//phomap", ns))
    
    
    # To Do: Export consistent dictionary format every time, even with empty tiers
    def get_transcription(self, zip_tiers=True) :
        """
        Get the aligned transcriptions for the record.

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
                print(error, "tier missing or errored.")
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
        except KeyError as error:
            print("***************************")
            print(f"{self.root.corpus}>{self.root.id}>{self.record_num}")  # {self.get_record_num()}
            print(char_indexes)
            print("\t",error)
            print(
                "\tIncomplete or missing tier data. No aligned transcriptions extracted."
            )
            
            return char_indexes
        except IndexError as error:
            print("***************************")
            print(f"{self.root.corpus}>{self.root.id}>{self.record_num}")  # {self.get_record_num()}
            print(char_indexes)
            print("\t",error)
            print(
                "\tError aligning tier data. No aligned transcriptions extracted."
            )
            return char_indexes
        return aligned_transcriptions
    

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
        t = self.get_transcription(zip_tiers=False)
        
        check_dict['not_excluded'] = not self.exclude_from_searches

        def check_tier_content():
            """
            Check for presence of tiers and equal number of groups across tiers.

            This function iterates through the list of tiers (orthography, model, actual, and alignment) and checks
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
                    print("Unequal number of groups across tiers.")
            except KeyError:
                check_dict['equal_num_groups'] = False
                print("A tier is empty.")
            return
        
        check_tier_content()

        def check_blind_transcription():
            
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

# This function is untested
def write_xml_to_file(xml_tree:ET.ElementTree, output_file):
    """
    Write an XML ElementTree to a file.

    Args:
        xml_tree (xml.etree.ElementTree.ElementTree): The XML ElementTree object to be written.
        output_file (str): The file path of the output file.

    Returns:
        None
    """
    try:
        with open(output_file, "wb") as file:
            xml_tree.write(file, encoding="utf-8", xml_declaration=True)
        print("XML tree successfully written to", output_file)
    except Exception as e:
        print("Error writing XML tree to file:", e)

def check_sessions(directory, to_csv=True, ignore_autosave=True):
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
                # s.check_session


                # For each column, look for errored values. 
                # Return the record numbers for rows with erorred value.
                # List of record numbers become the entry for that session in that column
                # of the new DataFrame.


# Test
if __name__ == "__main__":

    # Test 1: Single tutorial session. First record.

    # test_path = "/Users/pcombiths/Documents/GitHub/Phon-files/XML Test/groups-words/Anne_Pre_PC.xml"
    # s = Session(test_path)
    # t = s.get_records()
    # r1 = Record(t[0], s.root)
    # r2 = Record(t[0], s.tree)
    # test_result = r1.get_transcription()

    # Test 2: Single tutorial session. Multiple records

    # test_path = "/Users/pcombiths/Documents/GitHub/Phon-files/XML Test/groups-words/Anne_Pre_PC.xml"
    # s = Session(test_path)
    # records = s.get_records()
    # t2 = [Record(record, s.root) for record in records]
    # t2_transcription = [record.get_transcription() for record in t2]
    # pass  # Access e.g.: t2_0['model'][0][0]

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
    # pass

    # Test 4: Blind sessions

    # test_path = "/Users/pcombiths/Documents/GitHub/Phon-files/XML Test/blind/B319.xml"
    # test_dir = "/Users/pcombiths/Documents/GitHub/Phon-files/XML Test/blind"
    # s = Session(test_path)
    # s_list = []
    # for dirpath, dirs, files in os.walk(test_dir):
    #     for file in files:
    #         s_list.append(Session(os.path.join(dirpath, file)))
    # for s in s_list:
    #     records = s.get_records()
    #     t2 = [record[2] for record in records]
    #     t2_transcriptions_aligned = [record.get_transcription(zip_tiers=True) for record in t2]
    #     t2_transcriptions = [record.get_transcription(zip_tiers=False) for record in t2]
    #     # for record in t2:
    #     #     print(record.get_transcription())
    #     t2[0].get_blind_transcriptions()
    #     print("START")
    #     print("***************************")
    #     for t in t2:
    #         # print(t.get_blind_transcriptions())
    #         t.check_record()
    #     # t2[0].check_record()
    # print("DONE")
    # check_result = s.check_session(to_csv=False)

    # Test 4: A session with excluded records
    
    # test_path = "/Users/pcombiths/Documents/GitHub/Phon-files/XML Test/blind/C401_exclusions.xml"
    # s = Session(test_path)
    # p = s.participants[0]
    # r_list = s.records
    # r = Record(r_list[0], s.root) #Add functionality so it can take the Session object too.
    # records = s.get_records(exclude_records=True)

    # Test 4: Write to file
    test_path = "/Users/pcombiths/Documents/GitHub/Phon-files/XML Files/2275_PKP_PKP Pre.xml"
    s = Session(test_path)
    pass
