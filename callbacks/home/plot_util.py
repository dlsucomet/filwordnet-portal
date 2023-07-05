import pandas as pd
import re
import json
from .sense_util import *


def convert_double_quotes_json(string):
    pattern = re.compile('(?<!\\\\)\'')
    return pattern.sub('\"', string)


def convert_to_data_by_sense(contextual_info, sense_ids, pos_list):
    data_matrix = []
    for i in range(0, len(contextual_info)):
        sources = json.loads(convert_double_quotes_json(contextual_info[i]))
        for categories in sources:
            for title in sources[categories]:
                for year in sources[categories][title]:
                    pos_abbrev, pos = sanitize_pos(pos_list[i])
                    category = sanitize_category(categories)

                    entry = [sources[categories][title][year], year,
                             title, category, sense_ids[i], f'Sense {i+1} ({pos})']
                    data_matrix.append(entry)

    return pd.DataFrame(data_matrix, columns=['counts', 'year', 'source', 'category', 'sense', 'sense_and_pos'])


def sanitize_category(category):
    category = category.split('_')

    text_list = []
    for text in category:
        text_list.append(text.capitalize())

    return ' '.join(text_list)
