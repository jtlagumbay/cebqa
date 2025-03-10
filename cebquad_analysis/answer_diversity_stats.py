from utils import *

data = read_file(get_path(["cebquad_analysis", "answer_diversity-20250204-233450-f.json"]))

type_counts = Counter(item["type"] for item in data)
# Sorting bars by count (optional)
sorted_types = sorted(type_counts.items(), key=lambda x: x[1], reverse=True)
labels, values = zip(*sorted_types)
print(labels)
print(values)

plot_horizontal_bar_chart(labels, values, "Frequency", "Answer Type", "Answer Diversity (n=300)")

# article_labels = ["Articles with Questions", "Articles Used for Testing", "Articles with No Questions"]
# article_values = [1673, 21, 6]

# # plot_pie_chart(article_labels, article_values, "Distribution of Article Collected")

# questions_labels = ["Usable Questions", "Unusable Questions" ]
# question_values = [27629, 397]
# # plot_pie_chart(questions_labels, question_values, "Usable Questions")

# dataset_label = ["train", "test", "development"]
# dataset_value = [19340, 5526, 2763]
# plot_pie_chart(dataset_label, dataset_value, "Dataset Split")