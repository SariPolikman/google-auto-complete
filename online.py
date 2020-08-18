import json
import numpy as np
import offline
from auto_complete_data import AutoCompleteData
from init_search_data import trie

k = 5  # num of completions
losses_points = np.array([0, -1, -2, -3, -4, -5, -6, -8, -10])  # list of scores to release


def clean_str(string):
    _clean_str = ''.join(c for c in string if c.isalnum()).lower()

    return _clean_str


def init_auto_complete_data(auto):
    auto_complete_data = []

    for a in auto:
        auto_complete_data.append(AutoCompleteData(a[0], a[1], a[2], a[3]))
    return auto_complete_data


def read_sent_path_file():
    the_file = open('sent_path.json')
    data = json.load(the_file)
    the_file.close()

    return data


def get_source_sentence_and_path(index):
    data = read_sent_path_file()
    source_sentence, path = data[str(index)][0], data[str(index)][1]

    return source_sentence, path


def get_index_offset_pair(sentences_offsets):
    for index_sentence, offset in sentences_offsets.items():
        yield index_sentence, offset


def init_list_auto(sentences_offsets_pairs, score):
    _list = []
    for index, offset in get_index_offset_pair(sentences_offsets_pairs):
        source_sentence, path = get_source_sentence_and_path(index)

        _list.append([source_sentence, path, offset, score])

    return _list


def get_basic_score(text):
    return len(text) * 2


def get_sentences_by_score(sentences):
    for score in losses_points:
        yield {i: j for i, j in sentences[score].items()}, score


def get_best_k_completions(text):
    sentences = offline.search(trie, text)  # [{"index of sentence": offset},{i...: offset }... ]

    if not sentences:  # no match
        return []

    auto_data = []
    for sentence_offset_pair, loss_points in get_sentences_by_score(sentences):
        auto_data += init_list_auto(sentence_offset_pair, loss_points + get_basic_score(text))

        if len(auto_data) >= k:
            break

    return init_auto_complete_data(auto_data)


def print_k_match_sentences(auto):
    for i in auto:
        i.print_auto()


def main():
    while True:
        text = input("ready,Enter your text:")

        if not text:
            continue

        auto = get_best_k_completions(clean_str(text))
        print_k_match_sentences(auto)
        while text[-1] != '#':
            text += input(text)
            auto = get_best_k_completions(clean_str(text))
            print_k_match_sentences(auto)


if __name__ == '__main__':
    main()
