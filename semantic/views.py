from django.shortcuts import render
import spacy
from itertools import product, permutations
from . import wordnet
#import language_tool_python
from sentence_transformers import SentenceTransformer, util

nlp = spacy.load('en_core_web_lg')
suffixes = list(nlp.Defaults.suffixes + [r'''\w+-\w+'''])
suffix_regex = spacy.util.compile_suffix_regex(suffixes)
nlp.tokenizer.suffix_search = suffix_regex.search
#tool = language_tool_python.LanguageTool('en-US')


def sentence_scores(original, sentences):    
    model = SentenceTransformer('all-MiniLM-L6-v2')

    embeddings1 = model.encode(original, convert_to_tensor=True)
    embeddings2 = model.encode(sentences, convert_to_tensor=True)

    cosine_scores = util.cos_sim(embeddings1, embeddings2)

    return [cosine_scores[0][i] for i in range(len(sentences))]
'''
def correct(original,sentenses):       
    frase = tool.correct(original)

    aux = []
    for i in list(sentenses):
        aux.append(tool.correct(i))

    return frase, aux
'''
def create_sentences(lista, biblioteca):
    lista_a = []
    for i in lista:
        lista_a.append(biblioteca[i])
    l = []
    for i in range(1,len(lista_a)):
        if len(lista_a[i-1]) == 0:
            lista_a[i-1] = [lista[i-1]]
        if len(lista_a[i]) == 0:
            lista_a[i] = [lista[i]]
        x = list(product(lista_a[i-1], lista_a[i]))
        lista_a[i] = set([' '.join(j) for j in x])
    return ' '.join(lista) , lista_a[-1]

def getNGrams(wordlist, n):
    return [wordlist[i:i+n] for i in range(len(wordlist)-(n-1))]

def home(request):
    if request.POST:
        search = request.POST['search']

        data = {}

        conference_help_doc = nlp(search)

        #Tokenalização e Lematização
        lemmatization, token = [token.lemma_ for token in conference_help_doc],[token.norm_ for token in conference_help_doc]

        #N-grams
        unigrams = [[i] for i in lemmatization]
        bigrams = getNGrams(lemmatization,2)

        #Token n-gramas
        token_uni = [[i] for i in token]
        token_bi = getNGrams(token,2)

        #N-grams
        grams = unigrams + bigrams
        
        search = ' '.join(lemmatization) + ' '

        token_grams = []

        for i in range(len(unigrams),1,-1):
            for tokens in permutations(grams,i):
                string = ''
                for token in tokens:
                    string += ' '.join(token) + ' '
                if string == search:
                    token_grams.append(list(tokens))

        semantic = wordnet.busca_semantica([grams])

        originals = []
        all_results = []

        a = token_uni + token_bi

        teste = {}

        for i in range(len(a)):
            teste[' '.join(grams[i])] = ' '.join(a[i])
        
        for i in semantic[0].keys():
            semantic[0][i].append(teste[i])

        for gram in token_grams:
            original, results = create_sentences([' '.join(i) for i in gram],semantic[0])
            originals.append(gram)
            all_results.extend(results)
        
        all_results = set(all_results)

        #original, all_results = correct(original,all_results)
        
        data['original'] = original
        data['sentences'] = all_results
        data['score'] = {}

        output = {}

        #for sentence_transformer in sentence_transformers
        output['all-MiniLM-L6-v2'] = sentence_scores(data['original'], data['sentences'])

        lista = list(output.values())[1:]
        total = len(output)
        for i in range(total):
            soma = 0
            for j in lista:
                soma += j[i]
            
            data['score'][all_results[i]] = float(soma/total)

        return render(request,'results.html',data)
    
    return render(request,'index.html')