# Gender computer
---

Python tool that tries to infer a person's gender from their `name` (first name) and `location` (country). For example, *Andrea* is a first name typically used by men in *Italy* and women in *Germany*, while *Bogdan* is a first name typically used by men irrespective of the country. Similarly, a *Russian* person called *Anna Akhmatova* is more than likely a woman because of the *-ova* suffix.

### Data provenance

The tool uses lists of `male` and `female` first names for different countries. Whenever available, the data came from national statistics institutes and was accompanied by frequency information. See [this list](https://github.com/tue-mdse/genderComputer/tree/master/nameLists) for detailes about the source of data for each country.




### Licenses

- The database is made available under the [Open Database License](http://opendatacommons.org/licenses/odbl/1.0/)
- Any rights in individual contents of the database (i.e., the data) are licensed under the [Database Contents License](http://opendatacommons.org/licenses/dbcl/1.0/)
- The Python tool is licensed under the [GNU Lesser General Public License](http://www.gnu.org/licenses/lgpl.txt) version 3
