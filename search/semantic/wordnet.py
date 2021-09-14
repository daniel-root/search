from rdflib import Graph
from rdflib.plugins.sparql import prepareQuery
from rdflib.namespace import RDFS, RDF, OWL, XSD
from rdflib import URIRef, Namespace


SCHEMA = Namespace("http://www.w3.org/2006/03/wn/wn20/schema/")
INSTANCES = Namespace("http://www.w3.org/2006/03/wn/wn20/instances/")

wordnet = Graph()
'''
wordnet.load("semantic/wordnet/wnfull.rdfs")
wordnet.load("semantic/wordnet/wordnet-antonym.rdf")
wordnet.load("semantic/wordnet/wordnet-attribute.rdf")
wordnet.load("semantic/wordnet/wordnet-causes.rdf")
wordnet.load("semantic/wordnet/wordnet-classifiedby.rdf")
wordnet.load("semantic/wordnet/wordnet-derivationallyrelated.rdf")
wordnet.load("semantic/wordnet/wordnet-entailment.rdf")
wordnet.load("semantic/wordnet/wordnet-frame.rdf")
wordnet.load("semantic/wordnet/wordnet-glossary.rdf")
wordnet.load("semantic/wordnet/wordnet-membermeronym.rdf")
wordnet.load("semantic/wordnet/wordnet-participleof.rdf")
wordnet.load("semantic/wordnet/wordnet-partmeronym.rdf")
wordnet.load("semantic/wordnet/wordnet-pertainsto.rdf")
wordnet.load("semantic/wordnet/wordnet-sameverbgroupas.rdf")
wordnet.load("semantic/wordnet/wordnet-seealso.rdf")
wordnet.load("semantic/wordnet/wordnet-similarity.rdf")
wordnet.load("semantic/wordnet/wordnet-substancemeronym.rdf")
wordnet.load("semantic/wordnet/wordnet-synset.rdf")
wordnet.load("semantic/wordnet/wordnet-wordsensesandwords.rdf")
wordnet.load("semantic/wordnet/wordnet-hyponym.rdf")

'''