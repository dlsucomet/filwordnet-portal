with open('../static/data/final_network_filtered.graphml', encoding='utf-8') as network, open('../static/data/edge_list.tsv', 'a', encoding='utf-8') as edge_list:
    for idx, line in enumerate(network):
        line = line.strip()
        if line.startswith('<edge source='):
            info = line.split(' ')
            source = info[1][len('source="'): -len('"')]
            target = info[2][len('target="'): -len('">')]

            edge_list.write(source + '\t' + target + '\n')


# <edge source="n6508" target="n19480">
