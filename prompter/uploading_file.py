from openai import OpenAI
from utils import *

# https://platform.openai.com/docs/api-reference/files/create
# https://platform.openai.com/docs/guides/batch

client = OpenAI()

# batch_input_file = client.files.create(
#   file=open(get_path(["prompter", "batch-request-8-50.jsonl"]), "rb"),
#   purpose="batch"
# )

# FileObject(id='file-SG83Pb8aXAgdD25pd30mDC29', bytes=306660, created_at=1731742388, filename='batch-request-8-50.jsonl', object='file', purpose='batch', status='processed', status_details=None)

#  https://api.openai.com/v1/files/file-SG83Pb8aXAgdD25pd30mDC29

# batch_input_file_id = batch_input_file.id

# print(f"\n\n{batch_input_file_id}")

# batch_request = client.batches.create(
#     input_file_id=batch_input_file_id,
#     endpoint="/v1/chat/completions",
#     completion_window="24h",
#     metadata={
#       "description": "CebQA dataset generation "
#     }
# )

# print(f"\n\nbatch_request\n\n")
# print(batch_request)

# batch_status = client.batches.retrieve(batch_request.id)
# batch_status = client.batches.retrieve("batch_67384ce7ef78819099fe7c0635813788")

# print(batch_status)

file_response = client.files.content("file-4CwEkCFNEbdx05CLsZ5I8wKq")
print(file_response.text)