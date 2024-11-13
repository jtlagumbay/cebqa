import json
import os
import sys

from utils import *

script_dir = os.path.dirname(os.path.realpath(__file__))
person_names_path = os.path.join(script_dir, 'person_names.json')
person_names_filtered_path = os.path.join(script_dir, 'person_names_filtered.json')
stop_words_path = os.path.join(script_dir, 'stop_words.json')

person_names = []
persons = []

stop_words = read_file(stop_words_path)

person_names = read_file(person_names_path)

for name in person_names:
    print(name)
    if name not in stop_words \
    and len(name) > 2 \
    and not any(char.isdigit() for char in name) \
    and name not in persons:
        print("include")
        persons.append(name)
        

write_file(person_names_filtered_path, persons)