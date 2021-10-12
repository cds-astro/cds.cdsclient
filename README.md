## CDS Python package to query large catalogues

**Note**: API import changed in the last version - see example below

**License** : BSD License

**Installation** : 
python3 setup.py install --user

**vizquery.py** : the vizquery package
              query all VizieR catalogues using ASU parameters
              metadata retrieving: get columns/table information 
				   and list large tables

**Examples** :
* list big catalogues : vizquery.py -l
* get columns information for 2mass (=II/246) : vizquery.py -source=II/246 -i
* query GAIA  (I/337/gaia) arroud M1 (10arcsec) : vizquery.py -source=I/337/gaia -c=M1 -c.rs=10
* get hipparcos (HIP=A) in votable : vizquery.py -source=I/239/hip_main -mime=votable -out.max=50 "HIP=1"


**Using dedicated script: find_...py**
* query 2mass arround M1: find_2mass.py M1
* query sdss12 arround '217.488910+36.086880': find_sdss-dr12.py "217.488910+36.086880"
* query gaia by offset (**allows to get the whole table by parts**) : find_gaia_edr3.py --offset 0..1000 
* query 2mass with jamg constraint: find_2mass.py --jmag="<11"
You can also query with constraints see --help 
* query sdss using identifier: find_sdss-dr12.py  --objID=1237662225689281592  --mime=tsv

**API Example**:

```
import cdsclient.find_sdss9 as sdss
process = sdss.QueryCatVizieR()
process.position = "217.091350+35.985222"
process.radius = 120
process.query_cat(limit=10)
data = process.get()
print (data)
```

