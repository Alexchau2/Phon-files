from diacritics_list import diacritics_list
import Diacritic_fixer

class Phoneme:

    # @staticmethod def move_phoneme(self, word, index):

    #     # Check if phoneme has diacritic
    #     if len(self) == 1:
    #         # Convert word sequence to list type.
    #         phoneme_list = list(word)

    #         # Get the current index of the target phoneme.
    #         old_index = phoneme_list.index(self)

    #         # Remove the target phoneme from the character list.
    #         self = phoneme_list.pop(old_index)

    #         # Insert target phoneme at a new location.
    #         phoneme_list.insert(index, self)

    #         # Convert word list back to str type and return.
    #         phoneme_list = "".join(phoneme_list)

    #         print(phoneme_list)
    #         return "".join(phoneme_list)
    #     elif len(self) > 1:
    #         pass

    @staticmethod
    def move_phoneme(word, phoneme, index):

        # Single phoneme
        if len(phoneme) == 1:
            # Convert word sequence to list type.
            phoneme_list = list(word)

            # Get the current index of the target phoneme.
            old_index = phoneme_list.index(phoneme)

            # Remove the target phoneme from the character list.
            phoneme = phoneme_list.pop(old_index)

            # Insert target phoneme at a new location.
            phoneme_list.insert(index, phoneme)

            # Convert word list back to str type and return.
            phoneme_list = "".join(phoneme_list)

            print(phoneme_list)
            return "".join(phoneme_list)
        elif len(phoneme) > 1:
            pass

    @staticmethod
    def shift_phoneme(word, phoneme, spaces):

        print(abs(spaces))

        if (
            abs(spaces) > len(word) # Exclude if spaces to shift is more than length of word
            or abs(spaces) == len(word) # Exclude if spaces to shift is same length as word
            or (word.index(phoneme) + spaces > len(word) - 1) # Exclude if 
            or spaces == 0 # Exclude if spaces to shift is 0 
            or ( # Exclude if index to shift to has phoneme with diacritic before it
                word[word.index(phoneme) + spaces] not in diacritics_list 
                and word[(word.index(phoneme) + spaces) - 1] in diacritics_list
            )
            or ( # Exclude if index to shift to has phoneme with diacritic before and after it
                word[word.index(phoneme) + spaces] not in diacritics_list
                and word[(word.index(phoneme) + spaces) - 1] in diacritics_list
                and word[(word.index(phoneme) + spaces) + 1] in diacritics_list
            )
            or ( # Exclude if index to shift to has diacritic with diacritic before it
                word[word.index(phoneme) + spaces] in diacritics_list
                and word[(word.index(phoneme) + spaces) - 1] in diacritics_list
            )
            or ( # Exclude if index to shift to has a diacritic
                spaces == -1 and word[word.index(phoneme) + spaces] in diacritics_list
            )
            or ( # Exclude if index to shift to has phoneme with diacritic after it
                word[word.index(phoneme) + spaces] in diacritics_list
                and word[(word.index(phoneme) + spaces) - 1] not in diacritics_list
                and word[(word.index(phoneme) + spaces) + 1] in diacritics_list
            )
        ):

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
