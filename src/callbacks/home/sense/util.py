import re

EXPLETIVES = ['puta',
              'walang hiya'
              'tae',
              'taena',
              'punyeta',
              'gago',
              'shit',
              'shet',
              'fuck',
              'pakyu',
              'bwisit',
              'bwiset',
              'leche',
              'letse',
              'hayop',
              'tarantado']


def sanitize_sample_sentences(example_sentence):
    # data = df.loc[index, 'example_sentences']
    data = example_sentence.strip()[1:-1]
    # data = data.replace("'", '"')
    # data = re.findall('"[A-Z][^"]*"', data)
    regex1 = "'[\w]+[^']*'"
    regex2 = '"[\w]+[^"]*"'
    regex = f'{regex1}|{regex2}'
    data = re.findall(regex, data)
    data = [f'{x[1:-1]}' for x in data]

    return data


def sanitize_pos(pos):
    pos_dict = {
        'NN': 'Noun',
        'VB': 'Verb'
    }

    if pos:
        if pos in pos_dict:
            return pos, pos_dict[pos]
        else:
            return pos, ''

    return '', ''


def display_pos(pos):
    pos_abbrev, pos_fullname = sanitize_pos(pos)
    if pos_fullname and pos_abbrev:
        return f'{pos_fullname} ({pos_abbrev})'

    return None


def is_tweet(sentence):
    return 'XX_USERNAME' in sentence


def has_expletive(sentence):
    for word in EXPLETIVES:
        if word in sentence:
            return True

    return False


def is_quality_sentence(sentence):
    return not is_tweet(sentence) and not has_expletive(sentence)
