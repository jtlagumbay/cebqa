from openai import OpenAI
from utils import *
import json
import time
# https://platform.openai.com/docs/api-reference/files/create
# https://platform.openai.com/docs/guides/batch

client = OpenAI()

# ## UPLOADING FILE
# print("Uploading file to OpenAI")
# batch_input_file = client.files.create(
#   file=open(get_path(["prompter", "batch-request-9-20.jsonl"]), "rb"),
#   purpose="batch"
# )

# FileObject(id='file-SG83Pb8aXAgdD25pd30mDC29', bytes=306660, created_at=1731742388, filename='batch-request-8-50.jsonl', object='file', purpose='batch', status='processed', status_details=None)
#  https://api.openai.com/v1/files/file-SG83Pb8aXAgdD25pd30mDC29

# batch_input_file_id = batch_input_file.id
# print(f"\n\n{batch_input_file_id}")

## CREATE BATCH REQUEST

# print(f"\n\nCreating batch request\n\n")
# batch_request = client.batches.create(
#     input_file_id=batch_input_file_id,
#     endpoint="/v1/chat/completions",
#     completion_window="24h",
#     metadata={
#       "description": "CebQA dataset generation "
#     }
# )

# print(batch_request)

## CHECKING BATCH STATUS
# print("Checking batch status")
# batch_status = client.batches.retrieve("batch_67398341a66081908debc589bd4d3a1f")
# batch_status = client.batches.retrieve("batch_673997e37b508190a6270b0a285d740c")

# print(batch_status)

## RETRIEVING RESULT CONTENT
file_response = client.files.content("file-fy0aksLxaJINj9mjAdcIFo6N")
# print(file_response.text)
timestamp = time.strftime("%Y%m%d-%H%M%S")
lines = file_response.text.splitlines()

write_file(get_path(["prompter", f"qa-article-9-20-{timestamp}.json"]), [json.loads(line) for line in lines])


# 11-17 13:47
# Batch(id='batch_67398341a66081908debc589bd4d3a1f', completion_window='24h', created_at=1731822401, endpoint='/v1/chat/completions', input_file_id='file-GUoIhU3bdHtTmVW1SrQGN95W', object='batch', status='validating', cancelled_at=None, cancelling_at=None, completed_at=None, error_file_id=None, errors=None, expired_at=None, expires_at=1731908801, failed_at=None, finalizing_at=None, in_progress_at=None, metadata={'description': 'CebQA dataset generation '}, output_file_id=None, request_counts=BatchRequestCounts(completed=0, failed=0, total=0))

# 11-17 15:!4
# Batch(id='batch_673997e37b508190a6270b0a285d740c', completion_window='24h', created_at=1731827683, endpoint='/v1/chat/completions', input_file_id='file-AFnNG7FHwUqRVbaGAkc9jX2T', object='batch', status='validating', cancelled_at=None, cancelling_at=None, completed_at=None, error_file_id=None, errors=None, expired_at=None, expires_at=1731914083, failed_at=None, finalizing_at=None, in_progress_at=None, metadata={'description': 'CebQA dataset generation '}, output_file_id=None, request_counts=BatchRequestCounts(completed=0, failed=0, total=0))