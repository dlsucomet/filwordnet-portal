import json
import re

import pandas as pd

from ..sense.util import *

SOURCES = {'books': ['bible', 'gutenberg', 'google_books'],
           'news_sites': ['abante', 'abscbn', 'balita', 'bandera', 'gma', 'kami', 'mb', 'philstar', 'radyoinquirer'],
           'social_media': ['twitter', 'youtube', 'wattpad'],
           'online_forums': ['reddit', 'pinoyexchange'],
           'wikipedia': ['wikipedia'],
           'dictionaries': ['wikitionary', 'pinoydictionary']}


def convert_to_data_by_sense(contextual_info, sense_ids, pos_list, nlp=False):
    data_matrix = []
    for i in range(0, len(contextual_info)):
        sources = contextual_info[i]

        if nlp:
            sources = sanitize_sources(contextual_info[i])

        for categories in sources:
            for title in sources[categories]:
                for year in sources[categories][title]:
                    pos = ''
                    if pos:
                        pos = pos_list[i]
                    sense_and_pos = sense_and_pos_text(f'Sense {i+1}', pos)
                    category = sanitize_category(categories)

                    entry = [sources[categories][title][year], year,
                             title, category, sense_ids[i], sense_and_pos]
                    data_matrix.append(entry)

    return pd.DataFrame(data_matrix, columns=['counts', 'year', 'source', 'category', 'sense', 'sense_and_pos'])


def sanitize_category(category):
    category = category.split('_')

    text_list = []
    for text in category:
        text_list.append(text.capitalize())

    return ' '.join(text_list)


def sense_and_pos_text(sense, pos):
    pos_abbrev, pos_name = sanitize_pos(pos)

    if pos_name:
        return f'{sense} ({pos_name})'

    return f'{sense}'


def find_first_sample_sentence(sample_sentences):
    for sentence in sample_sentences:
        if is_quality_sentence(sentence):
            return sentence.capitalize()

    return ''


def sanitize_sources(nlp_contextual_info):
    nlp_contextual_info = nlp_contextual_info.replace("\'", "\"")
    contextual_info = json.loads(nlp_contextual_info)

    sources_dict = {}
    for source_category, sources in SOURCES.items():
        for source in sources:
            try:
                contextual_info[source]
            except:
                continue

            if source_category not in sources_dict:
                sources_dict[source_category] = {}

            sources_dict[source_category][source] = contextual_info[source]

    return sources_dict
