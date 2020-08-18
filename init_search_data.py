import json
import offline


def load_search_file():
    the_file = open('search_data.json')
    data = json.load(the_file)
    the_file.close()

    return data


def init_search_data():
    print("loading...")
    trie_ = offline.init_node()
    offline.init_trie(trie_)

    json_object = json.dumps(trie_)  # indent for readability
    with open("search_data.json", "w") as search_data:
        search_data.write(json_object)

    return trie_


trie = init_search_data()


def get_load_search_file():
    trie_ = load_search_file()
    return trie_
