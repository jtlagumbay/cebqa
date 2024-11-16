import json
import os
import csv

def write_file(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def read_file(path):
    if path.endswith('.csv'):
        with open(path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)  # Reads each row as a dictionary
            return [row for row in reader]
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_path(file_dir: list):
    """
    Gets absolute path of file

    Args:
        a (list of array): File path

    Returns:
        string of path

    Example:
        >>> get_path(["data", "superbalita-articles-20241109-052649.json"])
        /Users/jhoannaricalagumbay/School/cebqa/data/superbalita-articles-20241109-052649.json
    """
    script_dir = os.path.dirname(os.path.realpath(__file__))
    
    return os.path.join(script_dir, *file_dir)