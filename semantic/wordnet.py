from rdflib import Graph
from rdflib.plugins.sparql import prepareQuery
from rdflib.namespace import RDFS, RDF, OWL, XSD
from rdflib import URIRef, Namespace

SCHEMA = Namespace("http://www.w3.org/2006/03/wn/wn20/schema/")
INSTANCES = Namespace("http://www.w3.org/2006/03/wn/wn20/instances/")

wordnet = Graph()
wordnet.load("./wordnet/wnfull.rdfs")
wordnet.load("./wordnet/wordnet-antonym.rdf")
wordnet.load("./wordnet/wordnet-attribute.rdf")
wordnet.load("./wordnet/wordnet-causes.rdf")
wordnet.load("./wordnet/wordnet-classifiedby.rdf")
wordnet.load("./wordnet/wordnet-derivationallyrelated.rdf")
wordnet.load("./wordnet/wordnet-entailment.rdf")
wordnet.load("./wordnet/wordnet-frame.rdf")
wordnet.load("./wordnet/wordnet-glossary.rdf")
wordnet.load("./wordnet/wordnet-membermeronym.rdf")
wordnet.load("./wordnet/wordnet-participleof.rdf")
wordnet.load("./wordnet/wordnet-partmeronym.rdf")
wordnet.load("./wordnet/wordnet-pertainsto.rdf")
wordnet.load("./wordnet/wordnet-sameverbgroupas.rdf")
wordnet.load("./wordnet/wordnet-seealso.rdf")
wordnet.load("./wordnet/wordnet-similarity.rdf")
wordnet.load("./wordnet/wordnet-substancemeronym.rdf")
wordnet.load("./wordnet/wordnet-synset.rdf")
wordnet.load("./wordnet/wordnet-wordsensesandwords.rdf")
wordnet.load("./wordnet/wordnet-hyponym.rdf")

def synset(word):
  
  pre_query = """
  SELECT ?aSynset
  WHERE {
    ?aSynset wn20schema:containsWordSense ?aWordSense .
    ?aWordSense wn20schema:word ?aWord .
    ?aWord wn20schema:lexicalForm  "%s"@en-US
    }
    """ % (word)

  query = prepareQuery(pre_query, initNs = { "rdfs": RDFS, "wn20schema": SCHEMA,  "wn20instances": INSTANCES})

  results = wordnet.query(query)

  return [ row['aSynset'] for row in results]

def busca_semantica(sentenses):
  data = []
  for words in sentenses:
    aux = {}
    for word in words:
      results = synset(word)
      aux[word] = results
    data.append(aux)
  return data