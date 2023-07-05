import json


def get_num_communities(word):
    with open('static/data/wsi_comms_lm_v1.json') as f:
        communities = json.load(f)
        for entry in communities:
            if entry['ego'] == word:
                return len(entry['community'])
