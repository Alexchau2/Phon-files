"""Classes for parsing Phon XML session files."""

import os
import xml.etree.ElementTree as ET

import pandas as pd

from Diacritic_fixer import Diacritic_fixer

ns = {"": "http://phon.ling.mun.ca/ns/phonbank"}

class Session:
    """
    Class representing a single Phon session XML.

    Attributes:
        source (str or xml.etree.Element): The source data, either a file path or an XML Element.
        ns (dict): Namespace dictionary for XML element search.
        tree (xml.etree.ElementTree.ElementTree): The XML ElementTree object.
        root (xml.etree.ElementTree.Element): The root element of the XML.
        id (str): The session ID attribute.
        corpus (str): The session corpus attribute.
        version (str): The session version attribute.
        date (str): The date extracted from the header element of the session.
        transcribers (list): List of transcriber elements in the session.
        participants (list): List of participant elements in the session.
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
        """Get list of strings for transcriber usernames.

        Returns:
            list: List of transcriber username strings from session
        """
        transcriber_list = [transcriber.get("id") for transcriber in self.transcribers]
        return transcriber_list

    # To Do: Add consideration of excludeFromSearch and use Record class
    def get_records(self):
        """Get list of Record objects from session Element with ids and numbering.

        Returns:
            record_list: list[list[int, str, Record]]
        """
        record_counter = 0
        numbered_record_list = []
        for record_element in self.records:
            record = Record(record_element, self.root)
            record_counter+=1
            record_num = record_counter
            numbered_record_list.append([record_num, record.id, record])
        return numbered_record_list
    
    def check_session(self, to_csv=False):
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
        alignment_tier (xml.etree.ElementTree.Element): The alignment tier with 'segmental' type.
        blind_tiers
    Functions
        get_transcription: Get the aligned transcriptions for the record (dictionary).
    """

    # To Do: Handle when an element is empty or not present in the record.
    def __init__(self, element, root):
        self.element = element
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

    def get_blind_transcriptions(self):
        """
        Get blind transcriptions for different transcribers in a nested dictionary.

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
    
    def get_record_num(self):
        """
        Get the record number associated with the current session ID.

        Returns:
            record_num: int. The record number associated with the current session ID.

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
        
        check_list = ['orthography_present', 
                      'model_present', 
                      'actual_present', 
                      'alignment_present']
        check_dict = {}
        t = self.get_transcription(zip_tiers=False)
        
        check_dict['not_excluded'] = not self.exclude_from_searches

        def check_tier_content():
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


# This function is untested
def write_xml_to_file(xml_tree, output_file):
    """
    Write an XML tree to a file.

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
    #     records = s.get_records()
    #     t3 = [Record(record, s.root) for record in records]
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
    check_dir = "/Users/pcombiths/Documents/PhonWorkspace/SSDTx Phase III Blind"
    check_dir = r"R:\CLD Lab\Workspace\SSD Tx III"
    all_check_result = check_sessions(check_dir)
    pass
