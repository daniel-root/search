from django.shortcuts import render
from django.http import HttpResponse
import spacy
import requests
from itertools import product, permutations
from . import wordnet
from semantic.models import Vote
from django.contrib import messages
#import language_tool_python

nlp = spacy.load('en_core_web_lg')
suffixes = list(nlp.Defaults.suffixes + [r'''\w+-\w+'''])
suffix_regex = spacy.util.compile_suffix_regex(suffixes)
nlp.tokenizer.suffix_search = suffix_regex.search
#tool = language_tool_python.LanguageTool('en-US')
API_TOKEN = 'api_sDCDNZeeeRAQvnIYclYFlzmMZUZiuEgiBN'
headers = {"Authorization": f"Bearer {API_TOKEN}"}
'''
def sentence_scores(original, sentences):    
    model = SentenceTransformer('all-MiniLM-L6-v2')

    embeddings1 = model.encode(original, convert_to_tensor=True)
    embeddings2 = model.encode(sentences, convert_to_tensor=True)

    cosine_scores = util.cos_sim(embeddings1, embeddings2)

    return [cosine_scores[0][i] for i in range(len(sentences))]
'''
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

def query(payload,sentence_transformer):
    API_URL = f"https://api-inference.huggingface.co/models/sentence-transformers/{sentence_transformer}"
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def home(request):
    data = {}
    if request.POST:
        search = request.POST['search']

        

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
        
        data['original'] = request.POST['search']
        data['sentences'] = {}

        #output = {}

        lista = query({
                "inputs": {
                    "source_sentence": request.POST['search'],
                    "sentences": list(all_results)
                },
            },'all-MiniLM-L6-v2')

        if not isinstance(lista,list):
            vote = Vote.objects.get(id=1)
            data['vote'] = round((vote.like*100) / vote.total, 2)
            messages.info(request, 'There was an error performing your search. Please try again.')  
            return render(request,'index.html',data)
        #for sentence_transformer in sentence_transformers
        #output['all-MiniLM-L6-v2'] = sentence_scores(data['original'], data['sentences'])

        all_results = list(all_results)

        #lista = list(output.values())
        total = len(lista)
        for i in range(total):          
            data['sentences'][all_results[i]] = round(lista[i], 2)
        
        data['sentences'] = {k: v for k, v in sorted(data['sentences'].items(), reverse=True, key=lambda item: item[1])}

       


        return render(request,'results.html',data)

    vote = Vote.objects.get(id=1)
    data['vote'] = round((vote.like*100) / vote.total, 2)    

    return render(request,'index.html',data)

def api(request):
    data = {}
    if request.POST:
        search = request.POST['search']
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
        
        data['original'] = request.POST['search']
        data['sentences'] = {}

        #output = {}

        lista = query({
                "inputs": {
                    "source_sentence": request.POST['search'],
                    "sentences": list(all_results)
                },
            },'all-MiniLM-L6-v2')

        if not isinstance(lista,list):
            vote = Vote.objects.get(id=1)
            data['vote'] = round((vote.like*100) / vote.total, 2)
            messages.info(request, 'There was an error performing your search. Please try again.')  
            return render(request,'index.html',data)
        #for sentence_transformer in sentence_transformers
        #output['all-MiniLM-L6-v2'] = sentence_scores(data['original'], data['sentences'])

        all_results = list(all_results)

        #lista = list(output.values())
        total = len(lista)
        for i in range(total):          
            data['sentences'][all_results[i]] = round(lista[i], 2)
        
        data['sentences'] = {k: v for k, v in sorted(data['sentences'].items(), reverse=True, key=lambda item: item[1])}

        return HttpResponse(data, content_type="application/json")

       


def voting(request):
    if request.method == "POST":
        vote = Vote.objects.get(id=1)
        classe = request.POST['classe']
        if classe == "fa-thumbs-up":
            vote.likes()
            vote.save()
        else:
            vote.deslikes()
            vote.save()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False})
