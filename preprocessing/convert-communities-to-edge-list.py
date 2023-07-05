import json
import os


def get_community(word, idx):
    with open('../static/data/wsi_comms_lm_v1.json') as f:
        communities = json.load(f)
        for entry in communities:
            if entry['ego'] == word:
                return entry['community'][idx]['context_words']


def convert_community_to_edge_list(word, idx, community):
    community = set(community)

    if not os.path.exists(f'../static/data/{word}'):
        os.makedirs(f'../static/data/{word}')

    with open('../static/data/edge_list.tsv', encoding='utf-8') as edge_list, open(f'../static/data/{word}/{idx}.tsv', 'w', encoding='utf-8') as comm2edge:
        for edge in edge_list:
            edge = edge.strip()
            node1, node2 = edge.split('\t')

            if (node1 in community or node1 == word) and (node2 in community or node2 == word):
                comm2edge.write(f'{node1}\t{node2}\n')


def convert_communities_to_edge_list(word):
    with open('../static/data/wsi_comms_lm_v1.json') as f:
        communities = json.load(f)
        for entry in communities:
            if entry['ego'] == word:
                idx = 0
                while True:
                    try:
                        community = get_community(word, idx)
                        convert_community_to_edge_list(word, idx, community)
                        idx += 1
                    except IndexError:
                        break

                break


if __name__ == '__main__':
    convert_communities_to_edge_list('tuldok')
