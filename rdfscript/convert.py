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
outfile = io.open('companies_sorted0.ntriples', 'a', encoding='utf8')


def preprocess(data, isLiteralorURI):
	data = str(data)
	bad_char = ['<', '>', '|', '(', ')', '[', ']', ',', '"', '\\', '\t', '{', '}', '^', "'", ':', ';', "`", '+', '*', '=']
	data = str(data.encode('ascii', 'ignore').decode('utf-8'))
	data = ''.join(i for i in data if not i in bad_char)
	data = re.sub(u'[\u2018\u2019\u201a\u201b\u2039\u203a]','', data)
	if(isLiteralorURI == 1):
		data = data.replace('\t', ' ').replace('\n', ' ')
	elif(isLiteralorURI == 0):
		data = data.replace(' ', '_').replace('\n', '_').replace('.', '').replace('/', '')
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
		labelid =  '<' + prefix + c[0] + '>' + '\t' + '<' +'rdfs:label' + '>' + '\t' + '\"' + labelid + '\"' + '\t' + '.\n'
		outfile.write(labelid) 

		companyname = preprocess(c[1], 0)
		name = '<' + prefix + c[0] + '>' + '\t' + '<' + prefix + 'hasName' + '>' + '\t' + '<' + prefix + companyname + '>' + '\t' + '.\n'
		outfile.write(name)

		labelname = preprocess(c[1], 1)
		labelname =  '<' + prefix + companyname + '>' + '\t' + '<' +'rdfs:label' + '>' + '\t' + '\"' + labelname + '\"' + '\t' + '.\n'
		outfile.write(labelname)

		if(str(c[2]) != ""):
			website = preprocess(c[2], 1)
			domain = '<' + prefix + c[0] + '>' + '\t' + '<' + prefix + 'hasOfficialWebsite' + '>' + '\t' + '\"' + website + '\"' + '\t' + '.\n'
			outfile.write(domain)
		if(str(c[3]) != ""):
			year = '<' + prefix + c[0] + '>' + '\t' + '<' + prefix + 'yearFound' + '>' + '\t' + '\"' + c[3] + '\"' + '\t' + '.\n'
			outfile.write(year.replace('.0', ''))
		if(str(c[4]) != ""):
			inc = preprocess(c[4], 0)
			industry = '<' + prefix + c[0] + '>' + '\t' + '<' + prefix + 'isIndustry' + '>' + '\t' + '<' + prefix + inc + '>' + '\t' + '.\n'
			outfile.write(industry)

			labelindustry = preprocess(c[4], 1)
			labelindustry =  '<' + prefix + inc + '>' + '\t' + '<' +'rdfs:label' + '>' + '\t' + '\"' + labelindustry + '\"' + '\t' + '.\n'
			outfile.write(labelindustry)

		if(str(c[5]) != ""):
			company_size = str(c[5]).replace('\t', ' ').replace('\n', ' ')
			size = '<' + prefix + c[0] + '>' + '\t' + '<' + prefix + 'size_range' + '>' + '\t' + '\"' + company_size + '\"' + '\t' + '.\n'
			outfile.write(size)
		if(str(c[6]) != ""):
			local = preprocess(c[6], 0)
			locality = '<' + prefix + c[0] + '>' + '\t' + '<' + prefix + 'locality' + '>' + '\t' + '<' + prefix + local + '>' + '\t' + '.\n'
			outfile.write(locality)

			labellocality = preprocess(c[6], 1)
			labellocality =  '<' + prefix + local + '>' + '\t' + '<' +'rdfs:label' + '>' + '\t' + '\"' + labellocality + '\"' + '\t' + '.\n'
			outfile.write(labellocality)

		if(str(c[7]) != ""):
			place = preprocess(c[7], 0)
			country = '<' + prefix + c[0] + '>' + '\t' + '<' + prefix + 'locatedInCountry' + '>' + '\t' + '<' + prefix + place + '>' + '\t' + '.\n'
			outfile.write(country)

			labelcountry = preprocess(c[7], 1)
			labelcountry =  '<' + prefix + place + '>' + '\t' + '<' +'rdfs:label' + '>' + '\t' + '\"' + labelcountry + '\"' + '\t' + '.\n'
			outfile.write(labelcountry)

		if(str(c[8]) != ""):
			uri = preprocess(c[8], 1)
			linkedin = '<' + prefix + c[0] + '>' + '\t' + '<' + prefix + 'hasLinkedinURL' + '>' + '\t' + '\"' + uri + '\"' + '\t' + '.\n'
			outfile.write(linkedin)
		if(str(c[9]) != ""):
			current = '<' + prefix + c[0] + '>' + '\t' + '<' + prefix + 'current_employee' + '>' + '\t' + '\"' + c[9] + '\"' + '^^<http://www.w3.org/2001/XMLSchema#integer>' + '\t' + '.\n'
			outfile.write(current)
		if(str(c[10]) != ""):
			total = '<' + prefix + c[0] + '>' + '\t' + '<' + prefix + 'total_employee_estimate' + '>' + '\t' + '\"' + c[10] + '\"' + '^^<http://www.w3.org/2001/XMLSchema#integer>' + '\t' + '.\n'
			outfile.write(total)

	rownum += 1
	count += 1 
	if(count == 1000000):
		outfile.close()
		countfile += 1
		filename = 'companies_sorted' + str(countfile) + '.ntriples'
		outfile = io.open(filename, 'a', encoding='utf8')
		count = 0
	# advance the row number so we can loop through again with the next row
	# print("data : " + str(rownum))
	# if rownum == 1000:
	# 	break

# finish off by closing the two files we created

outfile.close()
ifile.close()