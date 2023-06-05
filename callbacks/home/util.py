import pandas as pd


def get_definition_list(word):
    df = pd.read_csv('static/data/merged_wordnet.csv')
    def_list = df.loc[df['word'] == word]

    return def_list


def sanitize_str_list_to_list(data):
    data = str(data)
    data = data.strip()
    data = data[1:]
    data = data[:-1]
    data = data.split(',')

    return data


def sanitize_example_sentences(data, df):
    example_sentences = df.loc[data, 'example_sentences']
    example_sentences = sanitize_str_list_to_list(example_sentences)

    return example_sentences
