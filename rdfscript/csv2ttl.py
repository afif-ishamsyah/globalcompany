#!/usr/bin/env python

#import the CSV module for dealing with CSV files
import csv
import io
import re
import string
from datetime import datetime
from urllib.parse import unquote

start_time = datetime.now()
print('start time: ' + str(start_time))

#create a 'reader' variable, which allows us to play with the contents of the CSV file
#in order to do that, we create the ifile variable, open the CSV file into that, then pass its' contents into the reader variable.
ifile = io.open('companies_sorted.csv', 'r', encoding='utf8')
reader = csv.reader(ifile)

#create a new variable called 'outfile' (could be any name), which we'll use to create a new file that we'll pass our TTL into.
outfile = io.open('companies_sorted.ttl', 'a', encoding='utf8')

def preprocess(data, isLiteralorURI):
	data = str(data)
	bad_char = ['<', '>', '|', '(', ')', '[', ']', ',', '"', '\\', '{', '}', '^', "'", ':', ';', "`", '+', '*', '=', '!', '?', '~']
	data = str(data.encode('ascii', 'ignore').decode('utf-8'))
	data = ''.join(i for i in data if not i in bad_char)
	printable = set(string.printable)
	data = ''.join(filter(lambda x: x in printable, data))
	data = re.sub(u'[\u2018\u2019\u201a\u201b\u2039\u203a]','', data)
	if(isLiteralorURI == 1):
		data = data.replace('\t', ' ').replace('\n', ' ').lstrip()
	elif(isLiteralorURI == 0):
		data = data.lstrip().replace('&', ' and ').replace('@', ' at ').replace('%', ' ').replace('$',' ')
		data = data.replace('-', ' ').replace('\n', '_').replace('\t', '_').replace('.', '').replace('/', '')
		data = re.sub(' +', ' ', data).replace(' ', '_')
	return data

outfile.write("@prefix gco: <https://globalcompany.org/ns#> .\n")
outfile.write("@prefix gcor: <https://globalcompany.org/resource/> .\n")
outfile.write("@prefix dct: <http://purl.org/dc/terms/> .\n")
outfile.write("@prefix owl: <http://www.w3.org/2002/07/owl#> .\n")
outfile.write("@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n")
outfile.write("@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n")
outfile.write("@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n\n")


#get python to loop through each row in the CSV, and ignore the first row.
count = 0
countfile = 0
rownum = 0
industry_list = []
cityStateDict = {}
stateCountryDict = {}

for row in reader:
	if rownum == 0: # if it's the first row, then ignore it, move on to the next one.
		pass
	else: # if it's not the first row, place the contents of the row into the 'c' variable, then create a 'd' variable with the stuff we want in the file.
		c = row

		id = preprocess(c[0], 1)
		companyname = preprocess(c[1], 0)

		id = 'gco:' + c[0] + ' a gco:ID ;\n'
		hasname_id = '\tgco:hasName gco:' + companyname + ' ;\n'
		labelid = '\trdfs:label "' + c[0] + '" .\n'
		outfile.write(id)
		outfile.write(hasname_id)
		outfile.write(labelid)

		companyname = preprocess(c[1], 0)
		globalcompany = 'gco:' + companyname + ' a gco:GlobalCompany ;\n'
		outfile.write(globalcompany)

		labelname = preprocess(c[1], 1).replace('/', '')
		labelname =  '\trdfs:label' + ' ' + '\"' + labelname + '\"' + ' ' + ';\n'
		outfile.write(labelname)

		if(str(c[2]) != ""):
			website = preprocess(c[2], 1)
			domain =  '\tgco:hasOfficialWebsite' + ' ' + '\"' + website + '\"' + ' ' + ';\n'
			outfile.write(domain)

		if(str(c[3]) != ""):
			year = '\tgco:yearFound' + ' ' + '\"' + c[3] + '\"' + '^^xsd:integer' + ' ' + ';\n'
			outfile.write(year.replace('.0', ''))

		if(str(c[4]) != ""):
			inc = preprocess(c[4], 0)
			industry = '\tgco:isIndustry' + ' ' + 'gco:' + inc + ' ' + ';\n'
			outfile.write(industry)

			industry_list.append(inc)

		if(str(c[5]) != ""):
			company_size = str(c[5]).replace('\t', ' ').replace('\n', ' ')
			size = '\tgco:hasSizeRange' + ' ' + '\"' + company_size + '\"' + ' ' + ';\n'
			outfile.write(size)

		if(str(c[6]) != ""):
			locality = c[6].split(", ")
			city = preprocess(locality[0], 0)
			state = preprocess(locality[1], 0)
			country = preprocess(locality[2], 0)
			cityLocated = '\tgco:locatedInCity' + ' ' + 'gco:' + city + ' ' + ';\n'
			stateLocated = '\tgco:locatedInState' + ' ' + 'gco:' + state + ' ' + ';\n'
			countryLocated = '\tgco:locatedInCountry' + ' ' + 'gco:' + country + ' ' + ';\n'
			outfile.write(cityLocated)
			outfile.write(stateLocated)
			outfile.write(countryLocated)

			cityStateDict[city] = state
			stateCountryDict[state] = country

		if(str(c[8]) != ""):
			uri = preprocess(c[8], 1)
			linkedin = '\tgco:hasLinkedinURL' + ' ' + '\"' + uri + '\"' + ' ' + ';\n'
			outfile.write(linkedin)

		if(str(c[9]) != ""):
			current = '\tgco:hasCurrentEmployee' + ' ' + '\"' + c[9] + '\"' + '^^xsd:integer' + ' ' + ';\n'
			outfile.write(current)

		if(str(c[10]) != ""):
			total = '\tgco:hasTotalEmployeeEstimate' + ' ' + '\"' + c[10] + '\"' + '^^xsd:integer' + ' ' + '.\n'	
			outfile.write(total)

	rownum += 1
	count += 1 
	# if count % 5000000 == 0:
	# 	print("data ke-" + str(count))
	if count == 2:
		break

outfile.write('\n')

industry_set = set(industry_list)
for industry in industry_set:
	inclabel = industry.replace('_', ' ')
	inc = 'gco:' + industry + ' a '+ 'gco:Industry ;\n\trdfs:label \"' + inclabel + '\" .\n'
	outfile.write(inc)

outfile.write('\n')

for k, v in cityStateDict.items():
	city = k
	state = v
	country = stateCountryDict[state]
	citylabel = city.replace('_', ' ')

	cityEntity = 'gco:' + city + ' a '+ 'gco:City ;\n\tgco:state gco:' + state + ' ;\n\tgco:country gco:' + country +' ;\n\trdfs:label \"' + citylabel + '\" .\n'
	outfile.write(cityEntity)

outfile.write('\n')

country_list = []
for k, v in stateCountryDict.items():
	state = k
	country = v
	statelabel = state.replace('_', ' ')

	stateEntity = 'gco:' + state + ' a '+ 'gco:State ;\n\tgco:country gco:' + country +' ;\n\trdfs:label \"' + statelabel + '\" .\n'
	outfile.write(stateEntity)

	country_list.append(v)

outfile.write('\n')

country_set = set(country_list)
for country in country_set:
	countrylabel = country.replace('_', ' ')
	countryEntity = 'gco:' + country + ' a ' + 'gco:Country ;\n\trdfs:label \"' + countrylabel + '\" .\n'
	outfile.write(countryEntity)

# finish off by closing the two files we created
end_time = datetime.now()
consume_time = end_time - start_time
print("consume_time: " + str(consume_time))

outfile.close()
ifile.close()