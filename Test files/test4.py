test_case = {'ᵖ̵fɛnt͜θ': [['f', 'θ'], ['ᵖ', '̵', '͜'], [2, 7], [0, 1, 6]]}

transcription = []
phonemes = []

for i in test_case:
    transcription = list(i)
    print(transcription)
    for list in test_case.values():
        for diacritics in list[1]:
            
            for phonemes in list[0]:
                # print(phonemes)
                if i.find(phonemes) > i.find(diacritics):
                    # print("True")
                    if phonemes not in transcription:
                        continue
                    else:
                        transcription.remove(phonemes)
                    # print(transcription)
                else:
                    pass
print(transcription)
                    # print("false")



# for i in test_case.values():
#     for lists in i:
#         for j in lists:
#             print(j)
        # for phoneme, diacritic, phoneme_index, diacritic_index in lists:
        #     print(phoneme)
        #     print(diacritic)
        #     print(phoneme_index)
        #     print(diacritic_index)