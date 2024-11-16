import unicodedata
from utils import * 
import time

def clean_text(text):
    # Normalize accented characters
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    # Replace non-breaking spaces with regular spaces
    text = text.replace('\xa0','').replace(' ','').strip()
    return text

name_cat = read_file(get_path(["data", "name_category.json"]))
names_female = read_file(get_path(["data", "names_female.csv"]))
names_male = read_file(get_path(["data", "names_male.csv"]))
surnames_other = read_file(get_path(["data", "surnames_other.csv"]))

print(len(names_female))
print(len(names_male))
print(len(surnames_other))

cleaned_surnames_other = []
seen_names = set()

for name in surnames_other:
    cleaned_name = clean_text(name["name"])
    if cleaned_name not in seen_names:
        name["name"] = cleaned_name
        cleaned_surnames_other.append(name)
        seen_names.add(cleaned_name)


cleaned_male = []

for name in names_male:
    cleaned_name = clean_text(name["name"])
    if cleaned_name not in seen_names:
        name["name"] = cleaned_name
        cleaned_male.append(name)
        seen_names.add(cleaned_name)


cleaned_female = []

for name in names_female:
    cleaned_name = clean_text(name["name"])
    if cleaned_name not in seen_names:
        name["name"] = cleaned_name
        cleaned_female.append(name)
        seen_names.add(cleaned_name)

timestamp = time.strftime("%Y%m%d-%H%M%S")
write_file(get_path(["pseudonymizer", f"surnames-{timestamp}.json"]), cleaned_surnames_other)
write_file(get_path(["pseudonymizer", f"males-{timestamp}.json"]), cleaned_male)
write_file(get_path(["pseudonymizer", f"females-{timestamp}.json"]), cleaned_female)