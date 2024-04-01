import json
import os
from collections import defaultdict
from math import log
import string
import pickle


def update_url_scores(old: dict[str, float], new: dict[str, float]):
    for url, score in new.items():
        if url in old:
            old[url] += score
        else:
            old[url] = score
    return old


def normalize_string(input_string: str) -> str:
    translation_table = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
    string_without_punc = input_string.translate(translation_table)
    string_without_double_spaces = ' '.join(string_without_punc.split())
    return string_without_double_spaces.lower()


def default_dict_int():
    return defaultdict(int)


class SearchEngine:
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self._index: dict[str, dict[str, int]] = defaultdict(default_dict_int)
        self._documents: dict[str, str] = {}
        self.k1 = k1
        self.b = b

    @property
    def posts(self) -> list[str]:
        return list(self._documents.keys())

    @property
    def number_of_documents(self) -> int:
        return len(self._documents)

    @property
    def avdl(self) -> float:
        return sum(len(d) for d in self._documents.values()) / len(self._documents)

    def idf(self, kw: str) -> float:
        N = self.number_of_documents
        n_kw = len(self.get_urls(kw))
        return log((N - n_kw + 0.5) / (n_kw + 0.5) + 1)

    def bm25(self, kw: str) -> dict[str, float]:
        result = {}
        idf_score = self.idf(kw)
        avdl = self.avdl
        for url, freq in self.get_urls(kw).items():
            numerator = freq * (self.k1 + 1)
            denominator = freq + self.k1 * (
                    1 - self.b + self.b * len(self._documents[url]) / avdl
            )
            result[url] = idf_score * numerator / denominator
        return result

    def search(self, query: str) -> dict[str, float]:
        keywords = normalize_string(query).split(" ")
        url_scores: dict[str, float] = {}
        for kw in keywords:
            kw_urls_score = self.bm25(kw)
            url_scores = update_url_scores(url_scores, kw_urls_score)
        sorted_url_scores = dict(sorted(url_scores.items(), key=lambda item: item[1], reverse=True))
        return sorted_url_scores

    def index(self, url: str, content: str) -> None:
        self._documents[url] = content
        words = normalize_string(content).split(" ")
        for word in words:
            self._index[word][url] += 1

    def bulk_index(self, documents: list[tuple[str, str]]):
        for url, content in documents:
            self.index(url, content)

    def get_urls(self, keyword: str) -> dict[str, int]:
        keyword = normalize_string(keyword)
        return self._index[keyword]

    def load_from_json(self, file_path: str):
        with open(file_path, 'r') as file:
            data = json.load(file)
            documents = [(item['url'], item['text']) for item in data]
            self.bulk_index(documents)

    def save_index(self, file_path: str):
        with open(file_path, 'wb') as file:
            pickle.dump((self._index, self._documents), file)

    def load_index(self, file_path: str):
        with open(file_path, 'rb') as file:
            self._index, self._documents = pickle.load(file)


# Example usage
if __name__ == '__main__':
    search_engine = SearchEngine()

    # Load data from all JSON files in a folder and index them
    # folder_path = '/Users/anupkumar/Desktop/POCS/jsons'  # Path to the folder containing JSON files
    # for file_name in os.listdir(folder_path):
    #     if file_name.endswith('.json'):
    #         file_path = os.path.join(folder_path, file_name)
    #         search_engine.load_from_json(file_path)

    # Save the index to a file
    # search_engine.save_index('search_index.pkl')
    # Load the index from the file (this can be done in a separate session)
    search_engine.load_index('search_index.pkl')

    # Perform a search
    results = search_engine.search('startup mindset')
    print(results)

