import rdflib
from rdflib.store import NO_STORE, VALID_STORE
from rdflib import plugin, ConjunctiveGraph, Graph
from rdflib.store import Store


g = ConjunctiveGraph('Sleepycat')
rt = g.open('company', create=False)

if rt == NO_STORE:
    
    rt = g.open('company', create=True)

g.parse("companies_sorted.ntriples", format="nt")

print ('Triples in graph after add: ', len(g))

g.close()