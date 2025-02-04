import json
import os
import csv
from datasets import load_from_disk
from fuzzywuzzy import fuzz
import joblib
from sklearn_crfsuite.metrics import *
import re
from collections import Counter


def write_file(path, data):
    if path.endswith('.jsonl'):
        with open(path, 'w', encoding='utf-8') as f:
            for item in data:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
        return
    
    if path.endswith('.csv'):
        # Assuming data is a list of dictionaries for CSV
        with open(path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        return

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def read_file(path):
    if path.endswith('.csv'):
        with open(path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)  # Reads each row as a dictionary
            return [row for row in reader]
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_path(file_dir: list):
    """
    Gets absolute path of file

    Args:
        a (list of array): File path

    Returns:
        string of path

    Example:
        >>> get_path(["data", "superbalita-articles-20241109-052649.json"])
        /Users/jhoannaricalagumbay/School/cebqa/data/superbalita-articles-20241109-052649.json
    """
    script_dir = os.path.dirname(os.path.realpath(__file__))
    
    return os.path.join(script_dir, *file_dir)

def get_dataset(dataset_path = get_path(["dataset", "cebquad"])):
    return load_from_disk(dataset_path)


def fuzzy_match(string1, string2_array, threshold=90):
    """
    Compares a string (string1) against an array of strings (string2_array) 
    and returns a list of matches based on fuzzywuzzy with a score above the threshold.

    :param string1: The string to compare
    :param string2_array: List of strings to compare against
    :param threshold: Minimum similarity score for a match (default is 80)
    :return: List of tuples containing matching string and score if match found
    """
    # Convert string1 to lowercase for case-insensitive matching
    string1 = string1.lower()

    matches = []

    # Iterate through each string in string2_array
    for string2 in string2_array:
        # Convert string2 to lowercase
        string2 = string2.lower()

        # Get the similarity score
        score = fuzz.partial_ratio(string1, string2)

        # If the score is above the threshold, add it to the matches
        if score >= threshold:
            matches.append((string2, score))

    return matches

def most_frequent_string(strings):
    counter = Counter(strings)  # Count occurrences of each string
    most_common = counter.most_common(1)  # Get the most common string
    return most_common[0][0] if most_common else None  # Return the string


class NER:
    model_path = get_path(["pseudonymizer", "CebuaNER"])
    cebtenten_path = get_path(["pseudonymizer", "cebtenten.tsv"])
    crf = joblib.load(model_path)

    def __init__(self):
        self.word2cluster = self.read_clusters(cluster_file=self.cebtenten_path)

    def read_clusters(self, cluster_file):
        print(f"cluster file {cluster_file}")
        word2cluster = {}
        with open(cluster_file, encoding = "utf8") as i:
            for line in i:
                word, cluster = line.strip().split('\t')
                word2cluster[word] = cluster
        return word2cluster
    
    def word2features(self, sent, i):
        word = sent[i]

        postag = "-X-"
        features = [
            'bias',
            'word.lower=' + word.lower(),
            'word[-3:]=' + word[-3:],
            'word[-2:]=' + word[-2:],
            'word.isupper=%s' % word.isupper(),
            'word.istitle=%s' % word.istitle(),
            'word.isdigit=%s' % word.isdigit(),
            'word.cluster=%s' % self.word2cluster[word.lower()] if word.lower() in self.word2cluster else "0",
            'postag=' + postag
        ]
        if i > 0:
            word1 = sent[i-1]
            postag1 = "-X-"
            features.extend([
                '-1:word.lower=' + word1.lower(),
                '-1:word.istitle=%s' % word1.istitle(),
                '-1:word.isupper=%s' % word1.isupper(),
                '-1:postag=' + postag1
            ])
        else:
            features.append('BOS')

        if i > 1: 
            word2 = sent[i-2]
            postag2 = "-X-"
            features.extend([
                '-2:word.lower=' + word2.lower(),
                '-2:word.istitle=%s' % word2.istitle(),
                '-2:word.isupper=%s' % word2.isupper(),
                '-2:postag=' + postag2
            ])        

            
        if i < len(sent)-1:
            word1 = sent[i+1]
            postag1 = "-X-"
            features.extend([
                '+1:word.lower=' + word1.lower(),
                '+1:word.istitle=%s' % word1.istitle(),
                '+1:word.isupper=%s' % word1.isupper(),
                '+1:postag=' + postag1
            ])
        else:
            features.append('EOS')

        if i < len(sent)-2:
            word2 = sent[i+2]
            postag2 = "-X-"
            features.extend([
                '+2:word.lower=' + word2.lower(),
                '+2:word.istitle=%s' % word2.istitle(),
                '+2:word.isupper=%s' % word2.isupper(),
                '+2:postag=' + postag2
            ])

            
        return features



    def sent2features(self, sent):
        return [self.word2features(sent, i) for i in range(len(sent))]

    def sent2labels(self, sent):
        return [label for token, postag, label in sent]

    def sent2tokens(self, sent):
        return [token for token in sent]

    def tokenize(self, sentence):
        tokens = re.findall(r'\w+(?:-\w+)*|[^\w\s]', sentence, re.UNICODE)
        return tokens
    
    def get_prediction(self, sentence):
        tokenize_sentence = self.tokenize(sentence)

        pred = self.crf.predict([self.sent2features(tokenize_sentence)])
        print(pred)
        return [item.split("-")[1] for item in pred[0] if item != 'O']


    def get_person_names(self, sentence, stop_words = []):
        tokenize_sentence = self.tokenize(sentence)

        pred = self.crf.predict([self.sent2features(tokenize_sentence)])
        print(pred)
        return [tokenize_sentence[i] for i in range(len(pred[0])) if "PER" in pred[0][i] and tokenize_sentence[i].lower() not in stop_words]

    def mark_name(self, name, type):
        print(name, type)