"""Copyright 2012-2013
Eindhoven University of Technology
Bogdan Vasilescu

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>."""



'''Normalise country names to match those used in the gender.c database'''
def normaliseCountryName(country):
    if country in ['Algeria', 'Bahrain', 'Comoros', 'Djibouti',
                   'Egypt', 'Irak', 'Iran', 'Jordan', 'Kuwait',
                   'Lebanon', 'Libya', 'Mauritania', 'Morocco',
                   'Oman', 'Palestine', 'Qatar', 'Saudi Arabia',
                   'Somalia', 'Sudan', 'Syria', 'Tunisia',
                   'United Arab Emirates', 'Yemen']:
        return 'Arabia/Persia'
    elif country in ['Bangladesh', 'India', 'Pakistan', 'Sri Lanka']:
        return 'India/Sri Lanka'
    elif country in ['North Korea', 'South Korea']:
        return 'Korea'
    return country


import re
def convert1(name):
    first_cap_re = re.compile('(.)([A-Z][a-z]+)')
    all_cap_re = re.compile('([a-z0-9])([A-Z])')
    s1 = first_cap_re.sub(r'\1_\2', name)
    return all_cap_re.sub(r'\1_\2', s1)#.lower()


'''Reverse camel-casing: ABCDefgh -> A_B_C_Defgh'''
def splitCamelCase(name):
    newstr = name[0]
    try:
        for ch in name[1:]:
            if ch.isupper():
                newstr = '%s_%s' % (newstr, ch)
            else:
                newstr = '%s%s' % (newstr, ch)
    except:
        pass
    return newstr


'''Inverse name parts: Bogdan Vasilescu -> Vasilescu Bogdan'''
def inverseNameParts(name):
    inverse = name.split()
    inverse.reverse()
    inverse = ' '.join(inverse)
    return inverse


'''Translate 1337 to Engligh
http://simple.wikipedia.org/wiki/Leet'''
def leet2eng(text):
    text = text.replace("4", "A")
    text = text.replace("@", "a")
    text = text.replace("8", "B")
    text = text.replace("b", "b")
    text = text.replace("[", "C")
    text = text.replace("|>", "D")
    text = text.replace("c|", "d")
    text = text.replace("3", "E")
    text = text.replace("3", "e")
    text = text.replace("|=", "F")
    text = text.replace("(=", "f")
    text = text.replace("6", "G")
    text = text.replace("#", "H")
    text = text.replace("!", "i")
    text = text.replace("_|", "J")
    text = text.replace("_)", "j")
    text = text.replace("|<", "K")
    text = text.replace("I<", "k")
    text = text.replace("|_", "L")
    text = text.replace("1", "l")
    text = text.replace("|\/|", "M")
    text = text.replace("|\|", "N")
    text = text.replace("0", "O")
    text = text.replace("|*", "P")
    text = text.replace("O,", "Q,")
    text = text.replace("9", "q")
    text = text.replace("|^", "r")
    text = text.replace("$", "S")
    text = text.replace("5", "s")
    text = text.replace("7", "T")
    text = text.replace("-|-", "t")
    text = text.replace("|_|", "U")
    text = text.replace("(_)", "u")
    text = text.replace("\/", "V")
    text = text.replace("VV", "W")
    text = text.replace("uu", "w")
    text = text.replace("><", "X")
    text = text.replace("}{", "x")
    text = text.replace("'|'", "Y")
    text = text.replace("`/", "y")
    text = text.replace("ZZ", "Z")
    text = text.replace("2", "z")
    text = text.lower()
    text = text.capitalize()
    return text



import unicodedata
cyrillic_letters = {}
greek_letters = {}

'''From http://stackoverflow.com/questions/3094498/how-can-i-check-if-a-python-unicode-string-contains-non-western-letters'''

'''Check whether a given character is written in Cyrillic'''
def is_cyrillic(uchr):
    try: return cyrillic_letters[uchr]
    except KeyError:
        return cyrillic_letters.setdefault(uchr, 'CYRILLIC' in unicodedata.name(uchr))

'''Check whether a given string is written in Cyrillic'''
def only_cyrillic_chars(unistr):
    return all(is_cyrillic(uchr)
        for uchr in unistr if uchr.isalpha())

'''Check whether a given character is written in Greek'''
def is_greek(uchr):
    try: return greek_letters[uchr]
    except KeyError:
        return greek_letters.setdefault(uchr, 'GREEK' in unicodedata.name(uchr))

'''Check whether a given string is written in Greek'''
def only_greek_chars(unistr):
    return all(is_greek(uchr)
        for uchr in unistr if uchr.isalpha())




