import pandas as pd
import requests


def get_word_db(API_URL, word):
    try:
        res = requests.get(
            f'{API_URL}/get_netsci_word/?word={word}&show_context=true')
        word_db = res.json()

        df = pd.DataFrame(word_db)
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
