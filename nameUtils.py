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

from nameparser import HumanName
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
    text = text.replace(r"4", "A")
    text = text.replace(r"@", "a")
    text = text.replace(r"8", "B")
    text = text.replace(r"b", "b")
    text = text.replace(r"[", "C")
    text = text.replace(r"|>", "D")
    text = text.replace(r"c|", "d")
    text = text.replace(r"3", "E")
    text = text.replace(r"3", "e")
    text = text.replace(r"|=", "F")
    text = text.replace(r"(=", "f")
    text = text.replace(r"6", "G")
    text = text.replace(r"#", "H")
    text = text.replace(r"!", "i")
    text = text.replace(r"_|", "J")
    text = text.replace(r"_)", "j")
    text = text.replace(r"|<", "K")
    text = text.replace(r"I<", "k")
    text = text.replace(r"|_", "L")
    text = text.replace(r"1", "l")
    text = text.replace(r"|\/|", "M")
    text = text.replace(r"|\|", "N")
    text = text.replace(r"0", "O")
    text = text.replace(r"|*", "P")
    text = text.replace(r"O,", "Q,")
    text = text.replace(r"9", "q")
    text = text.replace(r"|^", "r")
    text = text.replace(r"$", "S")
    text = text.replace(r"5", "s")
    text = text.replace(r"7", "T")
    text = text.replace(r"-|-", "t")
    text = text.replace(r"|_|", "U")
    text = text.replace(r"(_)", "u")
    text = text.replace(r"\/", "V")
    text = text.replace(r"VV", "W")
    text = text.replace(r"uu", "w")
    text = text.replace(r"><", "X")
    text = text.replace(r"}{", "x")
    text = text.replace(r"'|'", "Y")
    text = text.replace(r"`/", "y")
    text = text.replace(r"ZZ", "Z")
    text = text.replace(r"2", "z")
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



'''Get first name from <humanName> (python-nameparser object),
for a given <order> (direct, inverse)'''
def getFirstNameFromHumanName(humanName, order):
    if (order == 'direct'):
        return humanName.first
    else: #order == 'inverse'
        return humanName.last

'''Get first name from normal string of name parts
separated by space, for a given <order> (direct, inverse)'''
def getFirstNameFromSplitName(splitName, order):
    if (order == 'direct'):
        return splitName[0]
    else: #order == 'inverse'
        return splitName[-1]


'''Extract the first name from a <name>, assuming a 
given <order>ing of first/last name parts (direct, inverse)'''
def extractFirstName(name, order):
    '''Split on dots'''
    name = ' '.join(name.split('.'))
    '''Replace numbers by whitespace'''
    oldname = name
    name = re.sub(r"\d+", "", name)
    if not len(name):
        name = re.sub(r"\d+", "_", oldname)
    name = ' '.join(name.split('_'))
    
    '''Use the Python name parser'''
    try:
        firstName = getFirstNameFromHumanName(HumanName(name), order)
    except:
        firstName = getFirstNameFromSplitName(name.split(), order)
    
    '''If fail, use heuristics'''
    if firstName.strip() == name.strip():
        '''firstName('Ben Voigt') = 'Ben Voigt'!!!'''
        if len(name.split()) == 2:
            firstName = getFirstNameFromSplitName(name.split(), order)
        else:
            '''Try CamelCase'''
            uncamel = ' '.join(splitCamelCase(name).split('_'))
            if uncamel != name:
                try:
                    firstName = HumanName(uncamel).first
                    if len(firstName.split()) == 2:
                        firstName = getFirstNameFromSplitName(firstName.split(), order)
                except:
                    firstName = getFirstNameFromSplitName(uncamel.split(), order)
    
    if firstName == 'Mc':
        firstName = ''
    if len(firstName) == 1:
        firstName = ''
    return firstName.lower()


