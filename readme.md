# Gender computer
---

Python tool that tries to infer a person's gender from their `name` (first name) and `location` (country). For example, *Andrea* is a first name typically used by men in *Italy* and women in *Germany*, while *Bogdan* is a first name typically used by men irrespective of the country. Similarly, a *Russian* person called *Anna Akhmatova* is more than likely a woman because of the *-ova* suffix.

### Data provenance

The tool uses lists of `male` and `female` first names for different countries:

- Diminutives: 
	- http://en.wiktionary.org/wiki/Appendix:English_given_names
- Afganistan:
	- https://www.fbiic.gov/public/2008/nov/Naming_practice_guide_UK_2006.pdf UK naming practices guide
- Albania:
	- https://www.fbiic.gov/public/2008/nov/Naming_practice_guide_UK_2006.pdf UK naming practices guide
- Australia:
	- Department of Attorney General and Justice NSW, http://www.bdm.nsw.gov.au/births/popularBabyNames.htm
- Belgium: 
	- http://statbel.fgov.be/nl/modules/publications/statistiques/bevolking/prenoms_de_la_population_totale.jsp Voornamen van de bevolking op 1.1.2009 (XLS, 17.33 MB)
- Brazil:
	- http://www.dicionariodenomesproprios.com.br/nomes-masculinos/ 
	- http://www.dicionariodenomesproprios.com.br/nomes-femininos/
- Canada:
	- http://www.servicealberta.ca/1166.cfm (1990 lists)
- Czech republic: 
	- Czech name days http://www.myczechrepublic.com/czech_culture/czech_name_days/alphabetical.html
	- Diminutives http://www.myczechrepublic.com/czech_culture/czech_name_days/dimf.html and http://www.myczechrepublic.com/czech_culture/czech_name_days/dimm.html
- Finland: 
	- http://www.sci.fi/~kajun/finns/
- Frisia: 
	- http://allenamen.nl/friese_namen/jongens_namen.html and http://allenamen.nl/friese_namen/meisjes_namen.html
- Greece: 
	- http://www.fredonia.edu/faculty/emeritus/edwinlawson/greeknames/
- India:
	- www.eyeofindia.com/services/indian-names
	- www.iloveindia.com/babynames
	- http://en.wikipedia.org/wiki/Category:Indian_given_names
	- http://www.infernaldreams.com/names/Asia/India/Hin_Names.htm
- Iran:
	- http://persia.org/Information/boys.html
	- http://persia.org/Information/girls.html
- Ireland:
	- see Northern Ireland
- Israel:
	- http://www.learn-hebrew-names.com/Hebrew-names.aspx
- Italy: 
	- http://www3.istat.it/salastampa/comunicati/non_calendario/20100318_00/testointegrale20100318.pdf p.12
- Latvia:
	- http://en.wiktionary.org/wiki/Appendix:Latvian_given_names
	- http://en.wiktionary.org/wiki/Category:Latvian_male_given_names + also female
- Norway:
	- Namnestatistikk, 2011, http://www.ssb.no/emner/00/navn/
- Poland:
	- http://chomikuj.pl/justynadow/s*c5*82owniki+imion/S*c5*81OWNIK+IMION+POLSKICH,263985157.pdf	- augmented with diminutives from http://en.wiktionary.org/wiki/Appendix:Polish_given_names
- Romania:
	- http://childnamesworld.com/romanian-boy-baby-names.php?religion=Romanian&gender=boy
	- http://ro.wikipedia.org/wiki/List%C4%83_de_prenume_rom%C3%A2ne%C8%99ti
- Russia
	- http://en.wikipedia.org/wiki/Category:Russian_masculine_given_names and http://en.wikipedia.org/wiki/Category:Russian_feminine_given_names
	- http://habrahabr.ru/post/123856/
	- Male diminutives from http://irusik-05.narod.ru/index37.html
- Slovenia:
	- http://www.stat.si/eng/imena.asp
- Somalia
	- https://www.fbiic.gov/public/2008/nov/Naming_practice_guide_UK_2006.pdf UK naming practices guide
- Spain:
	- http://www.ine.es/daco/daco42/nombyapel/nombyapel.htm -> Nombres m·s frecuentes simples y exactos para total nacional y exactos por provincia de residencia
- Sweden:
	- http://www.scb.se/Pages/ProductTables____30919.aspx
- Turkey:
	- http://www.annecocuk.com/isim/isimler-xkiz.htm
	- http://www.annecocuk.com/isim/isim-erkek.htm
- UK:
	- http://www.ons.gov.uk/ons/publications/re-reference-tables.html?edition=tcm%3A77-243644
- Ukraine:
	- http://www.aratta-ukraine.com/sacred_ua.php?id=44 
	- http://database.ukrcensus.gov.ua/dw_name/tlum.asp?nom_zag=4
	- http://logistik.mybb.ru/viewtopic.php?id=141
- USA:
	- 1990 census: e.g., http://www.uta.fi/FAST/US7/NAMES/male1st.html and http://www.uta.fi/FAST/US7/NAMES/female-1.html


### Licenses

- The database is made available under the [Open Database License](http://opendatacommons.org/licenses/odbl/1.0/)
- Any rights in individual contents of the database (i.e., the data) are licensed under the [Database Contents License](http://opendatacommons.org/licenses/dbcl/1.0/)
- The Python tool is licensed under the [GNU Lesser General Public License](http://www.gnu.org/licenses/lgpl.txt) version 3
