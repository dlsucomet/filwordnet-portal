import json

from ..api_query import *
from ..plot.util import *
from ..sense.util import *


def sanitize_embeddings(embeddings):
    if embeddings:
        if embeddings != 'nan':
            embeddings = embeddings[1:-1]
            embeddings = embeddings.split()
            embeddings = [eval(e.strip())
                          for e in embeddings]  # change string to float

            return embeddings

    return ''


def get_all_embeddings(API_URL, word):
    df = get_word_embeddings_db(API_URL, word)

    embeddings_list = []

    for i in range(len(df)):
        embeddings = df.iloc[i]['sense_embedding']
        embeddings = sanitize_embeddings(embeddings)
        if embeddings:
            embeddings_list.append(embeddings)

    return embeddings_list


def get_all_info(API_URL, word):
    netsci_word_df = get_word_db(API_URL, word)
    nlp_word_df = get_nlp_word(API_URL, word)

    final_json = {}
    sense_idx = 1
    if len(netsci_word_df) >= 1:
        for i in range(len(netsci_word_df)):
            final_json[f'Sense {sense_idx}'] = {}

            final_json[f'Sense {sense_idx}']['example_sentences'] = []
            example_sentences = netsci_word_df.iloc[i]['example_sentences']
            for sentence in example_sentences:
                if is_quality_sentence(sentence):
                    final_json[f'Sense {sense_idx}']['example_sentences'].append(
                        capitalize_first_word(sentence))

            final_json[f'Sense {sense_idx}']['contextual_info'] = netsci_word_df.iloc[i]['contextual_info']
            final_json[f'Sense {sense_idx}']['community'] = netsci_word_df.iloc[i]['community']

            sense_idx += 1

    if len(nlp_word_df) >= 1:
        for i in range(len(nlp_word_df)):
            final_json[f'Sense {sense_idx}'] = {}

            final_json[f'Sense {sense_idx}']['example_sentences'] = []
            for sentence in nlp_word_df.iloc[i]['example_sentences']:
                if is_quality_sentence(sentence):
                    final_json[f'Sense {sense_idx}']['example_sentences'].append(
                        capitalize_first_word(sentence))

            final_json[f'Sense {sense_idx}']['contextual_info'] = sanitize_sources(
                nlp_word_df.iloc[i]['contextual_info'])

            sense_idx += 1

    return json.dumps(final_json)
