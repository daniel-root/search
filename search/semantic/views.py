from django.shortcuts import render
from nltk import data
from . import wordnet
# Create your views here.

import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from itertools import product
import re
pattern = r"[^\w]"
nltk.download('wordnet')
nltk.download('stopwords')
lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()
stop_words = set(stopwords.words("english"))


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


def regex(words):
    data = []
    for word in words:
        data.append(re.sub(pattern, " ", word))
    return data

def stop_word(words):
    data = []
    for word in words:
        data.append([w for w in word if not w in stop_words])
    return data

def stem(words):
    data = []
    for word in words:
        for w in word:
            data.append(stemmer.stem(w))
    return data

def lemmatize(words):
    data = []
    for word in words:
        for w in word:
            data.append(lemmatizer.lemmatize(w, wordnet.VERB))
    return data

def word_tokenize(sentenses):
    data = []
    for sentense in sentenses:
        data.append(nltk.word_tokenize(sentense))
    return data

def home(request):
    if request.POST:
        search = request.POST['search']
        data = {}
        sentence_tokenization = nltk.sent_tokenize(search)
        data['sentence_tokenization'] = sentence_tokenization
        regex_ = regex(sentence_tokenization)
        data['regex_'] = regex_
        word_tokenization = word_tokenize(regex_)
        data['word_tokenization'] = word_tokenization
        lemmatization = lemmatize(word_tokenization)
        data['lemmatization'] = lemmatization
        stemming = stem(word_tokenization)
        data['stemming'] = stemming
        without_stop_words = stop_word(word_tokenization)
        data['without_stop_words'] = without_stop_words
        semantic = {'Backgammon': [], 'be': ['be', 'be', 'exist', 'be', 'be', 'be', 'constitute', 'be', 'equal', 'embody', 'cost', 'be', 'be'], 'one': ['one', 'one', 'one', 'one'], 'of': [], 'the': [], 'oldest': ['oldest'], 'know': ['acknowledge', 'know', 'know', 'know', 'know', 'know', 'know', 'know', 'know', 'know', 'roll in the hay'], 'board': ['board', 'board', 'circuit board', 'control panel', 'dining table', 'display panel', 'board', 'board', 'board', 'board', 'board', 'board', 'board'], 'game': ['game', 'game', 'game', 'game', 'game', 'game', 'game', 'plot', 'game', 'game', 'bet on', 'game', 'crippled']}
        data['semantic'] = semantic
        data['original'], data['sentences'] = create_sentences(lemmatization, semantic)
        return render(request,'results.html',data)
    return render(request,'index.html')