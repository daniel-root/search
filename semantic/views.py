from django.shortcuts import render
from django.http import HttpResponse
import spacy
nlp = spacy.load('en_core_web_lg')
from itertools import product
from . import wordnet
#import language_tool_python
import requests
import csv
from django.http import JsonResponse


API_TOKEN = 'api_sDCDNZeeeRAQvnIYclYFlzmMZUZiuEgiBN'
headers = {"Authorization": f"Bearer {API_TOKEN}"}
sentence_transformers = ['sentence-transformers/all-mpnet-base-v2', 'sentence-transformers/clip-ViT-B-32', 'sentence-transformers/msmarco-bert-co-condensor', 'sentence-transformers/msmarco-distilbert-cos-v5', 'sentence-transformers/msmarco-MiniLM-L12-cos-v5', 'sentence-transformers/msmarco-MiniLM-L6-cos-v5', 'sentence-transformers/facebook-dpr-ctx_encoder-multiset-base', 'sentence-transformers/msmarco-bert-base-dot-v5', 'sentence-transformers/msmarco-distilbert-dot-v5', 'sentence-transformers/all-roberta-large-v1', 'sentence-transformers/paraphrase-distilroberta-base-v2', 'sentence-transformers/all-mpnet-base-v1', 'sentence-transformers/paraphrase-mpnet-base-v2', 'sentence-transformers/paraphrase-MiniLM-L12-v2', 'sentence-transformers/paraphrase-MiniLM-L6-v2', 'sentence-transformers/paraphrase-MiniLM-L3-v2', 'sentence-transformers/all-MiniLM-L12-v2', 'sentence-transformers/all-MiniLM-L12-v1', 'sentence-transformers/all-MiniLM-L6-v2', 'sentence-transformers/all-MiniLM-L6-v1', 'sentence-transformers/all-distilroberta-v1', 'sentence-transformers/multi-qa-mpnet-base-cos-v1', 'sentence-transformers/msmarco-distilbert-base-tas-b', 'sentence-transformers/multi-qa-mpnet-base-dot-v1', 'sentence-transformers/multi-qa-distilbert-cos-v1', 'sentence-transformers/multi-qa-MiniLM-L6-cos-v1', 'sentence-transformers/multi-qa-distilbert-dot-v1', 'sentence-transformers/multi-qa-MiniLM-L6-dot-v1', 'sentence-transformers/xlm-r-large-en-ko-nli-ststb', 'sentence-transformers/xlm-r-distilroberta-base-paraphrase-v1', 'sentence-transformers/xlm-r-bert-base-nli-stsb-mean-tokens', 'sentence-transformers/xlm-r-bert-base-nli-mean-tokens', 'sentence-transformers/xlm-r-base-en-ko-nli-ststb', 'sentence-transformers/xlm-r-100langs-bert-base-nli-stsb-mean-tokens', 'sentence-transformers/xlm-r-100langs-bert-base-nli-mean-tokens', 'sentence-transformers/stsb-xlm-r-multilingual', 'sentence-transformers/stsb-roberta-large', 'sentence-transformers/stsb-roberta-base', 'sentence-transformers/stsb-roberta-base-v2', 'sentence-transformers/stsb-mpnet-base-v2', 'sentence-transformers/stsb-distilroberta-base-v2', 'sentence-transformers/stsb-distilbert-base', 'sentence-transformers/stsb-bert-large', 'sentence-transformers/stsb-bert-base', 'sentence-transformers/roberta-large-nli-stsb-mean-tokens', 'sentence-transformers/roberta-large-nli-mean-tokens', 'sentence-transformers/roberta-base-nli-stsb-mean-tokens', 'sentence-transformers/roberta-base-nli-mean-tokens', 'sentence-transformers/quora-distilbert-multilingual', 'sentence-transformers/quora-distilbert-base', 'sentence-transformers/paraphrase-xlm-r-multilingual-v1', 'sentence-transformers/paraphrase-multilingual-mpnet-base-v2', 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2', 'sentence-transformers/paraphrase-distilroberta-base-v1', 'sentence-transformers/paraphrase-albert-small-v2', 'sentence-transformers/paraphrase-albert-base-v2', 'sentence-transformers/paraphrase-TinyBERT-L6-v2', 'sentence-transformers/nq-distilbert-base-v1', 'sentence-transformers/nli-roberta-large', 'sentence-transformers/nli-roberta-base', 'sentence-transformers/nli-roberta-base-v2', 'sentence-transformers/nli-mpnet-base-v2', 'sentence-transformers/nli-distilroberta-base-v2', 'sentence-transformers/nli-distilbert-base', 'sentence-transformers/nli-distilbert-base-max-pooling', 'sentence-transformers/nli-bert-large', 'sentence-transformers/nli-bert-large-max-pooling', 'sentence-transformers/nli-bert-large-cls-pooling', 'sentence-transformers/nli-bert-base', 'sentence-transformers/nli-bert-base-max-pooling', 'sentence-transformers/nli-bert-base-cls-pooling', 'sentence-transformers/msmarco-roberta-base-v3', 'sentence-transformers/msmarco-roberta-base-v2', 'sentence-transformers/msmarco-roberta-base-ance-firstp', 'sentence-transformers/msmarco-distilroberta-base-v2', 'sentence-transformers/msmarco-distilbert-multilingual-en-de-v2-tmp-trained-scratch', 'sentence-transformers/msmarco-distilbert-multilingual-en-de-v2-tmp-lng-aligned', 'sentence-transformers/msmarco-distilbert-base-v4', 'sentence-transformers/msmarco-distilbert-base-v3', 'sentence-transformers/msmarco-distilbert-base-v2', 'sentence-transformers/msmarco-distilbert-base-dot-prod-v3', 'sentence-transformers/msmarco-MiniLM-L-6-v3', 'sentence-transformers/msmarco-MiniLM-L-12-v3', 'sentence-transformers/facebook-dpr-question_encoder-single-nq-base', 'sentence-transformers/facebook-dpr-question_encoder-multiset-base', 'sentence-transformers/facebook-dpr-ctx_encoder-single-nq-base', 'sentence-transformers/distiluse-base-multilingual-cased', 'sentence-transformers/distiluse-base-multilingual-cased-v2', 'sentence-transformers/distiluse-base-multilingual-cased-v1', 'sentence-transformers/distilroberta-base-paraphrase-v1', 'sentence-transformers/distilroberta-base-msmarco-v2', 'sentence-transformers/distilroberta-base-msmarco-v1', 'sentence-transformers/distilbert-multilingual-nli-stsb-quora-ranking', 'sentence-transformers/distilbert-base-nli-stsb-quora-ranking', 'sentence-transformers/distilbert-base-nli-stsb-mean-tokens', 'sentence-transformers/distilbert-base-nli-mean-tokens', 'sentence-transformers/distilbert-base-nli-max-tokens', 'sentence-transformers/clip-ViT-B-32-multilingual-v1', 'sentence-transformers/bert-large-nli-stsb-mean-tokens', 'sentence-transformers/bert-large-nli-mean-tokens', 'sentence-transformers/bert-large-nli-max-tokens', 'sentence-transformers/bert-large-nli-cls-token', 'sentence-transformers/bert-base-wikipedia-sections-mean-tokens', 'sentence-transformers/bert-base-nli-stsb-mean-tokens', 'sentence-transformers/bert-base-nli-mean-tokens', 'sentence-transformers/bert-base-nli-max-tokens', 'sentence-transformers/bert-base-nli-cls-token', 'sentence-transformers/average_word_embeddings_levy_dependency', 'sentence-transformers/average_word_embeddings_komninos', 'sentence-transformers/average_word_embeddings_glove.840B.300d', 'sentence-transformers/average_word_embeddings_glove.6B.300d', 'sentence-transformers/allenai-specter', 'sentence-transformers/LaBSE']

#model = SentenceTransformer('stsb-roberta-large')
#tool = language_tool_python.LanguageTool('en-US')
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


def query(payload,sentence_transformer):
    API_URL = f"https://api-inference.huggingface.co/models/{sentence_transformer}"
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def home(request):
    if request.POST:
        search = request.POST['search']
        data = {}
        conference_help_doc = nlp(search)
        lemmatization = [[token.lemma_ for token in conference_help_doc]]
        semantic = wordnet.busca_semantica(lemmatization)
        data['semantic'] = semantic
        data['original'], data['sentences'] = create_sentences(lemmatization[0], semantic[0])
        #data['original'], data['sentences'] = correct(original, sentences)
        output = {}

        output[''] = data['sentences']
        return render(request,'results.html',data)
    '''
        for sentence_transformer in sentence_transformers:
            output[sentence_transformer] = query({
                "inputs": {
                    "source_sentence": data['original'],
                    "sentences": data['sentences']
                },
            },sentence_transformer)

        response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="somefilename.csv"'},
        )
        
        #a_file = open("sample.csv", "w")
        writer = csv.writer(response)
        for key, value in output.items():
            writer.writerow([key, value])
        #a_file.close()
        
        return response
       '''
        
    return render(request,'index.html')

def search_api(request):
    if request.GET:
        search = request.GET['search']
        data = {}
        conference_help_doc = nlp(search)
        lemmatization = [[token.lemma_ for token in conference_help_doc]]
        semantic = wordnet.busca_semantica(lemmatization)
        data['semantic'] = semantic
        data['original'], data['sentences'] = create_sentences(lemmatization[0], semantic[0])
        return JsonResponse(data)