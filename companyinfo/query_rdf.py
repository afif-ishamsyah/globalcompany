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
           (str(?result_netincome) as ?str_netincome)
           (str(?result_operatingincome) as ?str_operatingincome)
           (str(?result_revenue) as ?str_revenue)
           (str(?result_areaserved) as ?str_areaserved)
           (str(?result_thumbnail) as ?str_thumbnail)
           (group_concat(distinct ?result_keyperson;separator=", ") as ?result_keypersons)
           (group_concat(distinct ?result_product;separator=", ") as ?result_products)
           (group_concat(distinct ?result_service;separator=", ") as ?result_services)
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
            OPTIONAL {?s <http://dbpedia.org/ontology/netIncome> ?netincome .}
            OPTIONAL {?s <http://dbpedia.org/ontology/operatingIncome> ?operatingincome .}
            OPTIONAL {?s <http://dbpedia.org/ontology/revenue> ?revenue .}
            OPTIONAL {?s <http://dbpedia.org/property/areaServed> ?areaserved .}
            OPTIONAL {?s <http://dbpedia.org/ontology/keyPerson> ?keyperson .}
            OPTIONAL {?s <http://dbpedia.org/ontology/product> ?product .}
            OPTIONAL {?s <http://dbpedia.org/ontology/service> ?service .}
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
            BIND(COALESCE(?netincome, ?default_number) as ?result_netincome)
            BIND(COALESCE(?operatingincome, ?default_number) as ?result_operatingincome)
            BIND(COALESCE(?revenue, ?default_number) as ?result_revenue)
            BIND(COALESCE(?areaserved, ?default_string) as ?result_areaserved)
            BIND(COALESCE(?keyperson, ?default_string) as ?result_keyperson)
            BIND(COALESCE(?product, ?default_string) as ?result_product)
            BIND(COALESCE(?service, ?default_string) as ?result_service)
            BIND(COALESCE(?thumb, ?default_string) as ?result_thumbnail)
            FILTER (lang(?abstract) = 'en')
            FILTER ( lcase(str(?s)) = 'http://dbpedia.org/resource/""" + name + """' || lcase(?homepage_clean) = '""" + web + """')} GROUP BY ?s 
                                                                                                                                              ?result_thumbnail
                                                                                                                                              ?result_areaserved
                                                                                                                                              ?result_revenue
                                                                                                                                              ?result_operatingincome
                                                                                                                                              ?result_netincome
                                                                                                                                              ?result_equity
                                                                                                                                              ?result_assets
                                                                                                                                              ?result_abstract
                                                                                                                                              ?result_longitude
                                                                                                                                              ?result_latitude
                                                                                                                                              ?result_wikipageid
                                                                                                                                              ?result_topic
                                                                                                                                              LIMIT 1""")

            
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

def getCompanyData(param):
    company_id = '<https://globalcompany.org/ns#' + param + '>'

    sparql = SPARQLWrapper("http://localhost:3030/company/sparql")
    sparql.setQuery("""
    PREFIX gco: <https://globalcompany.org/ns#>
    PREFIX gcor: <https://globalcompany.org/resource/>
    PREFIX dct: <http://purl.org/dc/terms/>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    SELECT  (str(?name_label) as ?str_name_label)
            (str(?result_city) as ?str_city_label) (str(?result_state) as ?str_state_label)
            (str(?result_country) as ?str_country_label) (str(?result_industry) as ?str_industry_label)
            (str(?result_year) as ?str_year) (str(?result_size) as ?str_size)
            (str(?result_current) as ?str_current) (str(?result_total) as ?str_total)
            (str(?result_linkedin) as ?linkedinurl) (str(?result_domain) as ?domainurl)
    WHERE { BIND('-' as ?default_string)
            """ + company_id + """ gco:hasName ?name .
            OPTIONAL {""" + company_id + """ gco:hasOfficialWebsite ?domain .}
            OPTIONAL {""" + company_id + """ gco:isIndustry ?industry .}
            OPTIONAL {""" + company_id + """ gco:hasSizeRange ?size .}
            OPTIONAL {""" + company_id + """ gco:locatedInCity ?city .}
            OPTIONAL {""" + company_id + """ gco:locatedInState ?state .}
            OPTIONAL { """ + company_id + """ gco:locatedInCountry ?country .}
            OPTIONAL {""" + company_id + """ gco:hasLinkedinURL ?linkedin .}
            OPTIONAL {""" + company_id + """ gco:hasCurrentEmployee ?current .}
            OPTIONAL {""" + company_id + """ gco:hasTotalEmployeeEstimate ?total .}
            OPTIONAL {""" + company_id + """ gco:yearFound ?year .  }
            ?name rdfs:label ?name_label .
            OPTIONAL {?city rdfs:label ?city_label .}
            OPTIONAL {?state rdfs:label ?state_label .}
            OPTIONAL {?country rdfs:label ?country_label .}
            OPTIONAL {?industry rdfs:label ?industry_label .}
            BIND(COALESCE(?domain, ?default_string) as ?result_domain)
            BIND(COALESCE(?industry_label, ?default_string) as ?result_industry)
            BIND(COALESCE(?size, ?default_string) as ?result_size)
            BIND(COALESCE(?city_label, ?default_string) as ?result_city)
            BIND(COALESCE(?state_label, ?default_string) as ?result_state)
            BIND(COALESCE(?country_label, ?default_string) as ?result_country)
            BIND(COALESCE(?linkedin, ?default_string) as ?result_linkedin)
            BIND(COALESCE(?current, ?default_string) as ?result_current)
            BIND(COALESCE(?total, ?default_string) as ?result_total)
            BIND(COALESCE(?year, ?default_string) as ?result_year)}
            LIMIT 1""")

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results


def getSomeCompany(param):
    sparql = SPARQLWrapper("http://localhost:3030/company/sparql")
    sparql.setQuery("""
    PREFIX gco: <https://globalcompany.org/ns#>
    PREFIX gcor: <https://globalcompany.org/resource/>
    PREFIX dct: <http://purl.org/dc/terms/>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    SELECT DISTINCT (str(?id_label) as ?id) 
                    (str(?name_label) as ?str_name_label) 
                    (str(?country_label) as ?str_country_label) 
                    ?linkedinurl 
                    (str(?result_domain) as ?domainurl)
                    WHERE { BIND('-' as ?default_string)
                            ?s gco:hasName ?name .
                            ?s a gco:GlobalCompany .
                            ?s gco:locatedInCountry ?country .
                            ?s gco:hasLinkedinURL ?linkedin .
                            ?s rdfs:label ?id_label .
                            ?name rdfs:label ?name_label .
                            ?country rdfs:label ?country_label .
                            OPTIONAL {?s gco:hasOfficialWebsite ?domain .}
                            FILTER regex(str(?name_label), '""" + str(param) + """', 'i')
                            BIND(CONCAT("https://", STR( ?linkedin )) AS ?linkedinurl)  
                            BIND(COALESCE(?domain, ?default_string) as ?result_domain)
                            } ORDER BY ASC(?str_name_label)""")

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results