from django.shortcuts import render
import spacy
nlp = spacy.load('pt_core_news_sm')
from itertools import product
from . import wordnet
import language_tool_python
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('stsb-roberta-large')
tool = language_tool_python.LanguageTool('pt-BR')

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

def home(request):
    if request.POST:
        search = request.POST['search']
        data = {}
        conference_help_doc = nlp(search)
        lemmatization = [[token.lemma_ for token in conference_help_doc]]
        semantic = wordnet.busca_semantica(lemmatization)
        data['semantic'] = semantic
        #original, sentenses = create_sentences(lemmatization[0], semantic[0])
        data['original'], data['sentences'] = create_sentences(lemmatization[0], semantic[0])
        print(data['original'], data['sentences'])


        '''sentences1 = data['original'] 
        sentences2 = data['sentences']
        # encode list of sentences to get their embeddings
        embedding1 = model.encode(sentences1, convert_to_tensor=True)
        embedding2 = model.encode(sentences2, convert_to_tensor=True)
        # compute similarity scores of two embeddings
        cosine_scores = util.pytorch_cos_sim(embedding1, embedding2)
        for i in range(len(sentences1)):
            for j in range(len(sentences2)):
            #if cosine_scores[i][j].item() > 0.90:
                print("Sentence 1:", sentences1[i])
                print("Sentence 2:", sentences2[j])
                print("Similarity Score:", cosine_scores[i][j].item())
                print()
        '''
        return render(request,'results.html',data)
    return render(request,'index.html')