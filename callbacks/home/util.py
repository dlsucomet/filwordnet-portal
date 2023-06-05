import pandas as pd
import re
import json


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


def convert_double_quotes_json(string):
    pattern = re.compile('(?<!\\\\)\'')
    return pattern.sub('\"', string)


def convert_to_data_by_sense(contextual_info, sense_ids):
    data_matrix = []
    for i in range(0, len(contextual_info)):
        sources = json.loads(convert_double_quotes_json(contextual_info[i]))
        for categories in sources:
            for title in sources[categories]:
                for year in sources[categories][title]:
                    entry = [sources[categories][title][year], year,
                             title, categories, sense_ids[i]]
                    data_matrix.append(entry)

    return pd.DataFrame(data_matrix, columns=['counts', 'year', 'source', 'category', 'sense'])
