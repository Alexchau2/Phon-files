import xml.etree.ElementTree as ET

from Diacritic_fixer import Diacritic_fixer

ns = {"": "http://phon.ling.mun.ca/ns/phonbank"}


class Session:
    """
    Session class representing a Phon session XML.

    Attributes:
        source (str or xml.etree.Element): The source data, either a file path or an XML Element.
        ns (dict): Namespace dictionary for XML element search.
        tree (xml.etree.ElementTree.ElementTree): The XML ElementTree object.
        root (xml.etree.ElementTree.Element): The root element of the XML.
        id (str): The session ID attribute.
        corpus (str): The session corpus attribute.
        version (str): The session version attribute.
        date (str): The date extracted from the header element.
        transcribers (list): List of transcriber elements in the session.
        participants (list): List of participant elements in the session.
    """

    def __init__(self, source):
        self.ns = {"": "http://phon.ling.mun.ca/ns/phonbank"}
        if isinstance(source, str):  # If data is a filepath
            self.tree = ET.parse(source)
            self.root = self.tree.getroot()
        elif isinstance(source, ET.Element):  # If data is an element
            try:
                self.tree = ET.ElementTree(source)
                self.root = source
            except Exception as exc:
                raise Exception from exc
        elif isinstance(source, ET.ElementTree):  # If data is element tree
            try:
                self.tree = source
                self.root = self.tree.getroot()
            except Exception as exc:
                raise Exception from exc
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
        self.transcribers = session.find(".//transcribers/transcriber", self.ns)

        # Extract participants
        self.participants = session.findall(".//participants/participant", self.ns)

    def get_tier_list(self, include="all"):
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

    # To Do: Add consideration of excludeFromSearch and use Record class
    def get_records(self):
        record_list = self.root.findall(".//transcript/u", self.ns)
        return record_list


class Record:
    """
    Record class representing a single record/utterance from a Phon session.

    Attributes:
        element (xml.etree.ElementTree.Element): The XML element representing the record.
        root (Session): The parent Session object of the record.
        speaker (str): The speaker attribute of the record element.
        id (str): The ID attribute of the record element.
        excludeFromSearches (str): The excludeFromSearches attribute of the record element.
        orthography (str): The orthography text extracted from the record.
        flat_tiers (dict): A dictionary of tier names and their corresponding text content.
        model_ipa_tier (xml.etree.ElementTree.Element): The IPA tier with 'model' form.
        actual_ipa_tier (xml.etree.ElementTree.Element): The IPA tier with 'actual' form.
        alignment_tier (xml.etree.ElementTree.Element): The alignment tier with 'segmental' type.

    Functions
        get_transcription: Get the aligned transcriptions for the record (dictionary).
    """

    def __init__(self, element, root):
        self.element = element
        self.root = Session(root)
        self.speaker = element.get("speaker")
        self.id = element.get("id")
        self.excludeFromSearches = element.get("excludeFromSearches")
        self.orthography = element.find("orthography/g/w", ns).text
        self.flat_tiers = {
            tier.get("tierName"): tier.text for tier in element.findall("flatTier", ns)
        }
        self.model_ipa_tier = self.element.find(".//ipaTier[@form='model']", ns)
        self.actual_ipa_tier = self.element.find(".//ipaTier[@form='actual']", ns)
        self.alignment_tier = self.element.find(".//alignment[@type='segmental']", ns)

    def get_transcription(self):
        """
        Get the aligned transcriptions for the record.

        Returns:
            dict: A dictionary containing aligned model, actual, alignment indexes.
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
                        m, m_i = rev_char_indexes["model"][ag_i][a[0]]
                        ag_model.append(m)
                        model_dict[m] = m_i  # DEBUGGING

                    # Address -1 index for omission
                    if a[1] == -1:
                        ag_actual.append(" ")
                    else:
                        # Align actual segment
                        a, a_i = rev_char_indexes["actual"][ag_i][a[1]]
                        ag_actual.append(a)
                        actual_dict[a] = a_i  # DEBUGGING
                aligned_model.append(ag_model)
                aligned_actual.append(ag_actual)
            # DEBUGGING: Check for equal length of aligned tiers
            assert len(aligned_model) == len(aligned_actual) == len(alignment), (
                f"aligned tiers are not equal length\n"
                + f"u id:{id}\n"
                + f"model:{len(aligned_model)}\n+"
                + f"actual:{len(aligned_actual)}\n"
                + f"{len(alignment)}"
            )
            aligned_tiers = {
                "model": aligned_model,
                "actual": aligned_actual,
                "alignment": alignment,
            }
            # Zip aligned tiers
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

            # DEBUGGING
            # for i_g, group in enumerate(aligned_tiers["alignment"]):
            #     print("".join(aligned_model[i_g]))
            #     print("".join(aligned_actual[i_g]))

            return aligned_tiers

        aligned_transcriptions = align_transcriptions(self, char_indexes)

        return aligned_transcriptions


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


# Test
if __name__ == "__main__":
    test_path = "/Users/pcombiths/Documents/GitHub/Phon-files/XML Test/groups-words/Anne_Pre_PC.xml"
    test_dir_path = "/Users/pcombiths/Documents/GitHub/Phon-files/XML Test/dpa"
    s = Session(test_path)
    t = s.get_records()
    r1 = Record(t[0], s.root)
    r2 = Record(t[0], s.tree)
    test_result = r1.get_transcription()
