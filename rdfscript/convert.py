#!/usr/bin/env python

#import the CSV module for dealing with CSV files
import csv
import io
import re
from urllib.parse import unquote

#create a 'reader' variable, which allows us to play with the contents of the CSV file
#in order to do that, we create the ifile variable, open the CSV file into that, then pass its' contents into the reader variable.
ifile = io.open('companies_sorted.csv', 'r', encoding='utf8')
reader = csv.reader(ifile)
prefix = 'https://globalcompany.org/ns#'

#create a new variable called 'outfile' (could be any name), which we'll use to create a new file that we'll pass our TTL into.
outfile = io.open('companies_sorted.nt', 'a', encoding='utf8')


def preprocess(data, isLiteralorURI):
	data = str(data)
	bad_char = ['<', '>', '|', '(', ')', '[', ']', ',', '"', '\\', '{', '}', '^', "'", ':', ';', "`", '+', '*', '=']
	data = str(data.encode('ascii', 'ignore').decode('utf-8'))
	data = ''.join(i for i in data if not i in bad_char)
	data = re.sub(u'[\u2018\u2019\u201a\u201b\u2039\u203a]','', data)
	if(isLiteralorURI == 1):
		data = data.replace('\t', ' ').replace('\n', ' ').lstrip()
	elif(isLiteralorURI == 0):
		data = data.lstrip().replace(' ', '_').replace('\n', '_').replace('\t', '_').replace('.', '').replace('/', '').replace('#', '')
	return data

