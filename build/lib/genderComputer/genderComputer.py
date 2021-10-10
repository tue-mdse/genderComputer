#!/usr/bin/env python3
# This Python file uses the following encoding: utf-8

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
import re
import csv
from unidecode import unidecode

from genderComputer.dictUtils import MyDict
from genderComputer.nameUtils import only_greek_chars, only_cyrillic_chars
from genderComputer.nameUtils import leet2eng, inverseNameParts, extractFirstName
from genderComputer.filters import normaliseCountryName



def simplifiedGender(gender):
	if gender is not None:
		if gender == 'mostly male':
			return 'male'
		elif gender == 'mostly female':
			return 'female'
		# elif gender == 'unisex':
		# return ''
		else:
			return gender # male, female, unisex
	return None

def formatOutput(gender, simplified=True):
	if simplified:
		return simplifiedGender(gender)
	else:
		return gender


'''Load the male and female name lists for <country>'''
def loadData(country, dataPath, hasHeader=True):
	def loadGenderList(gender, country, dataPath, hasHeader):
		fd = open(os.path.join(dataPath, '%s%sUTF8.csv' % (country, gender)), 'r', encoding="utf8")
		reader = csv.reader(fd, delimiter=';', dialect=csv.excel)
		names = {}
		if hasHeader:
			unused_header = reader.next()
		'''Load names as-is, but lower cased'''
		for row in reader:
			name = row[0].lower()
			try:
				'''The second column should be the count
				(number of babies in some year with this name)'''
				count = row[1]
			except:
				'''If second column does not exist, default to count=1'''
				count = 1
				if name in names:
					'''If here then I've seen this name before, modulo case.
					Only count once (there is no frequency information anyway)'''
					count = 0
			if name in names:
				names[name] += count
			else:
				names[name] = count
		fd.close()
		
		'''Add versions without diacritics'''
		for name in list(names.keys()):
			dname = unidecode(name)
			if dname not in names:
				names[dname] = names[name]

		return names

	males = loadGenderList('Male', country, dataPath, hasHeader)
	females = loadGenderList('Female', country, dataPath, hasHeader)	
	return males, females


