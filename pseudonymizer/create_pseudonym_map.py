from utils import *

GIVEN_NAME_MALE = 0 # 1131
GIVEN_NAME_FEMALE = 1 # 684
SURNAME_OTHER = 2 # 2395
SURNAME_CH = 3 # 25
SURNAME_MORO = 4 # 9
NOT_NAME = 5 # 261
GIVEN_NAME_EITHER = 6 # 0

# Combine to one
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
print(name_cat)

# print([key for key, value in name_cat.items() if value == 2])
for key, value in name_cat.items():
    if value == 2:
        print(key)


