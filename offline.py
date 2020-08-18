import json
from auto_complete_data import AutoCompleteData
import os

path = './a'


def clean_str(string):
    clean_str = ''.join(c for c in string if c.isalnum()).lower()
    return clean_str


def walk_in_file_tree():
    for root, dirs, files in os.walk(path):
        for file in files:
            data = open(os.path.join(root, file), "r")
            yield data, file


def upload_sent_path_file(list_auto_complete):
    json_object = json.dumps(list_auto_complete)

    with open("sent_path.json", "w") as sent_path:
        sent_path.write(json_object)


def init_trie(_dict):
    list_auto_complete = {}

    for file, file_name in walk_in_file_tree():
        lines = file.readlines()

        for index_sent, line in enumerate(lines):
            list_auto_complete[index_sent] = [str(line), file_name]
            _dict = insert_line(line, _dict, index_sent)


def get_five_fit_sent_from_file(_dict):
    list_auto_complete = {}
    index_sent = 0

    for file, file_name in walk_in_file_tree():
        lines = file.readlines()

        for line in lines:
            clean_line = clean_str(line)
            if clean_line:
                list_auto_complete[index_sent] = [str(line), str(file_name)]
                clean_line = clean_str(line)

                _dict = insert_line(clean_line, _dict, index_sent)

            index_sent += 1

    upload_sent_path_file(list_auto_complete)


def char_to_index(ch):  # TODO nicely
    return ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l'
        , 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w'
        , 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'].index(ch)
    # if ch.isdigit():
    #     # return int(ch)
    #     return ord(ch) - ord('0') + ord('z')
    # return ord(ch) - ord('a')


def init_node():
    self = [[None] * 36, {0: {}, -1: {}, -2: {}, -3: {}, -4: {}, -5: {}, -6: {}, -8: {},
                          -10: {}}]  # first for the highest score etc.
    return self


def insert(node, sub_line, index_sentence, offset):
    node = node[0]

    prev_node = None  # from forget letter, how lose?
    prev_letter = None

    for index, letter in enumerate(sub_line):  # TODO
        letter_index = char_to_index(letter)

        if not node[letter_index]:
            node[letter_index] = init_node()
        if len(node[letter_index][1][0]) < 5:  # for opt space
            node[letter_index][1][0][index_sentence] = offset

            for idx, ch in enumerate(node):

                if not ch:
                    node[idx] = init_node()
                score = -1 if index - 5 >= 0 else index - 5
                if len(node[idx][1][score]) < 5:
                    node[idx][1][score][index_sentence] = offset

        node = node[letter_index][0]


def insert_line(clean_line, _dict, index_sent):
    for i in range(len(clean_line)):  # TODO why + 1
        sub_line = clean_line[i:]
        insert(_dict, sub_line, index_sent, i)
    return _dict


def init_trie(self):
    get_five_fit_sent_from_file(self)


def search(self, sub_line):
    node = self[0]
    tmp = []
    for letter in sub_line:
        letter_index = char_to_index(letter)

        if not node[letter_index]:
            return {}

        tmp = node[letter_index][1]
        node = node[letter_index][0]

    return tmp
