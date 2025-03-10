"""
Login in huggingface: `huggingface-cli login`
Create repository in huggingface: `huggingface-cli repo create cebquad --type dataset`

"""

from huggingface_hub import HfApi
from utils import *
# Path to your saved dataset folder
dataset_folder = get_path(["dataset", "cebquad"])

# Your repository ID on Hugging Face
repo_id = "jhoannarica/cebquad"

# Initialize API
api = HfApi()

# Upload your dataset directory
api.upload_folder(
    folder_path=dataset_folder,
    repo_id=repo_id,
    repo_type="dataset"
)
