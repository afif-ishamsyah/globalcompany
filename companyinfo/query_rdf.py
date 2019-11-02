import rdflib
from rdflib.store import NO_STORE, VALID_STORE
from rdflib import plugin, ConjunctiveGraph
from rdflib.store import Store
import sys
from SPARQLWrapper import SPARQLWrapper, JSON

# g = ConjunctiveGraph('Sleepycat')
g = ConjunctiveGraph()


def getCompanyDataOnline(param):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT (lcase(str(?s)) as ?name) (str(?p) as ?pred)  (str(?o) as ?obj)
    WHERE { ?s a dbo:Company .
            ?s ?p ?o .
            FILTER ( lcase(str(?s)) = 'http://dbpedia.org/resource/""" + str(param) + """' )} """)
            
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

def getCompanyData(param):
    # g.open('companyinfo/company', create=False)
    g.parse('companyinfo/companies_sorted_1000.ntriples', format='nt')

    company_id = '<http://globalcompany.org/' + param + '>'

    stringquery = """SELECT (str(?name_label) as ?str_name_label) 
                            (str(?country_label) as ?str_country_label)
                            (str(?industry_label) as ?str_industry_label)
                            (str(?year) as ?str_year)
                            (str(?size) as ?str_size)
                            (str(?locality_label) as ?str_locality_label)
                            (str(?current) as ?str_current)
                            (str(?total) as ?str_total)
                            ?linkedinurl
                            ?domainurl
                    WHERE { ?sub <http://globalcompany.org/hasName> ?name .
                            ?sub <http://globalcompany.org/hasOfficialWebsite> ?domain .
                            ?sub <http://globalcompany.org/isIndustry> ?industry .
                            ?sub <http://globalcompany.org/size_range> ?size .
                            ?sub <http://globalcompany.org/locality> ?locality .
                            ?sub <http://globalcompany.org/locatedInCountry> ?country .
                            ?sub <http://globalcompany.org/hasLinkedinURL> ?linkedin .
                            ?sub <http://globalcompany.org/current_employee> ?current .
                            ?sub <http://globalcompany.org/total_employee_estimate> ?total .
                            ?name <rdfs:label> ?name_label .
                            ?country <rdfs:label> ?country_label .
                            ?industry <rdfs:label> ?industry_label .
                            ?locality <rdfs:label> ?locality_label .
                            BIND(CONCAT("https://", STR( ?linkedin )) AS ?linkedinurl)
                            BIND(CONCAT("https://", STR( ?domain )) AS ?domainurl)
                            OPTIONAL { ?sub <http://globalcompany.org/yearFound> ?year .  }
                    FILTER ( ?sub = """ + company_id + """ )} """

    qres = g.query(stringquery)
    val = qres
    g.close()
    return val

def getAllCompany():
    # g.open('companyinfo/company', create=False)
    g.parse('companyinfo/companies_sorted_1000.ntriples', format='nt')

    stringquery = """SELECT (str(?sub_label) as ?id) (str(?name_label) as ?str_name_label) (str(?country_label) as ?str_country_label) ?linkedinurl
                    WHERE { ?sub <http://globalcompany.org/hasName> ?name .
                            ?sub <http://globalcompany.org/locatedInCountry> ?country .
                            ?sub <http://globalcompany.org/hasLinkedinURL> ?linkedin .
                            ?sub <rdfs:label> ?sub_label .
                            ?name <rdfs:label> ?name_label .
                            ?country <rdfs:label> ?country_label .
                            BIND(CONCAT("https://", STR( ?linkedin )) AS ?linkedinurl)
                            } ORDER BY ASC(?str_name_label)"""

    qres = g.query(stringquery)
    val = qres
    g.close()
    return val

def getSomeCompany(param):
    # g.open('companyinfo/company', create=False)
    g.parse('companyinfo/companies_sorted_1000.ntriples', format='nt')

    stringquery = """SELECT (str(?sub_label) as ?id) (str(?name_label) as ?str_name_label) (str(?country_label) as ?str_country_label) ?linkedinurl
                    WHERE { ?sub <http://globalcompany.org/hasName> ?name .
                            ?sub <http://globalcompany.org/locatedInCountry> ?country .
                            ?sub <http://globalcompany.org/hasLinkedinURL> ?linkedin .
                            ?sub <rdfs:label> ?sub_label .
                            ?name <rdfs:label> ?name_label .
                            ?country <rdfs:label> ?country_label .
                            FILTER regex(str(?name_label), '""" + str(param) + """', 'i')
                            BIND(CONCAT("https://", STR( ?linkedin )) AS ?linkedinurl)
                            } ORDER BY ASC(?str_name_label)"""

    qres = g.query(stringquery)
    val = qres
    g.close()
    return val