class GenderComputer():
	def __init__(self, nameListsPath=None):
		'''Data path'''
		if nameListsPath:
			self.dataPath = os.path.abspath(nameListsPath)
		else:
			self.dataPath = os.path.join(os.path.dirname(__file__), "..", "nameLists")
		
		'''gender.c, already lowercase'''
		self.genderDict = MyDict(os.path.join(self.dataPath, 'gender.dict'))
		
		'''Order of countries (columns) in the 
		nam_dict.txt file shipped together with gender.c'''
		self.countriesOrder = {
			'UK':0,
			'Ireland':1,
			'USA':2,
			'Italy':3,
			'Malta':4,
			'Portugal':5,
			'Spain':6,
			'France':7,
			'Belgium':8,
			'Luxembourg':9,
			'The Netherlands':10,
			'East Frisia':11,
			'Germany':12,
			'Austria':13,
			'Switzerland':14,
			'Iceland':15,
			'Denmark':16,
			'Norway':17,
			'Sweden':18,
			'Finland':19,
			'Estonia':20,
			'Latvia':21,
			'Lithuania':22,
			'Poland':23,
			'Czech Republic':24,
			'Slovakia':25,
			'Hungary':26,
			'Romania':27,
			'Bulgaria':28,
			'Bosnia and Herzegovina':29,
			'Croatia':30,
			'Kosovo':31,
			'Macedonia (FYROM)':32,
			'Montenegro':33,
			'Serbia':34,
			'Slovenia':35,
			'Albania':36,
			'Greece':37,
			'Russia':38,
			'Belarus':39,
			'Moldova':40,
			'Ukraine':41,
			'Armenia':42,
			'Azerbaijan':43,
			'Georgia':44,
			'Kazakhstan':45,
			'Turkey':46,
			'Arabia/Persia':47,
			'Israel':48,
			'China':49,
			'India/Sri Lanka':50,
			'Japan':51,
			'Korea':52,
			'Vietnam':53,
			'other countries':54,
		}
		self.countriesOrderRev = {}
		for country, idx in self.countriesOrder.items():
			self.countriesOrderRev[idx] = country
		
		self.threshold = 0.5
		
		self.nameLists = {}
		
		'''Name lists per country'''
		listOfCountries = ['Afghanistan', 'Albania', 'Australia', 'Belgium', 'Brazil', 
						'Canada', 'Czech', 'Finland', 'Greece', 'Hungary', 'India', 'Iran', 
						'Ireland', 'Israel', 'Italy', 'Japan', 'Latvia', 'Norway', 'Poland', 'Romania',
						'Russia', 'Slovenia', 'Somalia', 'Spain', 'Sweden', 'Turkey', 'UK', 
						'Ukraine', 'USA']
		for country in listOfCountries:
			self.nameLists[country] = {}
			self.nameLists[country]['male'], self.nameLists[country]['female'] = loadData(country, self.dataPath, hasHeader=False)
		
		'''Exceptions (approximations)'''
		#malesFrance, femalesFrance = loadData('Wallonia', self.dataPath, False)
		#self.nameLists['France'] = {}
		#self.nameLists['France']['male'] 	= malesFrance
		#self.nameLists['France']['female'] 	= femalesFrance
		
		malesNL, femalesNL = loadData('Frisia', self.dataPath, False)
		self.nameLists['The Netherlands'] = {}
		self.nameLists['The Netherlands']['male'] 	= malesNL
		self.nameLists['The Netherlands']['female'] = femalesNL
		
		'''Black list of first names'''
		self.blackList = ['The', 'the', 'nil', 'Nil', 'NULL', 'null', 
						'stack', 'cache', 'queue', 'core', 'linux', 'Net',
						'stillo', 'alfa', 'beta', 'testing', 'me']
		
		'''Gender-specific words'''
		self.maleWords = ['Mr.', 'mr.', 'Mr', 'mr', 'Sir', 'sir', 'Captain', 'captain', 'wizard', 
						'warrior', 'hillbilly', 'beer', 'Mister', 'Lord', 'Duke', 'Baron', 'coolguy']
		self.femaleWords = ['girl', 'grrl', 'grrrl', 'miss', 'Miss', 'Mrs.']
		
		'''Suffixes'''
		self.suffixes = {}
		
		self.suffixes['Russia'] = {}
		self.suffixes['Russia']['male'] = {}
		self.suffixes['Russia']['male']['include'] = ['ov','ev','sky','skiy','iy','uy','oy','skij','ij','uj','oj','off'] 
		'''in/yn excluded due to B-Rain and Earwin'''
		self.suffixes['Russia']['male']['exclude'] = ['Liubov','Ljubov','Lyubov','boy','Boy','toy','Toy','dev','Dev'] 
		'''['Iakov','Jakov','Yakov','dev','Dev','Lev','boy','Boy','toy','Toy']'''
		self.suffixes['Russia']['female'] = {}
		self.suffixes['Russia']['female']['include'] = ['ova','eva','skaya','aya','eya','oya','iaya' ]
		self.suffixes['Russia']['female']['exclude'] = {}
		
		self.suffixes['Belarus'] = self.suffixes['Russia']
		self.suffixes['Ukraine'] = self.suffixes['Russia']
		self.suffixes['Turkmenistan'] = self.suffixes['Russia']
		self.suffixes['Kyrgyzstan'] = self.suffixes['Russia']
		self.suffixes['Tajikistan'] = self.suffixes['Russia']
		self.suffixes['Kazakhstan'] = self.suffixes['Russia']
		self.suffixes['Uzbekistan'] = self.suffixes['Russia']
		self.suffixes['Azerbaijan'] = self.suffixes['Russia']
		self.suffixes['Uzbekistan'] = self.suffixes['Russia']
		self.suffixes['Bulgaria'] = self.suffixes['Russia']
		
		self.suffixes['Macedonia (FYROM)'] = {}
		self.suffixes['Macedonia (FYROM)']['male'] = {}
		self.suffixes['Macedonia (FYROM)']['male']['include'] = ['ov','ev','ski','evsk']
		self.suffixes['Macedonia (FYROM)']['male']['exclude'] = ['Iakov','Jakov','Yakov','dev','Dev','Lev','boy','Boy','toy','Toy']
		self.suffixes['Macedonia (FYROM)']['female'] = {}
		self.suffixes['Macedonia (FYROM)']['female']['include'] = ['ova','eva','ska','evska']
		self.suffixes['Macedonia (FYROM)']['female']['exclude'] = {}
		
		self.suffixes['Poland'] = {}
		self.suffixes['Poland']['male'] = {}
		self.suffixes['Poland']['male']['include'] = ['ski','sky','cki','cky']
		self.suffixes['Poland']['male']['exclude'] = {}
		self.suffixes['Poland']['female'] = {}
		self.suffixes['Poland']['female']['include'] = ['cka'] 
		'''-ska is not included because of Polska = Poland which might be confusing'''
		self.suffixes['Poland']['female']['exclude'] = {}
		
		self.suffixes['Czech Republic'] = {}
		self.suffixes['Czech Republic']['male'] = {}
		self.suffixes['Czech Republic']['male']['include'] = ['ov',u'ský','sky',u'ný','ny']
		self.suffixes['Czech Republic']['male']['include'] = ['ov','sky','ny']
		self.suffixes['Czech Republic']['male']['exclude'] = {}
		self.suffixes['Czech Republic']['female'] = {}
		self.suffixes['Czech Republic']['female']['include'] = ['ova','ska','na',u'ová',u'ská',u'ná']
		self.suffixes['Czech Republic']['female']['include'] = ['ova','ska','na']
		self.suffixes['Czech Republic']['female']['exclude'] = {}
		
		'''Male Latvian personal and family names typically end in  -s (-š). Some may be derived 
		from Russian names, with an -s ending: e.g. Vladislavs KAZANOVS
		Only Russian forms are included since we cannot distinguish between the regular Latvian -s and English plural -s'''
		
		self.suffixes['Latvia'] = {}
		self.suffixes['Latvia']['male'] = {}
		self.suffixes['Latvia']['male']['include'] = [u'š','ovs','ins']
		self.suffixes['Latvia']['male']['exclude'] = {}
		self.suffixes['Latvia']['female'] = {}
		self.suffixes['Latvia']['female']['include'] = ['ina']
		self.suffixes['Latvia']['female']['exclude'] = {}
		
		self.suffixes['Lithuania'] = {}
		self.suffixes['Lithuania']['male'] = {}
		self.suffixes['Lithuania']['male']['include'] = ['aitis', 'utis', 'ytis', 'enas', 'unas', 'inis', 'ynis', 'onis', 'ius', 'elis']
		self.suffixes['Lithuania']['male']['exclude'] = {}
		self.suffixes['Lithuania']['female'] = {}
		self.suffixes['Lithuania']['female']['include'] = ['iene', 'aite', 'yte', 'ute', 'te']
		self.suffixes['Lithuania']['female']['exclude'] = {}
		
		'''All inverse order countries should also be checked for direct order'''
		self.invOrder = ['Russia','Belarus','Ukraine','Turkmenistan','Kyrgyzstan','Tajikistan','Kazakhstan','Uzbekistan',
						 'Azerbaijan','Uzbekistan','Hungary','China','Bosnia', 'Serbia','Croatia','Sri Lanka','Vietnam',
						 'North Korea','South Korea']
		
		'''Diminutives list'''
		fd = open(os.path.join(self.dataPath, 'diminutives.csv'), 'r')
		reader = csv.reader(fd, delimiter=';', dialect=csv.excel)
		self.diminutives = {}
		for row in reader:
			mainName = row[0].strip().lower()
			for diminutive in row[1:]:
				try:
					self.diminutives[diminutive].add(mainName)
				except:
					self.diminutives[diminutive] = set()
					self.diminutives[diminutive].add(mainName)
					
		'''Distribution of StackOverflow users per different countries'''			
		fd = open(os.path.join(self.dataPath, 'countryStats.csv'), 'r')
		reader = csv.reader(fd, delimiter=';', dialect=csv.excel)
		self.countryStats = {}
		total = 0.0
		for row in reader:
			country = row[0]
			numUsers = float(row[1])
			total += numUsers
			self.countryStats[country] = numUsers
		for country in self.countryStats.keys():
			self.countryStats[country] = self.countryStats[country] / total
		
		print('Finished initialization')
	
	
	'''Look <firstName> (and potentially its diminutives) up for <country>.
	Decide gender based on frequency.'''
	def frequencyBasedLookup(self, firstName, country, withDiminutives=False):
		dims = set([firstName])
		if withDiminutives:
			try:
				dims = self.diminutives[firstName] # Includes firstName
				dims.add(firstName)
			except:
				pass
		
		countMale = 0.0
		countFemale = 0.0
		for name in dims:
			try:
				countMale += float(self.nameLists[country]['male'][name])
			except:
				pass
			try:
				countFemale += float(self.nameLists[country]['female'][name])
			except:
				pass
		
		if countMale > 0:
			if countFemale > 0:
				if countMale != 1.0 or countFemale != 1.0:
					if countMale > countFemale:
						prob = countFemale / countMale
						if prob < self.threshold:
							gender = "mostly male"
						else:
							gender = "unisex"
					else:
						prob = countMale / countFemale
						if prob < self.threshold:
							gender = "mostly female"
						else:
							gender = "unisex"
				else:
					gender = "unisex"
			else:
				gender = "male"
		else:
			if countFemale > 0:
				gender = "female"
			else:
				gender = None
		
		return gender
	
	
	'''Wrapper for <frequencyBasedLookup> that checks if data for the query <country>
	exists; can format the output.'''
	def countryLookup(self, firstName, country, withDiminutives, simplified=True):
		if country in self.nameLists.keys():
			gender = self.frequencyBasedLookup(firstName, country, withDiminutives)
			return formatOutput(gender, simplified)
		return None
	
	'''Checks whether a given <fullName> for a given <country>
	is <gender> (male/female).'''
	def checkSuffix(self, fullName, country, gender):
		for suffix in self.suffixes[country][gender]['include']:
			if fullName.endswith(suffix):
				for badSuffix in self.suffixes[country][gender]['exclude']:
					if fullName.endswith(badSuffix):
						return None
				return gender
		return None
	
	'''Given <fullName>, checks both male and female 
	name suffixes and infers gender for <country>.'''
	def suffixLookup(self, fullName, country):
		if country in self.suffixes:
			male = self.checkSuffix(fullName, country, 'male')
			if male is not None:
				return male
			else:
				female = self.checkSuffix(fullName, country, 'female')
				return female
		else:
			return None
	
	
	'''Search for a given <firstName> in the gender.c database.
	strict=True 	: look only in <country>
	simplified=True : reduce 'mostly male' to 'male' and 'mostly female' to 'female' '''
	def genderDotCLookup(self, firstName, country, strict=True, simplified=True):
		gender = None
		genderCountry = None
		country = normaliseCountryName(country)
		
		try: 
			'''Name in dictionary'''
			nameData = self.genderDict[firstName.lower()]
			
			def lab2key(lab):
				if lab in ['M', '1M', '?M']:
					return 'mmale'
				elif lab in ['F', '1F', '?F']:
					return 'mfemale'
				elif lab == '?':
					return 'uni'
			
			d = {}
			for lab in ['M', '1M', '?M', 'F', '1F', '?F', '?']:
				d[lab2key(lab)] = 0.0
			
			for [mf, frequencies] in nameData:
				for idx in range(len(frequencies)):
					hexFreq = frequencies[idx]
					if len(hexFreq.strip()) == 1:
						d[lab2key(mf)] += int(hexFreq, 16)
			
			thr = 256
			if d['mmale'] - d['mfemale'] > thr:
				gender = 'male'
			elif (thr >= d['mmale']-d['mfemale']) and (d['mmale'] > d['mfemale']):
				gender = 'mostly male'
			elif d['mfemale'] - d['mmale'] > thr:
				gender = 'female'
			elif (thr >= d['mfemale']-d['mmale']) and (d['mfemale'] > d['mmale']):
				gender = 'mostly female'
			else:
				gender = 'unisex'
			
			'''Options:
			1. I query for an existing name in a known country
			2. I query for an existing name in a country other
			than the ones I have data for'''
			if country in self.countriesOrder.keys():
				'''Here I still don't know if I have frequency information
				for this name and this country'''
				countryData = []
				'''[mf, frequencies] mf = M,1M,?M, F,1F,?F, ?, ='''
				for [mf, frequencies] in nameData:
					f = frequencies[self.countriesOrder[country]]
					if len(f.strip()) == 1:
						'''The name exists for that country'''
						countryData.append([mf, int(f, 16)])
				
				if len(countryData) == 1:
					'''The name is known for this country, and so is its gender'''
					genderCode = countryData[0][0]
					if genderCode == 'M':
						genderCountry = "male"
					elif genderCode in ['1M', '?M']:
						genderCountry = "mostly male"
					elif genderCode == 'F':
						genderCountry = "female"
					elif genderCode in ['1F', '?F']:
						genderCountry = "mostly female"
					elif genderCode == '?':
						genderCountry = "unisex"
		except:
			gender = None
		
		if strict:
			gender = genderCountry
		return formatOutput(gender, simplified)
	
	
	'''Simple check for gender-specific words (e.g., girl)'''
	def initialCheck(self, firstName):
		if firstName in self.blackList or len(firstName) < 2:
			return 'blacklist'
		elif firstName in self.maleWords:
			return 'male'
		elif firstName in self.femaleWords:
			return 'female'
		for word in ['girl']:
			if firstName.endswith(word) or firstName.startswith(word):
				return 'female'
		for word in ['guy', 'captain']:
			if firstName.endswith(word) or firstName.startswith(word):
				return 'male'
		return None
	
	
	''''Try to resolve gender based on <firstName>.
	Restrict search to a given <country>.'''
	def resolveFirstName(self, firstName, country, withDiminutives):
		'''Start with easy checks. If successful 
		then return gender directly, otherwise continue'''
		gender = self.initialCheck(firstName)
		if gender is not None:
			return gender
		
		'''If I have a list for that country, start with it'''
		if country in self.nameLists.keys():
			gender = self.countryLookup(firstName, country, withDiminutives, simplified=True)
			if gender is not None:
				return gender
		
		'''Try gender.c next (strict mode = country-dependent)'''
		gender = self.genderDotCLookup(firstName, country, strict=True, simplified=True)
		if gender is not None:
			return gender
		
		return None
	
	
	''''Try to resolve gender based on <firstName>.
	Look in all countries and resort to arbitrage.'''
	def resolveFirstNameOverall(self, firstName, withDiminutives):
		'''Start with easy checks. If successful 
		then return gender directly, otherwise continue'''
		gender = self.initialCheck(firstName)
		if gender is not None:
			return gender
		
		'''Try each available country list in turn,
		and record frequency information.'''
		genders = set()
		arbiter = {}
		for country in self.nameLists.keys():
			gender = self.countryLookup(firstName, country, withDiminutives, simplified=True)
			if gender is not None:
				genders.add(gender)
				try:
					arbiter[gender] += self.countryStats[country]
				except:
					arbiter[gender] = self.countryStats[country]
		
		'''Keep the gender with the highest total count
		(frequency) aggregated across all countries.'''
		l = [(g,c) for g, c in arbiter.items()]
		if len(l):
			ml = max(l, key=lambda pair:pair[1])
			gender = ml[0]
			return gender
					
		# If all countries agree on gender, keep. Otherwise ignore
