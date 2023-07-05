import pickle

with open('../static/data/final_network_filtered.graphml', encoding='utf-8') as network, open('../static/data/edge_list.tsv', 'a', encoding='utf-8') as edge_list, open('../static/data/node2word.pickle', 'rb') as node2word_pickle:
    node2word = pickle.load(node2word_pickle)

    for idx, line in enumerate(network):
        line = line.strip()
        if line.startswith('<edge source='):
            info = line.split(' ')
            source = info[1][len('source="'): -len('"')]
            target = info[2][len('target="'): -len('">')]

            source = node2word[source]
            target = node2word[target]

            edge_list.write(source + '\t' + target + '\n')
