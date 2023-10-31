import pandas as pd
import requests
from .sense import util

def get_word_list_db(API_URL):
    try:
        res = requests.get(
            f'{API_URL}/get_word_list/')
        word_db = res.json()

        #df = pd.DataFrame(word_db)
        return word_db
    except:
        return pd.DataFrame()

def get_netsci_word(API_URL, word):
    try:
        res = requests.get(f'{API_URL}/get_netsci_word/?word={word}&show_context=true')
        word_db = res.json()

        df = pd.DataFrame(word_db)
        return df
    except:
        return pd.DataFrame()

def get_nlp_word(API_URL, word):
    try:
        res = requests.get(
            f'{API_URL}/get_nlp_word/?word={word}')
        word_db = res.json()

        for word in word_db:
            word['example_sentences'] = util.sanitize_sample_sentences(word['example_sentences'])

        df = pd.DataFrame(word_db)  
        df = df.sort_values(by=['sense_id'])

        return df
    except Exception as e:
        print(repr(e))
        print(e)
        return pd.DataFrame()

def get_word_db(API_URL, word):
    try:
        res = requests.get(f'{API_URL}/get_netsci_word/?word={word}&show_context=true')
        word_db = res.json()

        df = pd.DataFrame(word_db)
        df = df.sort_values(by=['sense_id'])
        return df
    except:
        return pd.DataFrame()

def get_word_embeddings_db(API_URL, word):
    try:
        res = requests.get(f'{API_URL}/get_nlp_word/?word={word}')
        word_db = res.json()

        df = pd.DataFrame(word_db)

        return df
    except:
        return pd.DataFrame()


def get_pca_embeddings(API_URL, sense_id):
    try:
        res = requests.get(
            f'{API_URL}/get_pca_embeddings/?sense_id={sense_id}')
        pca_embeddings = res.json()

        return pca_embeddings
    except:
        return None


def get_netsci_word(API_URL, word):
    try:
        res = requests.get(f'{API_URL}/get_netsci_word/?word={word}')
        netsci_word = res.json()

        return netsci_word
    except:
        return None
