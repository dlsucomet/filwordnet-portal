with open('../static/data/final_network_filtered.graphml', encoding='utf-8') as network, open('../static/data/node2word.tsv', 'w', encoding='utf-8') as node2word:
    for idx, line in enumerate(network):
        line = line.strip()
        if line.startswith('<node id='):
            id = line.split('=')[1][1: -len('">')]
            node2word.write(id + '\t')
        elif line.startswith('<data key="v_word">'):
            word = line[len('<data key="v_word">'): -len("</data>")]
            node2word.write(word + '\n')
