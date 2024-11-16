from utils import *
import time

GIVEN_NAME_MALE = 0 # 1131
GIVEN_NAME_FEMALE = 1 # 684
SURNAME_OTHER = 2 # 2395
SURNAME_CH = 3 # 25
SURNAME_MORO = 4 # 9
NOT_NAME = 5 # 261
GIVEN_NAME_EITHER = 6 # 0

###### Combine to one
# cat1 = read_file(get_path(["pseudonymizer", "person_cat-0-500-20241113-094548"]))
# cat2 = read_file(get_path(["pseudonymizer", "person_cat-501-1000-20241113-104817"]))
# cat3 = read_file(get_path(["pseudonymizer", "person_cat-1000-1500-20241113-142806"]))
# cat4 = read_file(get_path(["pseudonymizer", "person_cat-1500-2000-20241113-155600"]))
# cat5 = read_file(get_path(["pseudonymizer", "person_cat-2000-2500-20241113-191653"]))
# cat6 = read_file(get_path(["pseudonymizer", "person_cat-2500-3000-20241114-085840"]))
# cat7 = read_file(get_path(["pseudonymizer", "person_cat-3000-3500-20241114-105103"]))
# cat8 = read_file(get_path(["pseudonymizer", "person_cat-3500-4000-20241114-121101"]))
# cat9 = read_file(get_path(["pseudonymizer", "person_cat-4000-4114-20241114-131444"]))
# cat10 = read_file(get_path(["pseudonymizer", "person_cat-4114-4513-20241115-072108"]))
# name_cat = {**cat1, **cat2, **cat3, **cat4, **cat5, **cat6, **cat7, **cat8, **cat9, **cat10}
# write_file(get_path(["data", "name_category.json"]), name_cat)

name_cat = read_file(get_path(["data", "name_category.json"]))
names_female = read_file(get_path(["data", "females-20241116-085707.json"]))
names_male = read_file(get_path(["data", "males-20241116-085707.json"]))
surnames_other = read_file(get_path(["data", "surnames-20241116-085707.json"]))
# stop_words = read_file(get_path(["data", "stop_words.json"]))
# stop_words = read_file(get_path(["daata", "stop_words.json"]))
# surnames_chinese = read_file(get_path(["data", "surnames_chinese.csv"]))
# surnames_moro = read_file(get_path(["data", "surnames_moro.csv"]))


pseudonym_map = []
new_stop_words = []
error_names = []
###### Get name per category
# for key, value in name_cat.items():
#     if value == 1:
#         print(key)

# Iterate each name in name_cat
print(f"Starting {len(name_cat)} names")
for index, (name, cat) in enumerate(name_cat.items()):
    print(f"{index} Processing {cat}: {name}")
    new_name = ""
    # if index >= 5:
    #     break
    if cat == GIVEN_NAME_MALE:
        for i, name_male in enumerate (names_male):
            if name_male["used"] == '0' and name != name_male["name"]:
                new_name = name_male["name"]
                names_male[i]["used"] = 1
                break
        else:
            print("All male names are used")
    elif cat == GIVEN_NAME_FEMALE:
        for i, name_female in enumerate (names_female):
            if name_female["used"] == '0' and name != name_female["name"]:
                new_name = name_female["name"]
                names_female[i]["used"] = 1
                break
        else:
            print("All female names are used")
    elif cat == SURNAME_OTHER or cat == SURNAME_CH or cat == SURNAME_MORO:
        for i, surname_other in enumerate (surnames_other):
            if surname_other["used"] == '0' and name != surname_other["name"]:
                new_name = surname_other["name"]
                surnames_other[i]["used"] = 1
                break
        else:
            print("All surnames are used")
    elif cat == NOT_NAME:
        new_stop_words.append(name)
    else:
        error_names.append(name)

    if cat != NOT_NAME:
        pseudo = {
            "id": len(pseudonym_map),
            "original": name,
            "category": cat,
            "new": new_name
        }
        pseudonym_map.append(pseudo)

timestamp = time.strftime("%Y%m%d-%H%M%S")
write_file(get_path(["pseudonymizer", f"pseudonyms-{timestamp}.json"]), pseudonym_map)
write_file(get_path(["pseudonymizer", f"new_stop_words-{timestamp}.json"]), new_stop_words)
write_file(get_path(["pseudonymizer", f"error_names-{timestamp}.json"]), error_names)
print("done")