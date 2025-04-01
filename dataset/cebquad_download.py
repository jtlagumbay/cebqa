# Downloads cebquad files to csv
from datasets import load_dataset


dataset = load_dataset("jhoannarica/cebquad")

# Convert and save each split (train, validation, test) to CSV
dataset['train'].to_csv('train.csv')
dataset['validation'].to_csv('val.csv')
dataset['test'].to_csv('test.csv')

