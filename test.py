import unicodedata
import unidecode




# print(unicodedata.normalize('ᵇ̵wɛˡ'))
accented_string = 'ᵇ̵wɛˡ'
unaccented_string = unidecode.unidecode(accented_string)
# print(unaccented_string)

# for character in accented_string:
#     if unicodedata.combining(character):
#         print(character, " is combining character")
#     else:
#         print(character, " is not combining")

def combine(s: str):
  buf = None
  for x in s:
    if unicodedata.combining(x) != 0:
      # combining character
      buf += x
    else:
      if buf is not None:
        yield buf
      buf = x
  if buf is not None:
    yield buf

for character in combine(accented_string):
    print(character)

# str1 = "ᵇ̵wɛˡ"
# str2 = tuple(str1)
# print(str2)
# print(len(str2))