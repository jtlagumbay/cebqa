from utils import *
from fuzzywuzzy import fuzz
import re
import time

dataset = get_dataset()

# Shuffle the "dev" split and select the first 300 rows
sampled_dev = dataset["dev"].shuffle(seed=42).select(range(300))

# Print the sampled rows
print(sampled_dev)

DATE_TIME = "DATE_TIME"
NUMERIC = "NUMERIC"
PERSON = "PERSON"
LOCATION = "LOCATION"
OTHER_ENTITY = "OTHER_ENTITY"
NOUN = "NOUN"
ADJ = "ADJ"
VERB = "VERB"
OTHERS = "OTHERS"

months = ["enero", "pebrero", "marso", "abril", "mayo", "hunyo", "hulyo", "agosto", "septembre", "oktobre", "nobyembre", "disyembre", "january", "february", "march", "april", "may", "june", "july", "august", "september", "november", "december"]
days = ["dominggo", "lunes", "martes", "miyerkules", "huwebes", "biyernes", "sabado", "sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
diversity = []
location = ["barangay", "brgy", "sitio", "st.", "dakbayan", "lungsod", "siyudad", "isla", "probinsiya", "munisipyo", "ospital", "hospital", "city", "province", "municipality", "island"]
names_female = read_file(get_path(["data", "females-20241116-085707.json"]))
names_male = read_file(get_path(["data", "males-20241116-085707.json"]))
surnames_other = read_file(get_path(["data", "surnames-20241116-085707.json"]))

all_names = names_female + names_male + surnames_other
all_names = [entry["name"] for entry in all_names]
print(all_names)

for data in sampled_dev:
    print(f"processing {data["id"]}")
    ans = data["answer"]["text"].lower()
    answer_type = ""

    # time
    if "alas" in ans.split() and re.search(r'\d', ans):
        answer_type = DATE_TIME

    elif any(date in ans.split() for date in months + days):
        answer_type = DATE_TIME

    elif re.search(r'\d', ans):
        answer_type =  NUMERIC

    elif any(name in ans.split() for name in all_names):
        answer_type = PERSON
    
    elif "nga" in ans.split():
        answer_type = ADJ
    
    elif any(loc in ans.split() for loc in location):
        answer_type = LOCATION

    ans_div = {
        "id": data["id"],
        "answer": ans,
        "type": answer_type
    }

    diversity.append(ans_div) 


timestamp = time.strftime("%Y%m%d-%H%M%S")

write_file(get_path(["cebquad_analysis", f"answer_diversity-{timestamp}.json"]), diversity)