#get python to loop through each row in the CSV, and ignore the first row.
# 

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

		labelid = preprocess(c[0], 1)
		labelid =  '<' + prefix + c[0] + '>' + ' ' + '<' +'http://www.w3.org/2000/01/rdf-schema#label' + '>' + ' ' + '\"' + labelid + '\"' + ' ' + '.\n'
		outfile.write(labelid)

		companytype =  '<' + prefix + c[0] + '>' + ' ' + '<' +'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' + '>' + ' ' + '<' + prefix + 'GlobalCompany' + '>' + ' ' + '.\n'
		outfile.write(companytype)

		companyname = preprocess(c[1], 0)
		name = '<' + prefix + c[0] + '>' + ' ' + '<' + prefix + 'hasName' + '>' + ' ' + '<' + prefix + companyname + '>' + ' ' + '.\n'
		outfile.write(name)

		labelname = preprocess(c[1], 1).replace('/', '')
		labelname =  '<' + prefix + companyname + '>' + ' ' + '<' +'http://www.w3.org/2000/01/rdf-schema#label' + '>' + ' ' + '\"' + labelname + '\"' + ' ' + '.\n'
		outfile.write(labelname)

		if(str(c[2]) != ""):
			website = preprocess(c[2], 1)
			domain = '<' + prefix + c[0] + '>' + ' ' + '<' + prefix + 'hasOfficialWebsite' + '>' + ' ' + '\"' + website + '\"' + ' ' + '.\n'
			outfile.write(domain)
		if(str(c[3]) != ""):
			year = '<' + prefix + c[0] + '>' + ' ' + '<' + prefix + 'yearFound' + '>' + ' ' + '\"' + c[3] + '\"' + ' ' + '.\n'
			outfile.write(year.replace('.0', ''))
		if(str(c[4]) != ""):
			inc = preprocess(c[4], 0)
			industry = '<' + prefix + c[0] + '>' + ' ' + '<' + prefix + 'isIndustry' + '>' + ' ' + '<' + prefix + inc + '>' + ' ' + '.\n'
			outfile.write(industry)

			industry_list.append(inc)

			# labelindustry = preprocess(c[4], 1)
			# labelindustry =  '<' + prefix + inc + '>' + ' ' + '<' +'http://www.w3.org/2000/01/rdf-schema#label' + '>' + ' ' + '\"' + labelindustry + '\"' + ' ' + '.\n'
			# outfile.write(labelindustry)

		if(str(c[5]) != ""):
			company_size = str(c[5]).replace('\t', ' ').replace('\n', ' ')
			size = '<' + prefix + c[0] + '>' + ' ' + '<' + prefix + 'hasSizeRange' + '>' + ' ' + '\"' + company_size + '\"' + ' ' + '.\n'
			outfile.write(size)
		if(str(c[6]) != ""):
			# local = preprocess(c[6], 0)
			# locality = '<' + prefix + c[0] + '>' + ' ' + '<' + prefix + 'locality' + '>' + ' ' + '<' + prefix + local + '>' + ' ' + '.\n'
			# outfile.write(locality)

			# labellocality = preprocess(c[6], 1)
			# labellocality =  '<' + prefix + local + '>' + ' ' + '<' +'http://www.w3.org/2000/01/rdf-schema#label' + '>' + ' ' + '\"' + labellocality + '\"' + ' ' + '.\n'
			# outfile.write(labellocality)
			locality = c[6].split(", ")
			city = preprocess(locality[0], 0)
			state = preprocess(locality[1], 0)
			country = preprocess(locality[2], 0)
			cityLocated = '<' + prefix + c[0] + '>' + ' ' + '<https://globalcompany.org/ns#locatedInCity>' + ' ' + '<' + 'https://globalcompany.org/ns#' + city + '>' + ' ' + '.\n'
			stateLocated = '<' + prefix + c[0] + '>' + ' ' +'<https://globalcompany.org/ns#locatedInState>' + ' ' + '<' + 'https://globalcompany.org/ns#' + state + '>' + ' ' + '.\n'
			countryLocated = '<' + prefix + c[0] + '>' + ' ' + '<https://globalcompany.org/ns#locatedInCountry>' + ' ' + '<' + 'https://globalcompany.org/ns#' + country + '>' + ' ' + '.\n'
			outfile.write(cityLocated)
			outfile.write(stateLocated)
			outfile.write(countryLocated)

			cityStateDict[city] = state
			stateCountryDict[state] = country

		# if(str(c[7]) != ""):
		# 	place = preprocess(c[7], 0)
		# 	country = '<' + prefix + c[0] + '>' + ' ' + '<' + prefix + 'locatedInCountry' + '>' + ' ' + '<' + prefix + place + '>' + ' ' + '.\n'
		# 	outfile.write(country)

		# 	labelcountry = preprocess(c[7], 1)
		# 	labelcountry =  '<' + prefix + place + '>' + ' ' + '<' +'http://www.w3.org/2000/01/rdf-schema#label' + '>' + ' ' + '\"' + labelcountry + '\"' + ' ' + '.\n'
		# 	outfile.write(labelcountry)

		if(str(c[8]) != ""):
			uri = preprocess(c[8], 1)
			linkedin = '<' + prefix + c[0] + '>' + ' ' + '<' + prefix + 'hasLinkedinURL' + '>' + ' ' + '\"' + uri + '\"' + ' ' + '.\n'
			outfile.write(linkedin)
		if(str(c[9]) != ""):
			current = '<' + prefix + c[0] + '>' + ' ' + '<' + prefix + 'hasCurrentEmployee' + '>' + ' ' + '\"' + c[9] + '\"' + '^^<http://www.w3.org/2001/XMLSchema#integer>' + ' ' + '.\n'
			outfile.write(current)
		if(str(c[10]) != ""):
			total = '<' + prefix + c[0] + '>' + ' ' + '<' + prefix + 'hasTotalEmployeeEstimate' + '>' + ' ' + '\"' + c[10] + '\"' + '^^<http://www.w3.org/2001/XMLSchema#integer>' + ' ' + '.\n'
			outfile.write(total)

	rownum += 1
	count += 1 
	# if(count == 1000000):
	# 	outfile.close()
	# 	countfile += 1
	# 	filename = 'companies_sorted' + str(countfile) + '.ntriples'
	# 	outfile = io.open(filename, 'a', encoding='utf8')
	# 	count = 0
	# advance the row number so we can loop through again with the next row
	# print("data : " + str(rownum))
	if count == 200000:
		break


