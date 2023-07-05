import pickle

with open('../static/data/node2word.tsv', encoding='utf-8') as node2word, open('../static/data/node2word.pickle', 'wb') as node2word_pickle:
    node2word_dict = {}
    for line in node2word:
        line = line.strip()
        id, word = line.split('\t')

        node2word_dict[id] = word

    pickle.dump(node2word_dict, node2word_pickle, pickle.HIGHEST_PROTOCOL)
