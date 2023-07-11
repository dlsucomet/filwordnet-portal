import re


def sanitize_sample_sentences(data, df):
    data = df.loc[data, 'example_sentences']
    data = data.strip()
    data = data[1:]
    data = data[:-1]
    #data = data.replace("'", '"')
    #data = re.findall('"[A-Z][^"]*"', data)
    data = re.findall("'[A-Z][^']*'", data)
    data = [f'"{x[1:-1]}"' for x in data]
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


def display_pos(pos):
    pos_abbrev, pos_fullname = sanitize_pos(pos)
    if pos_fullname and pos_abbrev:
        return f'{pos_fullname} ({pos_abbrev})'

    return None
