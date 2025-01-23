import joblib
from sklearn_crfsuite.metrics import *
import os
import re
import json
from utils import *
import time
#### Constants
GIVEN_NAME = "Given Name"
SURNAME = "Surname"

###### Functions for NER tagging from CebuaNER
def read_clusters(cluster_file):
    word2cluster = {}
    with open(cluster_file, encoding = "utf8") as i:
        for line in i:
            word, cluster = line.strip().split('\t')
            word2cluster[word] = cluster
    return word2cluster


def word2features(sent, i, word2cluster):
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
        'word.cluster=%s' % word2cluster[word.lower()] if word.lower() in word2cluster else "0",
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


def sent2features(sent, word2cluster):
    return [word2features(sent, i, word2cluster) for i in range(len(sent))]


def sent2tokens(sent):
    return [token for token in sent]

def tokenize(sentence):
    tokens = re.findall(r'\w+(?:-\w+)*|[^\w\s]', sentence, re.UNICODE)
    return tokens

def get_person_names(sentence, stop_words):
    tokenize_sentence = tokenize(sentence)

    pred = crf.predict([sent2features(tokenize_sentence, word2cluster)])

    return [tokenize_sentence[i] for i in range(len(pred[0])) if "PER" in pred[0][i] and tokenize_sentence[i].lower() not in stop_words]

def mark_name(name, type):
    print(name, type)

if __name__ == "__main__":

    script_dir = os.path.dirname(os.path.realpath(__file__))
    data_dir = os.path.join(script_dir, '..', 'data')

    timestamp = time.strftime("%Y%m%d-%H%M%S")

    model_path = os.path.join(script_dir, 'CebuaNER')
    cebtenten_path = os.path.join(script_dir, 'cebtenten.tsv')
    stop_words_path = os.path.join(script_dir, 'stop_words.json')
    person_names_path = os.path.join(script_dir, 'person_names_map.json')
    article_path = os.path.join(data_dir, 'superbalita-articles-20241109-052649.json')



    crf = joblib.load(model_path)
    word2cluster = read_clusters(cebtenten_path)
    stop_words = []

    stop_words = read_file(stop_words_path)

    articles = read_file(article_path)

    person_names = []
    article_error_id = []

    # Ger person names in article

    for article in articles[10:15]:
        print(f"Processing {article["id"]}, {article["title"]}")
        body = article["body"]
        persons = get_person_names(body, stop_words)

        if persons:
            for person in persons:
                if person not in person_names:
                    person_names.append(person)
        else:
            article_error_id.append(article["id"])
            print(f"Error Processing {article["id"]}, {article["title"]}")


    with open(person_names_path, 'w', encoding='utf-8') as f:
        json.dump(person_names, f, ensure_ascii=False, indent=4)
    

    print(f"Error id: {article_error_id}")