# globalcompany
Web Semantic (2019) Project Assignment

How to Use
I. Data
1. Get data source from https://www.kaggle.com/peopledatalabssf/free-7-million-company-dataset. The file is in CSV format.
2. Open rdfscript folder, copy/cut the CSV file there. 
3. Run convert.py with python. You will get 50.000 data sample from the CSV as a RDF file. The file name should be companies_sorted.nt.

II. Fuseki
1. Download fuseki from https://jena.apache.org/download/. Choose apache-jena-fuseki-*version*.zip.
2. Extract zip file, open the folder.
3. Run with cmd : fuseki-server.bat. Make sure your system have java and the cmd recognized java command.
4. Open browser, go to localhost:3030. You will get a fuseki homepage.
5. Go to "manage dataset", create new dataset with name "company". Choose "TDB2" Presistence
6. With the "company" dataset, click on "upload data", and find your companies_sorted.nt. Wait until it finish uploading. It should give upload complete feedback.

III. Django
1. Open anaconda prompt
2. Make sure you have these libraries : django and SPARQLWrapper
3. Enter directory /globalcompany
4. Run command : python manage.py runserver
5. Pay attention on the locahost port given by manage.py. Usually it use localhost:8000
6. Go to url : localhost:port/companyinfo/
7. Search a company. Enjoy
