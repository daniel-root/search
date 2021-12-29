from django.shortcuts import render
import spacy
from itertools import product, permutations
from . import wordnet
import language_tool_python
from sentence_transformers import SentenceTransformer, util

nlp = spacy.load('en_core_web_lg')
suffixes = nlp.Defaults.suffixes + (r'''\w+-\w+''',)
suffix_regex = spacy.util.compile_suffix_regex(suffixes)
nlp.tokenizer.suffix_search = suffix_regex.search
tool = language_tool_python.LanguageTool('en-US')

sentence_transformers = ['all-mpnet-base-v2',
                         'clip-ViT-B-32',
                         'msmarco-bert-co-condensor',
                         'msmarco-distilbert-cos-v5',
                         'msmarco-MiniLM-L12-cos-v5',
                         'msmarco-MiniLM-L6-cos-v5',
                         'facebook-dpr-ctx_encoder-multiset-base',
                         'msmarco-bert-base-dot-v5', 
                         'msmarco-distilbert-dot-v5',
                         'all-roberta-large-v1', 
                         'paraphrase-distilroberta-base-v2',
                         'all-mpnet-base-v1',
                         'paraphrase-mpnet-base-v2',
                         'paraphrase-MiniLM-L12-v2', 
                         'paraphrase-MiniLM-L6-v2', 
                         'paraphrase-MiniLM-L3-v2', 
                         'all-MiniLM-L12-v2',
                         'all-MiniLM-L12-v1', 
                         'all-MiniLM-L6-v2', 
                         'all-MiniLM-L6-v1', 
                         'all-distilroberta-v1', 
                         'multi-qa-mpnet-base-cos-v1', 
                         'msmarco-distilbert-base-tas-b',
                         'multi-qa-mpnet-base-dot-v1', 
                         'multi-qa-distilbert-cos-v1', 
                         'multi-qa-MiniLM-L6-cos-v1', 
                         'multi-qa-distilbert-dot-v1',
                         'multi-qa-MiniLM-L6-dot-v1',
                         'xlm-r-large-en-ko-nli-ststb', 
                         'xlm-r-distilroberta-base-paraphrase-v1',
                         'xlm-r-bert-base-nli-stsb-mean-tokens', 
                         'xlm-r-bert-base-nli-mean-tokens', 
                         'xlm-r-base-en-ko-nli-ststb', 
                         'xlm-r-100langs-bert-base-nli-stsb-mean-tokens', 
                         'xlm-r-100langs-bert-base-nli-mean-tokens', 
                         'stsb-xlm-r-multilingual', 
                         'stsb-roberta-large', 
                         'stsb-roberta-base', 
                         'stsb-roberta-base-v2', 
                         'stsb-mpnet-base-v2', 
                         'stsb-distilroberta-base-v2',
                         'stsb-distilbert-base', 
                         'stsb-bert-base', 
                         'roberta-large-nli-stsb-mean-tokens',
                         'roberta-large-nli-mean-tokens', 
                         'roberta-base-nli-stsb-mean-tokens',
                         'roberta-base-nli-mean-tokens',
                         'quora-distilbert-multilingual', 
                         'quora-distilbert-base', 
                         'paraphrase-xlm-r-multilingual-v1',
                         'paraphrase-multilingual-mpnet-base-v2', 
                         'paraphrase-multilingual-MiniLM-L12-v2',
                         'paraphrase-distilroberta-base-v1', 
                         'paraphrase-albert-small-v2',
                         'paraphrase-albert-base-v2',
                         'paraphrase-TinyBERT-L6-v2', 
                         'nq-distilbert-base-v1', 
                         'nli-roberta-large', 
                         'nli-roberta-base', 
                         'nli-roberta-base-v2',
                         'nli-mpnet-base-v2', 
                         'nli-distilroberta-base-v2',
                         'nli-distilbert-base', 
                         'nli-distilbert-base-max-pooling',
                         'nli-bert-large', 
                         'nli-bert-large-max-pooling',
                         'nli-bert-large-cls-pooling',
                         'nli-bert-base', 
                         'nli-bert-base-max-pooling', 
                         'nli-bert-base-cls-pooling',
                         'msmarco-roberta-base-v3',
                         'msmarco-roberta-base-v2',
                         'msmarco-roberta-base-ance-firstp',
                         'msmarco-distilroberta-base-v2', 
                         'msmarco-distilbert-multilingual-en-de-v2-tmp-trained-scratch',
                         'msmarco-distilbert-multilingual-en-de-v2-tmp-lng-aligned',
                         'msmarco-distilbert-base-v4', 
                         'msmarco-distilbert-base-v3', 
                         'msmarco-distilbert-base-v2', 
                         'msmarco-distilbert-base-dot-prod-v3', 
                         'msmarco-MiniLM-L-6-v3', 
                         'msmarco-MiniLM-L-12-v3', 
                         'facebook-dpr-question_encoder-single-nq-base',
                         'facebook-dpr-question_encoder-multiset-base', 
                         'facebook-dpr-ctx_encoder-single-nq-base', 
                         'distiluse-base-multilingual-cased', 
                         'distiluse-base-multilingual-cased-v2',
                         'distiluse-base-multilingual-cased-v1',
                         'distilroberta-base-paraphrase-v1',
                         'distilroberta-base-msmarco-v2',
                         'distilroberta-base-msmarco-v1', 
                         'distilbert-multilingual-nli-stsb-quora-ranking',
                         'distilbert-base-nli-stsb-quora-ranking', 
                         'distilbert-base-nli-stsb-mean-tokens',
                         'clip-ViT-B-32-multilingual-v1', 
                         'bert-large-nli-stsb-mean-tokens', 
                         'bert-large-nli-mean-tokens', 
                         'bert-large-nli-max-tokens',
                         'bert-large-nli-cls-token',
                         'bert-base-wikipedia-sections-mean-tokens',
                         'bert-base-nli-stsb-mean-tokens', 
                         'bert-base-nli-mean-tokens',
                         'bert-base-nli-max-tokens',
                         'bert-base-nli-cls-token',
                         'average_word_embeddings_levy_dependency',
                         'average_word_embeddings_komninos',
                         'average_word_embeddings_glove.840B.300d',
                         'average_word_embeddings_glove.6B.300d',
                         'allenai-specter',
                         'LaBSE']

def sentence_scores(original, sentences, model):    
    model = SentenceTransformer(model)

    embeddings1 = model.encode(original, convert_to_tensor=True)
    embeddings2 = model.encode(sentences, convert_to_tensor=True)

    cosine_scores = util.cos_sim(embeddings1, embeddings2)

    return [cosine_scores[0][i] for i in range(len(sentences))]

def correct(original,sentenses):       
    frase = tool.correct(original)

    aux = []
    for i in list(sentenses):
        aux.append(tool.correct(i))

    return frase, aux

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

        teste = {}
        for i in range(len(a)):
            teste[' '.join(grams[i])] = ' '.join(a[i])
        
        for gram in token_grams:
            original, results = create_sentences([' '.join(i) for i in gram],semantic[0])
            originals.append(gram)
            all_results.extend(results)
        
        all_results = set(all_results)

        original, all_results = correct(original,all_results)
        
        data['original'] = originals
        data['sentences'] = all_results

        #output = {}

        #output[''] = data['sentences']

    '''
        for sentence_transformer in sentence_transformers:
            output[sentence_transformer] = sentence_scores(data['original'], data['sentences'], sentence_transformer)
    '''
        return render(request,'results.html',data)
    
    return render(request,'index.html')