from ..api_query import *


def get_num_senses(API_URL, word):
    return len(get_netsci_word(API_URL, word))


def get_num_nlp_senses(API_URL, word):
    return len(get_nlp_word(API_URL, word))
