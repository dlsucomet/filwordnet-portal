import pandas as pd


def get_definition_list(word):
    df = pd.read_csv('static/data/merged_wordnet.csv')

    def_list = df.loc[df['word'] == word]
    def_list = def_list.reset_index()

    return def_list

