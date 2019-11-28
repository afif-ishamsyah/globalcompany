# globalcompany
Web Semantic (2019) Project Assignment

This project webpage can be accessed in [https://globalcompanies.herokuapp.com](https://globalcompanies.herokuapp.com)

## How to use (after you clone this git) :

### Data
1. Get data source from https://www.kaggle.com/peopledatalabssf/free-7-million-company-dataset. 
2. You will get a zip folder. Extract it, and you will get a CSV file. The name file should be companies_sorted.csv. DONT RENAME IT
2. Open rdfscript folder, copy/cut the CSV file there. 
3. Run convert.py with python. You will get 50.000 data sample from the CSV as a RDF file. The file name should be companies_sorted.nt. DONT CHANGE IT

### Fuseki
1. Download fuseki from https://jena.apache.org/download/. Choose apache-jena-fuseki-*version*.zip.
2. Extract zip file, open the folder. You can place the folder you extracted everywhere. However, it is recommended to be put as shown below.
```
|-apache-jena-fuseki-3.13.1
|--fuseki-server.bat
|-companyinfo
|-globalcompany
|-rdfscript
|-.gitignore
|-db.sqlite3
|-manage.py
|-README.md
```
3. Run with cmd : fuseki-server.bat. Make sure your system have java and the cmd recognized java command.
4. Open browser, go to localhost:3030. You will get a fuseki homepage.
5. Go to "manage dataset", create new dataset with name "company". Choose "TDB2" Presistence
6. With the "company" dataset, click on "upload data", and find your companies_sorted.nt. Wait until it finish uploading. It should give upload complete feedback.

### Django
1. Open anaconda prompt.
2. Make sure you have these libraries : django and SPARQLWrapper.
3. Enter directory /globalcompany.
4. Run command : python manage.py runserver.
5. Pay attention on the locahost port given by manage.py. Usually it use localhost:8000.
6. Go to url : localhost:port/companyinfo/.
7. Search a company. Enjoy.

*Credits : https://github.com/r4isstatic/csv-to-ttl/blob/master/csv-ttl-convert-v1.py as template to convert csv to ntriples.*
