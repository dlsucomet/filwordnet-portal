import pandas as pd
import re
import json
from sklearn.decomposition import PCA


def get_definition_list(word):
    df = pd.read_csv('static/data/merged_wordnet.csv')

    def_list = df.loc[df['word'] == word]
    def_list = def_list.reset_index()

    return def_list


def sanitize_example_sentences(data, df):
    data = df.loc[data, 'example_sentences']
    data = data.strip()
    data = data[1:]
    data = data[:-1]
    data = data.replace("'", '"')
    data = data.split(',')

    return data


def sanitize_pos(pos):
    pos_dict = {
        'NN': 'Noun',
        'VB': 'Verb'
    }

    if pos:
        pos = str(pos)
        if pos != 'nan':
            pos = pos[1:]
            pos = pos[:-1]
            pos = pos.replace("'", '')

            return pos, pos_dict[pos]
        else:
            return '', ''

    return '', ''


def display_pos_with_id(sense_id, pos):
    pos_abbrev, pos_fullname = sanitize_pos(pos)

    if pos_abbrev:
        return f'{sense_id} - {pos_fullname} ({pos_abbrev})'

    return f'{sense_id}'


def sanitize_network_data(network):
    if network:
        network = str(network)
        if network != 'nan':
            network = network.replace('list', '')
            network = network[3:]
            network = network[:-3]
            network = network.replace(',', '')
            network = network.replace("'", '')
            network = network.split()

            return network

    return ''


def load_network():

    return None


def sanitize_embeddings(embeddings):
    if embeddings:
        embeddings = str(embeddings)
        if embeddings != 'nan':
            embeddings = embeddings.replace('tensor', '')
            embeddings = embeddings[4:]
            embeddings = embeddings[:-3]
            embeddings = embeddings.replace(',', '')
            embeddings = embeddings.split()
            embeddings = [eval(e.strip())
                          for e in embeddings]  # change string to float

            return embeddings

    return ''


def load_embeddings(embeddings_list):
    if embeddings_list:

        pca = PCA(n_components=3)

        return pca.fit_transform(embeddings_list)

    return ''


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
