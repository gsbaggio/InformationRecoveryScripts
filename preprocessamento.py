import spacy
import unicodedata
import nltk
from nltk.stem import RSLPStemmer
from nltk.corpus import stopwords

tokenizer_ptbr = spacy.load("pt_core_news_sm") # tokenizer do spacy

nltk.download("stopwords")
nltk.download("rslp")

stemmer = RSLPStemmer() # stemmer do nltk
stop_words = set(stopwords.words("portuguese")) # stopwords do nltk

def removeAcentos(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto) 
        if unicodedata.category(c) != 'Mn'
    )

def preProcessamento(doc):
    tokens = tokenizer_ptbr(doc) # transforma o texto em tokens

    # transforma os tokens. Tira sinais de pontuacao, remove 'stop words', passa pra minusculo, remove acentos e aplica stemmer (tira sufixos)

    tokens = [token for token in tokens if not token.is_punct] # verifica se não é pontuação

    tokens = [token for token in tokens if token.is_alpha] # verifica se não é '\n', etc

    tokens = [token.text for token in tokens] # transforma de objetos para strings

    tokens = [token.lower() for token in tokens] # deixa minusculo

    tokens = [token for token in tokens if token not in stop_words] # verifica se não é stopword

    tokens = [stemmer.stem(token) for token in tokens] # remove sufixos e radicais (stemming)   

    tokens = [removeAcentos(token) for token in tokens] # remove acentos

    return tokens
