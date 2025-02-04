from utils import *

data = read_file(get_path(["cebquad_analysis", "answer_diversity-20250204-233450-f.json"]))

type_counts = Counter(item["type"] for item in data)

print(type_counts)