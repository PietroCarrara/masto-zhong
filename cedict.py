#This code was written by Franki Allegra in February 2020.

# Download CC-CEDICT: https://www.mdbg.net/chinese/dictionary?page=cc-cedict

import re

class Dict(list):
    pass

class Word():
    traditional = ""
    simplified = ""
    pinyin = ""
    english = ""
    classifier = ""

def read():
    # TODO: Check if the file is downloaded, and if it's not, download it from
    # https://www.mdbg.net/chinese/export/cedict/cedict_1_0_ts_utf-8_mdbg.zip

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
            english, classifier = parse_meaning(line[1:])
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
            word.classifier = classifier
            dictionary.append(word)

        def remove_surnames():
            for x in range(len(dictionary)-1, -1, -1):
                if "surname " in dictionary[x].english:
                    if dictionary[x].traditional == dictionary[x+1].traditional:
                        dictionary.pop(x)

        # Remove entries starting with 'variant of ...', 'erhua variant of ...' and etc.
        def remove_variants():
            for x in range(len(dictionary)-1, -1, -1):
                if re.search('^(\w* )?variant of', dictionary[x].english) != None:
                    dictionary.pop(x)

        # Triggering the parsing
        for line in dict_lines:
                parse_line(line)

        # Comment out what you want to keep
        remove_surnames()
        remove_variants()

        return dictionary

def parse_meaning(texts):
    meaning = []
    classifiers = []

    for i in texts:
        if i.startswith('CL:'):
            cl = i.lstrip('CL:').split(',')
            classifiers.extend(cl)
        else:
            meaning.append(i)

    return '/'.join(meaning), '/'.join(classifiers) if len(classifiers) > 0 else None