industry_set = set(industry_list)
for industry in industry_set:
	inclabel = industry.replace('_', ' ')
	# inc = prefix + industry + ' a '+ 'https://globalcompany.org/ns#Industry ;\n\trdfs:label \"' + inclabel + '\" .\n'
	inc = '<' + prefix + industry + '>' + ' ' + '<' +'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' + '>' + ' ' + '<' + prefix + 'Industry' + '>' + ' ' + '.\n'
	inc += '<' + prefix + industry + '>' + ' ' + '<' +'http://www.w3.org/2000/01/rdf-schema#label' + '>' + ' ' + '\"' + inclabel + '\"' + ' ' + '.\n'
	outfile.write(inc)

# outfile.write('\n')

for k, v in cityStateDict.items():
	city = k
	state = v
	country = stateCountryDict[state]
	citylabel = city.replace('_', ' ')

	# cityEntity = 'gco:' + city + ' a '+ 'gco:City ;\n\tgco:state gco:' + state + ' ;\n\tgco:country gco:' + country +' ;\n\trdfs:label \"' + citylabel + '\" .\n'
	cityEntity = '<' + prefix + city + '>' + ' ' + '<' +'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' + '>' + ' ' + '<' + prefix + 'City' + '>' + ' ' + '.\n'
	cityEntity += '<' + prefix + city + '>' + ' ' + '<' + prefix + 'state' + '>' + ' ' + '<' + prefix + state + '>' + ' ' + '.\n'
	cityEntity += '<' + prefix + city + '>' + ' ' + '<' + prefix + 'country' + '>' + ' ' + '<' + prefix + country + '>' + ' ' + '.\n'
	cityEntity += '<' + prefix + city + '>' + ' ' + '<' +'http://www.w3.org/2000/01/rdf-schema#label' + '>' + ' ' + '\"' + citylabel + '\"' + ' ' + '.\n'
	outfile.write(cityEntity)

# outfile.write('\n')

country_list = []
for k, v in stateCountryDict.items():
	state = k
	country = v
	statelabel = state.replace('_', ' ')

	# stateEntity = 'gco:' + state + ' a '+ 'gco:State ;\n\tgco:country gco:' + country +' ;\n\trdfs:label \"' + statelabel + '\" .\n'
	stateEntity = '<' + prefix + state + '>' + ' ' + '<' +'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' + '>' + ' ' + '<' + prefix + 'State' + '>' + ' ' + '.\n'
	stateEntity += '<' + prefix + state + '>' + ' ' + '<' + prefix + 'country' + '>' + ' ' + '<' + prefix + country + '>' + ' ' + '.\n'
	stateEntity += '<' + prefix + state + '>' + ' ' + '<' +'http://www.w3.org/2000/01/rdf-schema#label' + '>' + ' ' + '\"' + statelabel + '\"' + ' ' + '.\n'
	outfile.write(stateEntity)

	country_list.append(v)

# outfile.write('\n')

country_set = set(country_list)
for country in country_set:
	countrylabel = country.replace('_', ' ')
	# countryEntity = 'gco:' + country + ' a ' + 'gco:Country ;\n\trdfs:label \"' + countrylabel + '\" .\n'
	countryEntity = '<' + prefix + country + '>' + ' ' + '<' +'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' + '>' + ' ' + '<' + prefix + 'Country' + '>' + ' ' + '.\n'
	countryEntity += '<' + prefix + country + '>' + ' ' + '<' +'http://www.w3.org/2000/01/rdf-schema#label' + '>' + ' ' + '\"' + countrylabel + '\"' + ' ' + '.\n'
	outfile.write(countryEntity)
# finish off by closing the two files we created

outfile.close()
ifile.close()