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
prefix = 'http://globalcompany.org/'

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
		data = data.lstrip().replace(' ', '_').replace('\n', '_').replace('\t', '_').replace('.', '').replace('/', '')
	return data

#get python to loop through each row in the CSV, and ignore the first row.
# 
count = 0
countfile = 0
rownum = 0
for row in reader:
	if rownum == 0: # if it's the first row, then ignore it, move on to the next one.
		pass
	else: # if it's not the first row, place the contents of the row into the 'c' variable, then create a 'd' variable with the stuff we want in the file.
		c = row

		labelid = preprocess(c[0], 1)
		labelid =  '<' + prefix + c[0] + '>' + ' ' + '<' +'http://www.w3.org/2000/01/rdf-schema#label' + '>' + ' ' + '\"' + labelid + '\"' + ' ' + '.\n'
		outfile.write(labelid) 

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

			labelindustry = preprocess(c[4], 1)
			labelindustry =  '<' + prefix + inc + '>' + ' ' + '<' +'http://www.w3.org/2000/01/rdf-schema#label' + '>' + ' ' + '\"' + labelindustry + '\"' + ' ' + '.\n'
			outfile.write(labelindustry)

		if(str(c[5]) != ""):
			company_size = str(c[5]).replace('\t', ' ').replace('\n', ' ')
			size = '<' + prefix + c[0] + '>' + ' ' + '<' + prefix + 'size_range' + '>' + ' ' + '\"' + company_size + '\"' + ' ' + '.\n'
			outfile.write(size)
		if(str(c[6]) != ""):
			local = preprocess(c[6], 0)
			locality = '<' + prefix + c[0] + '>' + ' ' + '<' + prefix + 'locality' + '>' + ' ' + '<' + prefix + local + '>' + ' ' + '.\n'
			outfile.write(locality)

			labellocality = preprocess(c[6], 1)
			labellocality =  '<' + prefix + local + '>' + ' ' + '<' +'http://www.w3.org/2000/01/rdf-schema#label' + '>' + ' ' + '\"' + labellocality + '\"' + ' ' + '.\n'
			outfile.write(labellocality)

		if(str(c[7]) != ""):
			place = preprocess(c[7], 0)
			country = '<' + prefix + c[0] + '>' + ' ' + '<' + prefix + 'locatedInCountry' + '>' + ' ' + '<' + prefix + place + '>' + ' ' + '.\n'
			outfile.write(country)

			labelcountry = preprocess(c[7], 1)
			labelcountry =  '<' + prefix + place + '>' + ' ' + '<' +'http://www.w3.org/2000/01/rdf-schema#label' + '>' + ' ' + '\"' + labelcountry + '\"' + ' ' + '.\n'
			outfile.write(labelcountry)

		if(str(c[8]) != ""):
			uri = preprocess(c[8], 1)
			linkedin = '<' + prefix + c[0] + '>' + ' ' + '<' + prefix + 'hasLinkedinURL' + '>' + ' ' + '\"' + uri + '\"' + ' ' + '.\n'
			outfile.write(linkedin)
		if(str(c[9]) != ""):
			current = '<' + prefix + c[0] + '>' + ' ' + '<' + prefix + 'current_employee' + '>' + ' ' + '\"' + c[9] + '\"' + '^^<http://www.w3.org/2001/XMLSchema#integer>' + ' ' + '.\n'
			outfile.write(current)
		if(str(c[10]) != ""):
			total = '<' + prefix + c[0] + '>' + ' ' + '<' + prefix + 'total_employee_estimate' + '>' + ' ' + '\"' + c[10] + '\"' + '^^<http://www.w3.org/2001/XMLSchema#integer>' + ' ' + '.\n'
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
	if count == 50000:
		break

# finish off by closing the two files we created

outfile.close()
ifile.close()