#		if len(genders) == 1:
#			return list(genders)[0]
		
		'''I might have the name in gender.c, but for a different country'''
		gender = self.genderDotCLookup(firstName, country, strict=False, simplified=True)
		return gender
	
	
	
	'''Main gender resolution function. Process:
	- if name is written in Cyrillic or Greek, transliterate
	- if country in {Russia, Belarus, ...}, check suffix
		* name might be inversed, so also try inverse if direct fails
	- extract first name and try to resolve
		* name might be inversed, so also try inverse if direct fails
	- assume name is in fact username, and try different tricks:
		* if country in {The Netherlands, ..}, look for vd, van, ..
		* try to guess name from vbogdan and bogdanv
	- if still nothing, inverse and try first name again (maybe country was empty)'''
	def resolveGender(self, name, country):
		'''Check if name is written in Cyrillic or Greek script, and transliterate'''
		if only_cyrillic_chars(name) or only_greek_chars(name):
			name = unidecode(name)
		
		'''Initial check for gender-specific words at the beginning of the name'''
		f = name.split()[0]
		if f in self.maleWords:
			return 'male'
		elif f in self.femaleWords:
			return 'female'
		
		'''Extract first name from name string'''
		firstName = extractFirstName(name, 'direct')
		
		if country is not None:
			'''Start with suffixes
			Works well for Russians (can determine gender based on surname suffix)'''
			if country in self.suffixes.keys():
				gender = self.suffixLookup(name, country)
				if gender is not None:
					return gender
			'''If still no luck, extract first name and try to resolve'''
			gender = self.resolveFirstName(firstName, country, True)
			if gender is not None:
				if gender == 'blacklist':
					return None
				return gender
			
			'''Try to inverse if no luck
			Hungarians use reversed first/last names order'''
			if country in self.invOrder:
				gender = self.suffixLookup(inverseNameParts(name), country)
				if gender is not None:
					return gender
				
				gender = self.resolveFirstName(extractFirstName(name, 'inverse'), country, True)
				if gender is not None:
					if gender == 'blacklist':
						return None
					return gender
			
			'''Starting to get desperate by now. Assume name is in fact username,
			and try different tricks:'''
			if len(name.split()) == 1:
				'''- Try the Dutch tricks'''
				if country in ['Belgium', 'The Netherlands', 'South Africa']:
					positions = [m.start() for m in re.finditer('v', name)]
					bestMatch = []
					if len(positions):
						for pos in positions:
							gender = self.resolveFirstName(name[:pos], country, True)
							if gender is not None:
								if gender != 'blacklist':
									bestMatch.append(gender)
					gender = next((g for g in bestMatch if g != 'unisex'), None)
					if gender is not None:
						return gender
					if 'unisex' in bestMatch:
						return 'unisex'
				
				'''- Try to guess first name from: bogdanv, vbogdan'''
				# bogdanv
				gender = self.resolveFirstName(name[:-1].lower(), country, True)
				if gender is not None:
					if gender == 'blacklist':
						return None
					return gender
				# vbogdan
				gender = self.resolveFirstName(name[1:].lower(), country, True)
				if gender is not None:
					if gender == 'blacklist':
						return None
					return gender
			
			'''I can't believe I'm trying leet'''
			nameL = leet2eng(name)
			gender = self.resolveFirstName(extractFirstName(nameL, 'direct'), country, True)
			if gender is not None:
				if gender == 'blacklist':
					return None
				return gender
			
			'''Try also the unidecoded version'''
			dname = unidecode(name)
			gender = self.resolveFirstName(extractFirstName(dname, 'direct'), country, True)
			if gender is not None:
				if gender == 'blacklist':
					return None
				return gender
		
		'''If everything failed, try cross-country'''
		gender = self.resolveFirstNameOverall(firstName, True)
		if gender is not None:
			if gender == 'blacklist':
				return None
			return gender
		'''Try also unidecoded version'''
		dname = unidecode(name)
		gender = self.resolveFirstNameOverall(extractFirstName(dname, 'direct'), True)
		if gender is not None:
			if gender == 'blacklist':
				return None
			return gender
		
		if len(name.split()) == 1:
			'''- Try to guess first name from: bogdanv, vbogdan'''
			# bogdanv
			gender = self.resolveFirstNameOverall(name[:-1].lower(), True)
			if gender is not None:
				if gender == 'blacklist':
					return None
				return gender
#			 vbogdan
			gender = self.resolveFirstNameOverall(name[1:].lower(), True)
			if gender is not None:
				if gender == 'blacklist':
					return None
				return gender
				
		return None
	

def runTests():
	import os
	from testSuites import testSuite1, testSuite2
	
	dataPath = os.path.abspath(".")
	gc = GenderComputer(os.path.join(dataPath, 'nameLists'))
	
	print('Test suite 1')
	for (name, country) in testSuite1:
		print([unidecode(name), country], gc.resolveGender(name, country))
	
	print()
	print('Test suite 2')
	for (name, country) in testSuite2:
		print([unidecode(name), country], gc.resolveGender(name, country))


if __name__=="__main__":
	runTests()
