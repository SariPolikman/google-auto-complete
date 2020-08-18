from dataclasses import dataclass


@dataclass
class AutoCompleteData:
    completed_sentence: str
    source_text: str
    offset: int
    score: int
    # methods that you need to define by yourself

    def print_auto(self):
        print(f'{self.completed_sentence} ({self.source_text}) score: {self.score}')


def print_auto(auto):
    print(f'{auto.completed_sentence} ({auto.source_text}) score: {auto.score}')
