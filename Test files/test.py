import unicodedata
import unidecode
import re
import os

folder = "C:\\Users\\alex\\Documents\\GitHub\\Combiths Lab\\Phon"
print(folder)

os.chdir(folder)

# textfile = open("C:\\Users\\alex\\Documents\\GitHub\\Combiths Lab\\Phon\\diacritic_list.txt", 'r', errors='ignore')
# filetext = textfile.read()
# textfile.close()

# matches = re.findall("[\\u*\d\w]", filetext)
# print(matches)

# pattern = re.compile("[\\u*\d\w]")
# open("diacritic_list.txt","r",encoding='utf-8')

# diacritics = []

# with open("diacritic_list.txt","a",encoding='utf-8') as f:
# with open("diacritic_list.txt",encoding='utf-8') as i: # open file for reading, i = input file 
#   with open("diacritic_list.txt","w",encoding='utf-8') as o: # open temp file in write mode, o = output 
#      for l in i: # read line by line  
#          o.write('"%s",text\n' % l[:-1]) # concate ' and text 
        # print('"' + line + '"')
    # diacritics.append('"' + i + '"')

    # for match in re.finditer(pattern, line):
        # print (i+1, match.group())

# print(diacritics)

# print(unicodedata.normalize('ᵇ̵wɛˡ'))
# accented_string = 'ᵇ̵wɛˡ'
# unaccented_string = unidecode.unidecode(accented_string)
# print(unaccented_string)

# for character in accented_string:
#     if unicodedata.combining(character):
#         print(character, " is combining character")
#     else:
#         print(character, " is not combining")

# def combine(s: str):
#   buf = None
#   for x in s:
#     if unicodedata.combining(x) != 0:
#       # combining character
#       buf += x
#     else:
#       if buf is not None:
#         yield buf
#       buf = x
#   if buf is not None:
#     yield buf

# # for character in combine(accented_string):
#     # print(character)

import unicodedata
from collections import Counter

characters = []

text = "ᵇ̵wɛˡ"

# Decompose all characters into plain letters + marking diacritics:
text = unicodedata.normalize("NFD", text)
for character in text:
    if unicodedata.category(character)[0] == "M": 
        # character is a composing mark, so agregate it with
        # previous character
        characters[-1] += character
    else:
        characters.append(character)

counting = Counter(characters)

print(counting)

# def has_diacritic(s):
#     return ''.join(c for c in unicodedata.normalize('NFD', s))

# print(has_diacritic(text))

# def strip_accents(s):
#    return ''.join(c for c in unicodedata.normalize('NFD', s)
                #   if unicodedata.category(c) != 'Mc')

# print("strip accents: ", strip_accents(text))

# str1 = "ᵇ̵wɛˡ"
# str2 = tuple(str1)
# print(str2)
# print(len(str2))

# import dcl

# print(dcl.clean_diacritics(text))
# print(dcl.has_diacritics(text))
# print(dcl.get_diacritics(text))

