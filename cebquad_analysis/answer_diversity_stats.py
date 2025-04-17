from utils import *
from datasets import load_dataset

# Login using e.g. `huggingface-cli login` to access this dataset
# ds = load_dataset("jhoannarica/superbalita_split")
# ds = load_dataset("jhoannarica/cebquad_split")
# print(ds)
# data = read_file(get_path(["cebquad_analysis", "answer_diversity-20250204-233450-f.json"]))

# type_counts = Counter(item["type"] for item in data)
# # Sorting bars by count (optional)
# sorted_types = sorted(type_counts.items(), key=lambda x: x[1], reverse=True)
# labels, values = zip(*sorted_types)
# print(labels)
# print(values)

# plot_horizontal_bar_chart(labels, values, "Frequency", "Answer Type", "Answer Diversity (n=300)")

# article_labels = ["Articles with Questions", "Articles Used for Testing", "Articles with No Questions"]
# article_values = [1673, 21, 6]

# # plot_pie_chart(article_labels, article_values, "Distribution of Article Collected")

# questions_labels = ["Usable Questions", "Unusable Questions" ]
# question_values = [27629, 397]
# # plot_pie_chart(questions_labels, question_values, "Usable Questions")

# dataset_label = ["train", "test", "validation"]
# dataset_value = [19300, 5597, 2732]
# plot_pie_chart(dataset_label, dataset_value, "CebQuAD Split")

ds = load_dataset("jhoannarica/cebquad_split")

# ds = load_dataset("jhoannarica/superbalita_split")

# Function to compute average word count for a split
def compute_word_counts(split):
    return [len(example["answer"].split()) for example in split if example["answer"] ]

# Get word counts for each split
train_word_counts = compute_word_counts(ds["train"])
test_word_counts = compute_word_counts(ds["test"])
validation_word_counts = compute_word_counts(ds["validation"])

# Compute averages separately
avg_train = sum(train_word_counts) / len(train_word_counts)
avg_test = sum(test_word_counts) / len(test_word_counts)
avg_validation = sum(validation_word_counts) / len(validation_word_counts)

# Compute overall average
all_word_counts = train_word_counts + test_word_counts + validation_word_counts
overall_avg = sum(all_word_counts) / len(all_word_counts)

# Print results
print(f"Average word count:")
print(f"Train: {avg_train:.2f}")
print(f"Test: {avg_test:.2f}")
print(f"Validation: {avg_validation:.2f}")
print(f"Overall: {overall_avg:.2f}")