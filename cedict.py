#A parser for the CC-Cedict. Convert the Chinese-English dictionary into a list of python dictionaries with "traditional","simplified", "pinyin", and "english" keys.
#Make sure that the cedict_ts.u8 file is in the same folder as this file, and that the name matches the file name on line 13.
#Before starting, open the CEDICT text file and delete the copyright information at the top. Otherwise the program will try to parse it and you will get an error message.
#Characters that are commonly used as surnames have two entries in CC-CEDICT. This program will remove the surname entry if there is another entry for the character. If you want to include the surnames, simply delete lines 59 and 60.
#This code was written by Franki Allegra in February 2020.

# Download CC-CEDICT: https://www.mdbg.net/chinese/dictionary?page=cc-cedict

class Dict(list):
    pass

class Word():
    traditional = ""
    simplified = ""
    pinyin = ""
    english = ""


def read():
    #open CEDICT file
    with open('cedict_ts.u8') as file:
        dictionary = Dict()
        text = file.read()
        lines = text.split('\n')
        dict_lines = list(lines)

        def parse_line(line):
            if line == '' or line.startswith('#'):
                dict_lines.remove(line)
                return 0
            line = line.rstrip('/')
            line = line.split('/')
            if len(line) <= 1:
                return 0
            english = '/'.join(line[1:])
            char_and_pinyin = line[0].split('[')
            characters = char_and_pinyin[0]
            characters = characters.split()
            traditional = characters[0]
            simplified = characters[1]
            pinyin = char_and_pinyin[1]
            pinyin = pinyin.rstrip()
            pinyin = pinyin.rstrip("]")

            word = Word()
            word.traditional = traditional
            word.simplified = simplified
            word.pinyin = pinyin
            word.english = english
            dictionary.append(word)

        def remove_surnames():
            for x in range(len(dictionary)-1, -1, -1):
                if "surname " in dictionary[x].english:
                    if dictionary[x].traditional == dictionary[x+1].traditional:
                        dictionary.pop(x)

        #make each line into a dictionary
        print("Parsing dictionary . . .")
        for line in dict_lines:
                parse_line(line)

        #remove entries for surnames from the data (optional):

        print("Removing Surnames . . .")
        remove_surnames()

        return dictionary