import pandas as pd
import requests

def get_definition_list(word):
    df = pd.read_csv('static/data/merged_wordnet.csv')

    def_list = df.loc[df['word'] == word.lower()]
    def_list = def_list.reset_index()

    return def_list

def get_word_db(API_URL, word):
    try:
        #res = requests.get(f'{API_URL}/get_sentences?query={word}')
        res = requests.get(f'{API_URL}/get_netsci_word/?word={word}')
        #res = requests.get(f'{API_URL}/get_nlp_word/?word={word}')
        word_db = res.json()
        
        df = pd.DataFrame(word_db)

        return df
    except:
        return pd.DataFrame()