diacritics_list = {
    "ʰ" : "\u02B0",
    "ˡ" : "\u02E1",
    "ʱ" : "\u02B1",
    "ʲ" : "\u02B2",
    "ʳ" : "\u02B3",
    "ʴ" : "\u02B4",
    "ʵ" : "\u02B5",
    "ʶ" : "\u02B6",
    "ʷ" : "\u02B7",
    "ʸ" : "\u02B8",
    "ʹ" : "\u02B9",
    "ʺ" : "\u02BA",
    "ʻ" : "\u02BB",
    "ʼ" : "\u02BC",
    "ʽ" : "\u02BD",
    "ʾ" : "\u02BE",
    "ʿ" : "\u02BF",
    "ˀ" : "\u02C0",
    "ˁ" : "\u02C1",
    "˂" : "\u02C2",
    "˃" : "\u02C4",
    "˄" : "\u02C4",
    "˅" : "\u02C5",
    "ˆ" : "\u02C6",
    "ˇ" : "\u02C7",
    "ˈ" : "\u02C8",
    "ˉ" : "\u02C9",
    "ˊ" : "\u02CA",
    "ˋ" : "\u02CB",
    "ˌ" : "\u02CC",
    "ˍ" : "\u02CD",
    "ˎ" : "\u02CE",
    "ˏ" : "\u02CF",
    "ː" : "\u02D0",
    "ˑ" : "\u02D1",
    "˒" : "\u02D2",
    "˓" : "\u02D3",
    "˔" : "\u02D4",
    "˕" : "\u02D5",
    "˖" : "\u02D6",
    "˗" : "\u02D7",
    "˘" : "\u02D8",
    "˙" : "\u02D9",
    "˚" : "\u02DA",
    "˛" : "\u02DB",
    "˜" : "\u02DC",
    "˝" : "\u02DD",
    "˞" : "\u02DE",
    "˟" : "\u02DF",
    "ˠ" : "\u02E0",
    "ˢ" : "\u02E2",
    "ˣ" : "\u02E3",
    "ˤ" : "\u02E4",
    "˥" : "\u02E5",
    "˦" : "\u02E6",
    "˧" : "\u02E7",
    "˨" : "\u02E8",
    "˩" : "\u02E9",
    "˪" : "\u02EA",
    "˫" : "\u02EB",
    "ˬ" : "\u02EC",
    "˭" : "\u02ED",
    "ˮ" : "\u02EE",
    "˯" : "\u02EF",
    "˰" : "\u02F0",
    "˱" : "\u02F1",
    "˲" : "\u02F2",
    "˳" : "\u02F3",
    "˴" : "\u02F4",
    "˵" : "\u02F5",
    "˶" : "\u02F6",
    "˷" : "\u02F7",
    "˸" : "\u02F8",
    "˹" : "\u02F9",
    "˺" : "\u02FA",
    "˻" : "\u02FB",
    "˼" : "\u02FC",
    "˽" : "\u02FD",
    "˾" : "\u02FE",
    "˿" : "\u02FF",
    " ̀" : "\u0300",
    "̀" : "\u0301",
    " ́" : "\u0302",
    "̂ " : "\u0303",
    " ̃" : "\u0304",
    " ̄" : "\u0305",
    " ̅" : "\u0306",
    " ̆" : "\u0307",
    " ̇" : "\u0308",
    " ̉" : "\u0309",
    " ̊" : "\u030A",
    " ̋" : "\u030B",
    " ̌" : "\u030C",
    " ̍" : "\u030D",
    " ̎" : "\u030E",
    " ̏" : "\u030F",
    " ̐" : "\u0310",
    " ̑" : "\u0311",
    " ̒" : "\u0312",
    " ̓" : "\u0313",
    " ̔" : "\u0314",
    " ̕" : "\u0315",
    " ̖" : "\u0316",
    " ̗" : "\u0317",
    " ̘" : "\u0318",
    " ̙" : "\u0319",
    " ̚" : "\u031A",
    " ̛" : "\u031B",
    " ̜" : "\u031C",
    " ̝" : "\u031D",
    " ̞" : "\u031E",
    " ̟" : "\u031F",
    " ̠" : "\u0320",
    " ̡" : "\u0321",
    " ̢" : "\u0322",
    " " : "\u0323",
    " ̤" : "\u0324",
    " ̥" : "\u0325",
    " ̦" : "\u0326",
    " ̧" : "\u0327",
    " ̨" : '\u0328',
    " ̩" : "\u0329",
    " ̪" : "\u032A",
    " ̫" : "\u032B",
    " ̬" : "\u032C",
    " ̭" : "\u032D",
    " ̮" : "\u032E",
    " ̯" : "\u032F",
    " ̰" : "\u0330",
    " ̱" : "\u0331",
    " ̲" : "\u0332",
    " ̳" : "\u0333",
    " ̴" : "\u0334",
    " ̵" : "\u0335",
    " ̶" : "\u0336",
    " ̷" : "\u0337",
    " ̸" : "\u0338",
    " ̹" : "\u0339",
    " ̺" : "\u033A",
    " ̻" : "\u033B",
    " ̼" : "\u033C",
    " ̽" : "\u033D",
    " ̾" : "\u033E",
    " ̿" : "\u033F",
    " ̀" : "\u0340",
    " ́" : "\u0341",
    " ͂" : "\u0342",
    " ̓" : "\u0343",
    " ̈́" : "\u0344",
    " ͅ" : "\u0345",
    " ͆" : "\u0346",
    " ͇" : "\u0347",
    " ͈" : "\u0348",
    " ͉" : "\u0349",
    " ͊" : "\u034A",
    " ͋" : "\u034B",
    " ͌" : "\u034C",
    " ͍" : "\u034D",
    " ͎" : "\u034E",
    # " ͏" : "\u034F",
    " ͐" : "\u0350",
    " ͑" : "\u0351",
    " ͒" : "\u0352",
    " ͓" : "\u0353",
    " ͔" : "\u0354",
    " ͕" : "\u0355",
    " ͖" : "\u0356",
    " ͗" : "\u0357",
    " ͘" : "\u0358",
    " ͙" : "\u0359",
    " ͚" : "\u035A",
    " ͛" : "\u035B",
    " ͜" : "\u035C",
    " ͝" : "\u035D",
    " ͞" : "\u035E",
    " ͟" : "\u035F",
    " ͠" : "\u0360",
    " ͡" : "\u0361",
    " ͢" : "\u0362",
    " ͣ" : "\u0363",
    " ͤ" : "\u0364",
    " ͥ" : "\u0365",
    " ͦ" : "\u0366",
    "ͨ" : "\u0367",
    "ͩ" : "\u0368",
    "ͪ" : "\u0369",
    "ͫ" : "\u036A",
    "" : "\u036B",
    "ͬ" : "\u036C",
    "ͭ" : "\u036D",
    "ͮ" : "\u036E",
    "ͯ" : "\u036F",
    "ᴬ" : "\u1D2C",
    "ɫ" : "\u026B",
    "ᵖ" : "\u1D56",
    "ᵇ" : "\u1D47",
    "ᵐ" : "\u1D50",
    "ᶬ" : "\u1DAC",
    "ⁿ" : "\u207F",
    "ᶯ" : "\u1DAF",
    "ᶮ" : "\u1DAE",
    "ᵑ" : "\u1D51",
    "ᶰ" : "\u1DB0",
    "ᵗ" : "\u1D57",
    "ᵈ" : "\u1D48",
    "ᶜ" : "\u1D9C",
    "ᶡ" : "\u1DA1",
    "ᵏ" : "\u1D4F",
    "ᶢ" : "\u1DA2",
    "ᵍ" : "\u1D4D",
    # "ˀ" : "\u2C0",
    "ˀ" : "",
    "ᶲ" : "\u1DB2",
    "ᵝ" : "\u1D5D",
    "ᶠ" : "\u1DA0",
    "ᵛ" : "\u1D5B",
    "ᶿ" : "\u1DBF",
    "ᶞ" : "\u1D9E",
    # "ˢ" : "\u2E2",
    "ˢ" : "",
    "ᶻ" : "\u1DBB",
    "ᶴ" : "\u1DB4",
    "ᶝ" : "\u1D9D",
    "ᶾ" : "\u1DBE",
    "ᶽ" : "\u1DBD",
    "ᶳ" : "\u1DB3",
    "ᶼ" : "\u1DBC",
    "ᶨ" : "\u1DA8",
    # "ˣ" : "\u2E3",
    "ˣ" : "",
    # "ˠ" : "\u2E0",
    "ˠ" : "",
    "ᵡ" : "\u1D61",
    # "ʶ" : "\u2B6",
    # "ˤ" : "\u2E4",
    # "ˁ" : "\u2C1",
    # "ʰ" : "\u2B0",
    # "ʱ" : "\u2B1",
    "ʶ" : "",
    "ˤ" : "",
    "ˁ" : "",
    "ʰ" : "",
    "ʱ" : "",
    "ᶹ" : "\u1DB9",
    # "ʴ" : "\u2B4",
    # "ʵ" : "\u2B5",
    # "ʲ" : "\u2B2",
    "ʴ" : "",
    "ʵ" : "",
    "ʲ" : "",
    "ᶣ" : "\u1DA3",
    "ᶭ" : "\u1DAD",
    # "ʷ" : "\u2B7",
    # "ʳ" : "\u2B3",
    # "ˡ" : "\u2E1",
    "ʷ" : "",
    "ʳ" : "",
    "ˡ" : "",
    "ꭞ" : "\uAB5E",
    "ᶩ" : "\u1DA9",
    "ᶫ" : "\u1DAB",
    "ⁱ" : "\u2071",
    # "ʸ" : "\u2B8",
    "ʸ" : "",
    "ᶤ" : "\u1DA4",
    "ᶶ" : "\u1DB6",
    "ᵚ" : "\u1D5A",
    "ᵘ" : "\u1D58",
    "ᶦ" : "\u1DA6",
    "ᶷ" : "\u1DB7",
    "ᵉ" : "\u1D49",
    "ᶱ" : "\u1DB1",
    "ᵒ" : "\u1D52",
    "ᵊ" : "\u1D4A",
    "ᵋ" : "\u1D4B",
    "ꟹ" : "\uA7F9",
    "ᶟ" : "\u1D9F",
    "ᶺ" : "\u1DBA",
    "ᵓ" : "\u1D53",
    "ᵄ" : "\u1D44",
    "ᵅ" : "\u1D45",
    "ᶛ" : "\u1D9B",
    "ᵃ" : "\u1D43"

}

for i in text:
    print(i)
    if i in diacritics_list:
        print(i, " in list")

