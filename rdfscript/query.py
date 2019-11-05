import rdflib
from rdflib.store import NO_STORE, VALID_STORE
from rdflib import plugin, ConjunctiveGraph
from rdflib.store import Store
from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery("""
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX foaf: <http://xmlns.com/foaf/0.1/>

                SELECT (str(?thumb) as ?img) WHERE { <http://dbpedia.org/resource/Amazon.com> <http://dbpedia.org/ontology/thumbnail> ?thumb . }""")

sparql.setReturnFormat(JSON)
results = sparql.query().convert()
for result in results["results"]["bindings"]:
    print(result["img"]["value"])

# g = ConjunctiveGraph('Sleepycat')
# g.open('./company', create=False)
# 

# g = ConjunctiveGraph()
# g.parse("companies_sorted_1000.ntriples", format="nt")

# stringquery = """SELECT ?sub ?obj 
#                 WHERE { ?sub <http://globalcompany.org/hasName> ?obj . 
#                 FILTER (regex(str(?obj), "hewlett"))  }
#                 """

# stringquery = """SELECT ?sub ?obj 
#                 WHERE { ?sub <http://globalcompany.org/hasName> ?obj .  }
#                 """

# qres = g.query(stringquery)

# print(len(g))
# for row in qres:
#     print(str(row.sub) + '\t' + str(row.obj))

# g.close()