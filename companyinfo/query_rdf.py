import sys
from SPARQLWrapper import SPARQLWrapper, JSON

def getCompanyDataOnline(name, web):
    name  = str(name).replace(' ','_')
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    SELECT
           (str(?result_topic) as ?str_topic)
           (str(?result_wikipageid) as ?str_wikipageid)
           (str(?result_latitude) as ?str_latitude)
           (str(?result_longitude) as ?str_longitude)
           (str(?result_abstract) as ?str_abstract)
           (str(?result_assets) as ?str_assets)
           (str(?result_equity) as ?str_equity)
           (str(?result_location) as ?str_location)
           (str(?result_netincome) as ?str_netincome)
           (str(?result_operatingincome) as ?str_operatingincome)
           (str(?result_revenue) as ?str_revenue)
           (str(?result_areaserved) as ?str_areaserved)
           (str(?result_thumbnail) as ?str_thumbnail)
    WHERE { ?s a dbo:Company .
            BIND('-' as ?default_string)
            BIND( 0 as ?default_number)
            OPTIONAL {?s <http://xmlns.com/foaf/0.1/isPrimaryTopicOf> ?topic .}
            OPTIONAL {?s <http://dbpedia.org/ontology/wikiPageID> ?wikipageid .}
            OPTIONAL {?s <http://www.w3.org/2003/01/geo/wgs84_pos#lat> ?latitude .}
            OPTIONAL {?s <http://www.w3.org/2003/01/geo/wgs84_pos#long> ?longitude .}
            OPTIONAL {?s <http://dbpedia.org/ontology/abstract> ?abstract .}
            OPTIONAL {?s <http://dbpedia.org/ontology/assets> ?assets .}
            OPTIONAL {?s <http://dbpedia.org/ontology/equity> ?equity .}
            OPTIONAL {?s <http://dbpedia.org/ontology/location> ?location .}
            OPTIONAL {?s <http://dbpedia.org/ontology/netIncome> ?netincome .}
            OPTIONAL {?s <http://dbpedia.org/ontology/operatingIncome> ?operatingincome .}
            OPTIONAL {?s <http://dbpedia.org/ontology/revenue> ?revenue .}
            OPTIONAL {?s <http://dbpedia.org/property/areaServed> ?areaserved .}
            OPTIONAL {?s foaf:homepage ?website .}
            OPTIONAL {?s <http://dbpedia.org/ontology/thumbnail> ?thumb .}
            BIND(REPLACE(STR(?website), "https://www.", "", "i") AS ?homepage1)
            BIND(REPLACE(STR(?homepage1), "http://www.", "", "i") AS ?homepage2)
            BIND(REPLACE(STR(?homepage2), "https://", "", "i") AS ?homepage3)
            BIND(REPLACE(STR(?homepage3), "http://", "", "i") AS ?homepage_clean)
            BIND(COALESCE(?topic, ?default_string) as ?result_topic)
            BIND(COALESCE(?wikipageid, ?default_string) as ?result_wikipageid)
            BIND(COALESCE(?latitude, ?default_string) as ?result_latitude)
            BIND(COALESCE(?longitude, ?default_string) as ?result_longitude)
            BIND(COALESCE(?abstract, ?default_string) as ?result_abstract)
            BIND(COALESCE(?assets, ?default_number) as ?result_assets)
            BIND(COALESCE(?equity, ?default_number) as ?result_equity)
            BIND(COALESCE(?location, ?default_string) as ?result_location)
            BIND(COALESCE(?netincome, ?default_number) as ?result_netincome)
            BIND(COALESCE(?operatingincome, ?default_number) as ?result_operatingincome)
            BIND(COALESCE(?revenue, ?default_number) as ?result_revenue)
            BIND(COALESCE(?areaserved, ?default_string) as ?result_areaserved)
            BIND(COALESCE(?thumb, ?default_string) as ?result_thumbnail)
            FILTER (lang(?abstract) = 'en')
            FILTER ( lcase(str(?s)) = 'http://dbpedia.org/resource/""" + name + """' || lcase(?homepage_clean) = '""" + web + """')} LIMIT 1""")

            
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

def getThumbnail(name, web):
    name  = str(name).replace(' ','_')
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    SELECT 
           (str(?result_thumbnail) as ?str_thumbnail)
    WHERE { ?s a dbo:Company .
            BIND('-' as ?default_string)
            ?s <http://dbpedia.org/ontology/thumbnail> ?thumb .
            OPTIONAL {?s foaf:homepage ?website .}
            BIND(REPLACE(STR(?website), "https://www.", "", "i") AS ?homepage1)
            BIND(REPLACE(STR(?homepage1), "http://www.", "", "i") AS ?homepage2)
            BIND(REPLACE(STR(?homepage2), "https://", "", "i") AS ?homepage3)
            BIND(REPLACE(STR(?homepage3), "http://", "", "i") AS ?homepage_clean)
            BIND(COALESCE(?thumb, ?default_string) as ?result_thumbnail)
            FILTER ( lcase(str(?s)) = 'http://dbpedia.org/resource/""" + name + """' || lcase(?homepage_clean) = '""" + web + """')} LIMIT 1""")

            
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

def getCompanyData(param):
    company_id = '<http://globalcompany.org/' + param + '>'

    sparql = SPARQLWrapper("http://localhost:3030/company/sparql")
    sparql.setQuery("""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    SELECT (str(?name_label) as ?str_name_label) 
                            (str(?result_country) as ?str_country_label)
                            (str(?result_industry) as ?str_industry_label)
                            (str(?result_year) as ?str_year)
                            (str(?result_size) as ?str_size)
                            (str(?result_locality) as ?str_locality_label)
                            (str(?result_current) as ?str_current)
                            (str(?result_total) as ?str_total)
                            (str(?result_linkedin) as ?linkedinurl)
                            (str(?result_domain) as ?domainurl)
                    WHERE { BIND('-' as ?default_string)
                            """ + company_id + """ <http://globalcompany.org/hasName> ?name .
                            OPTIONAL {""" + company_id + """ <http://globalcompany.org/hasOfficialWebsite> ?domain .}
                            """ + company_id + """ <http://globalcompany.org/isIndustry> ?industry .
                            OPTIONAL {""" + company_id + """ <http://globalcompany.org/size_range> ?size .}
                            """ + company_id + """ <http://globalcompany.org/locality> ?locality .
                            """ + company_id + """ <http://globalcompany.org/locatedInCountry> ?country .
                            OPTIONAL {""" + company_id + """ <http://globalcompany.org/hasLinkedinURL> ?linkedin .}
                            OPTIONAL {""" + company_id + """ <http://globalcompany.org/current_employee> ?current .}
                            OPTIONAL {""" + company_id + """ <http://globalcompany.org/total_employee_estimate> ?total .}
                            OPTIONAL {""" + company_id + """ <http://globalcompany.org/yearFound> ?year .  }
                            ?name rdfs:label ?name_label .
                            OPTIONAL {?country rdfs:label ?country_label .}
                            OPTIONAL {?industry rdfs:label ?industry_label .}
                            OPTIONAL {?locality rdfs:label ?locality_label .}
                            BIND(COALESCE(?domain, ?default_string) as ?result_domain)
                            BIND(COALESCE(?industry_label, ?default_string) as ?result_industry)
                            BIND(COALESCE(?size, ?default_string) as ?result_size)
                            BIND(COALESCE(?locality_label, ?default_string) as ?result_locality)
                            BIND(COALESCE(?country_label, ?default_string) as ?result_country)
                            BIND(COALESCE(?linkedin, ?default_string) as ?result_linkedin)
                            BIND(COALESCE(?current, ?default_string) as ?result_current)
                            BIND(COALESCE(?total, ?default_string) as ?result_total)
                            BIND(COALESCE(?year, ?default_string) as ?result_year)}
                            LIMIT 1""")

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

def getAllCompany():
    sparql = SPARQLWrapper("http://localhost:3030/company/sparql")
    sparql.setQuery("""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    SELECT (str(?sub_label) as ?id) (str(?name_label) as ?str_name_label) (str(?country_label) as ?str_country_label) ?linkedinurl 
                    WHERE { ?sub <http://globalcompany.org/hasName> ?name .
                            ?sub <http://globalcompany.org/locatedInCountry> ?country .
                            ?sub <http://globalcompany.org/hasLinkedinURL> ?linkedin .
                            ?sub rdfs:label ?sub_label .
                            ?name rdfs:label ?name_label .
                            ?country rdfs:label ?country_label .
                            BIND(CONCAT("https://", STR( ?linkedin )) AS ?linkedinurl)
                            } ORDER BY ASC(?str_name_label)""")

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

def getSomeCompany(param):
    sparql = SPARQLWrapper("http://localhost:3030/company/sparql")
    sparql.setQuery("""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    SELECT (str(?sub_label) as ?id) (str(?name_label) as ?str_name_label) (str(?country_label) as ?str_country_label) ?linkedinurl (str(?result_domain) as ?domainurl)
                    WHERE { BIND('-' as ?default_string)
                            ?sub <http://globalcompany.org/hasName> ?name .
                            ?sub <http://globalcompany.org/locatedInCountry> ?country .
                            ?sub <http://globalcompany.org/hasLinkedinURL> ?linkedin .
                            ?sub rdfs:label ?sub_label .
                            ?name rdfs:label ?name_label .
                            ?country rdfs:label ?country_label .
                            OPTIONAL {?sub <http://globalcompany.org/hasOfficialWebsite> ?domain .}
                            FILTER regex(str(?name_label), '""" + str(param) + """', 'i')
                            BIND(CONCAT("https://", STR( ?linkedin )) AS ?linkedinurl)  
                            BIND(COALESCE(?domain, ?default_string) as ?result_domain)
                            } ORDER BY ASC(?str_name_label)""")

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results