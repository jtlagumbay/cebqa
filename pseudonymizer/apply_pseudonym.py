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

    # Prepare NER Model
    script_dir = os.path.dirname(os.path.realpath(__file__))
    data_dir = os.path.join(script_dir, '..', 'data')
    model_path = os.path.join(script_dir, 'CebuaNER')
    cebtenten_path = os.path.join(script_dir, 'cebtenten.tsv')
    crf = joblib.load(model_path)
    word2cluster = read_clusters(cebtenten_path)

    # Get stop words (Words that are tagged as person but should not be)
    stop_words = read_file(get_path(["data", 'stop_words.json']))
    stop_words = list(set([word.lower() for word in stop_words]))

    # Get articles dataset
    articles = read_file(get_path(["data", 'superbalita-articles-20241109-052649.json']))

    # Get pseudonym map
    pseudonym_map = read_file(get_path(["data", "pseudonyms-20241116-091919.json"]))
   
    # List of pseudonymized articles
    pseudonymized_articles = []

    # Error names
    error_names = []
    for i, article in enumerate(articles):
        # if article["id"] != 1566:
        #     continue
        print(f"Processing {article["id"]}, {article["title"]}")
        body = article["body"]
        persons = get_person_names(body, stop_words)
        if persons:
            for person in persons:
                pseudonym = [obj for obj in pseudonym_map if obj.get("original").lower() == person.lower()]
                if pseudonym:
                    new_name = pseudonym[0]['new']
                    body = body.replace(person, new_name.capitalize())
                elif "-" in person:
                    hyphenated_surnames = person.split("-")
                    for name in hyphenated_surnames:
                        pseudonym = [obj for obj in pseudonym_map if obj.get("original").lower() == name.lower()]
                        if pseudonym:
                            new_name = pseudonym[0]['new']
                            body = body.replace(name, new_name.capitalize())
                else:
                    print(f"No Pseudonym found: {article["id"]}: {person}")
                    error_names.append({
                        'article_id': article["id"],
                        'name': person
                    })
                    continue
        article["pseudonymized_body"] = body
        pseudonymized_articles.append(article)
    
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    write_file(get_path(["pseudonymizer", f"pseudonymized_articles-{timestamp}"]), pseudonymized_articles)
    write_file(get_path(["pseudonymizer", f"error_names-{timestamp}"]), error_names)
    

