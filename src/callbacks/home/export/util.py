from ..api_query import *


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
