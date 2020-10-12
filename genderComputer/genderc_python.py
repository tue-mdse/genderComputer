# This Python file uses the following encoding: UTF-8

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

import os

'''char set = iso8859-1
"Non-iso" unicode chars are represented as follows'''

charMap = {
    '<A/>':chr(256),
    '<a/>':chr(257),
    '<¬>':chr(258),
    '<‚>':chr(259),
    '<A,>':chr(260),
    '<a,>':chr(261),
    '<C¥>':chr(262),
    '<c¥>':chr(263),
    '<C^>':chr(268),
    '<CH>':chr(268),
    '<c^>':chr(269),
    '<ch>':chr(269),
    '<d¥>':chr(271),
    '<–>':chr(272),
    '<DJ>':chr(272),
    '<>':chr(273),
    '':chr(273),
    '<dj>':chr(273),
    '<E/>':chr(274),
    '<e/>':chr(275),
    '<E∞>':chr(278),
    '<e∞>':chr(279),
    '<E,>':chr(280),
    '<e,>':chr(281),
    '< >':chr(282),
    '<Í>':chr(283),
    '<G^>':chr(286),
    '<g^>':chr(287),
    '<G,>':chr(290),
    '<g¥>':chr(291),
    '<I/>':chr(298),
    '<i/>':chr(299),
    '<I∞>':chr(304),
    '<i>':chr(305),
    '<IJ>':chr(306),
    '<ij>':chr(307),
    '<K,>':chr(310),
    '<k,>':chr(311),
    '<L,>':chr(315),
    '<l,>':chr(316),
    '<L¥>':chr(317),
    '<l¥>':chr(318),
    '<L/>':chr(321),
    '<l/>':chr(322),
    '<N,>':chr(325),
    '<n,>':chr(326),
    '<N^>':chr(327),
    '<n^>':chr(328),
    '<÷>':chr(336),
    '<ˆ>':chr(337),
#    'å':chr(338),
    '<OE>':chr(338),
#   'ú':chr(339),
    '<oe>':chr(339),
    '<R^>':chr(344),
    '<r^>':chr(345),
    '<S,>':chr(350),
    '<s,>':chr(351),
#    'ä':chr(352),
    '<S^>':chr(352),
    '<SCH>':chr(352),
    '<SH>':chr(352),
#    'ö':chr(353),
    '<s^>':chr(353),
    '<sch>':chr(353),
    '<sh>':chr(353),
    '<T,>':chr(354),
    '<t,>':chr(355),
    '<t¥>':chr(357),
    '<U/>':chr(362),
    '<u/>':chr(363),
    '<U∞>':chr(366),
    '<u∞>':chr(367),
    '<U,>':chr(370),
    '<u,>':chr(371),
    '<Z∞>':chr(379),
    '<z∞>':chr(380),
    '<Z^>':chr(381),
    '<z^>':chr(382),
    '<ﬂ>':chr(7838),
}

dataPath = os.path.abspath('.')

'''Replace HTML encoded unicode chars by the true unicode equivalent'''

f = open(os.path.abspath('./0717-182/nam_dict1.txt'), 'rb')
g = open(os.path.join(dataPath, 'nameLists', 'nam_dict2.txt'), 'wb')

def rewrite(s):
    suffix = s[-59:]
    prefix = s[:len(s)-len(suffix)].strip()
    for key in charMap.keys():
        prefix = prefix.replace(key, charMap[key])
    s = prefix + ' ' * (29-len(prefix)) + suffix  
    return s

idx = 0
for row in f.readlines():
    if idx >= 362:
        nrow = rewrite(row)
    else:
        nrow = row
    idx += 1
    g.write(nrow)

f.close()
g.close()

'''Read the data into a Python dictionary'''

f = open(os.path.join(dataPath, 'nameLists', 'nam_dict2.txt'), 'rb')
reader = csv.reader(f, delimiter=';', dialect=csv.excel)

genderDict = {}

idx = 0

shortNames = []    
for row in reader:
    if idx > 361:
        text = row[0]
        mf = text[:2].strip() # M,1M,?M, F,1F,?F, ?, =
        #  =  <short_name> <long_name> 
        name = text[2:29].lower().strip()
        sortingFlag = text[29] # +,-; ignore +
        frequencies = text[30:-2]
    
        if sortingFlag != '+':
            if mf == '=':
                shortNames.append([name, frequencies])
            else:
                '''"Jun+Wei" represents the names "Jun-Wei", "Jun Wei" and "Junwei"'''
                if name.find('+') != -1:
                    names = [name.replace('+','-'), name.replace('+',' '), name.replace('+','').capitalize()]
                else:
                    names = [name]
                for name in names:
                    if name in genderDict:
                        genderDict[name].append([mf, frequencies])
                    else:
                        genderDict[name] = [[mf, frequencies]]
    idx += 1
             
    
for [name, frequencies] in shortNames:
    shortName, longName = name.split()
    if shortName in genderDict and longName not in genderDict:
        for nameList in genderDict[shortName]:
            if longName in genderDict:
                genderDict[longName].append(nameList)
            else:
                genderDict[longName] = [nameList]
            
    elif longName in genderDict and shortName not in genderDict:
        for nameList in genderDict[longName]:
            if shortName in genderDict:
                genderDict[shortName].append(nameList)
            else:
                genderDict[shortName] = [nameList]
            
print(len(genderDict.keys()), 'names in dictionary')


import pickle
fdict = open(os.path.join(dataPath, 'nameLists', 'gender.dict'), "wb")
pickle.dump(genderDict, fdict)
fdict.close()
