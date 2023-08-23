import pandas as pd
import re
from ..sense.util import *


def convert_to_data_by_sense(contextual_info, sense_ids, pos_list):
    data_matrix = []
    for i in range(0, len(contextual_info)):
        sources = contextual_info[i]
        for categories in sources:
            for title in sources[categories]:
                if title != 'twitter':
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
