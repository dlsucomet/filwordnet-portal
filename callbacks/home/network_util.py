import json


def parse_json_communities(word, idx):
    with open('static/data/wsi_comms_lm_v1.json') as f:
        communities = json.load(f)
        for entry in communities:
            if entry['ego'] == word:
                return entry['community'][idx]['context_words']
