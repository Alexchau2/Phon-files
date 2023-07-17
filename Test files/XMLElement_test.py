# XMLElement class test

import xml.etree.ElementTree as ET

ns = {"": "http://phon.ling.mun.ca/ns/phonbank"}


class XMLElement:
    def __init__(self, element):
        self.element = element
        self.attrib = self.element.attrib
        self.text = self.element.text

    def get(self, key):
        return self.element.get(key)

    def get_attribute(self, attribute_name):
        return self.element.get(attribute_name)

    def get_attributes(self):
        return self.element.attrib

    def get_text(self):
        return self.element.text

    def get_children(self, tag=None):
        if tag:
            return [XMLElement(child) for child in self.element.iter(tag)]
        return [XMLElement(child) for child in self.element]

    def display_info(self):
        print("Tag:", self.element.tag)
        print("Attributes:", self.element.attrib)
        print("Text Content:", self.get_text())
        print("-------------------------------")

    def find(self, path):
        return XMLElement(self.element.find(path, ns))

    def findall(self, path):
        return [XMLElement(x) for x in self.element.findall(path, ns)]

    def findtext(self, path, default=None):
        return self.element.findtext(path, default=default)

    def findall_text(self, path, default=None):
        return [child.text for child in self.element.findall(path, ns)] or default

    def find_attribute(self, path, attribute_name):
        child = self.element.find(path, ns)
        if child is not None:
            return child.get(attribute_name)
        return None

    def findall_attributes(self, path, attribute_name):
        return [child.get(attribute_name) for child in self.element.findall(path, ns)]

    def find_all_elements(self, path):
        return self.element.findall(path)

    def remove_element(self, element):
        if self.parent is not None:
            self.parent.remove(element)

    def replace_element(self, old_element, new_children):
        # Helper function to replace an element with new children
        parent = old_element.parent
        index = list(parent).index(old_element)
        parent.remove(old_element)
        parent.insert(index, new_children)


# Example usage:

# Parse the XML data
tree = ET.parse(
    "/Volumes/rdss_pcombiths/CLD Lab/Workspace/Phon Training/Anne (Canvas Tutorial)/Anne_Pre_PC.xml"
)
root = tree.getroot()

# Create an XMLElement object for the root element
xml_data = XMLElement(root)

# Accessing information from the XML
print("Root Tag:", xml_data.element.tag)
print("Root Attributes:", xml_data.element.attrib)

# Get information from the <header> element
header = xml_data.find("header")
print("Header Tag:", header.element.tag)
print("Header Attributes:", header.element.attrib)
print("Header Date:", header.findtext("date"))

# Get information from the <participant> elements
participants = xml_data.findall("participants/participant")
for participant in participants:
    print("Participant ID:", participant.get_attribute("id"))
    print("Participant Name:", participant.findtext("name"))
    print("Participant Role:", participant.findtext("role"))

# Get information from the <orthography> and <ipaTier form="model"> elements
transcripts = xml_data.findall("transcript/u")
for transcript in transcripts:
    orthography = transcript.find("orthography")
    print("Orthography Words:", orthography.findall_text("w"))
    ipa_tier_model = transcript.find("ipaTier[@form='model']")
    if ipa_tier_model is not None:
        print("IPA Tier (Model) Words:", ipa_tier_model.findall_text("w"))
