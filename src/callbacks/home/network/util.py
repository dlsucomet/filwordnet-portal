from ..api_query import *


def get_num_senses(API_URL, word):
    return len(get_netsci_word(API_URL, word))
