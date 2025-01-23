from openai import OpenAI
from utils import *
from datetime import datetime

import json
import time
import sys
import argparse



client = OpenAI()

def upload_file(file):
    print(f"\nUploading file to OpenAI\n")

    return client.files.create(
      file=open(get_path(["prompter", file]), "rb"),
      purpose="batch"
    )

def create_batch_request(file_id):
    print(f"\nCreating batch request\n")
    return client.batches.create(
        input_file_id = file_id,
        endpoint = "/v1/chat/completions",
        completion_window = "24h",
        metadata = {
          "description": "CebQA dataset generation "
        }
    )

def retrieve_batch_status(batch_id):
    print(f"\nRetrieving batch status\n")
    return client.batches.retrieve(batch_id)

def retrieve_result_content(file_id, start, end):
    print(f"\nRetrieve result content\n")
    file_response = client.files.content(file_id)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    lines = file_response.text.splitlines()
    write_file(get_path(["prompter", f"qa-article-{start}-{end}-{timestamp}.json"]), [json.loads(line) for line in lines])


def list_of_all_batches():
    return client.batches.list()

# batch_requests_jsonl = [
#     "batch-request-21-300.jsonl",
#     "batch-request-301-600.jsonl",
#     "batch-request-601-900.jsonl",
#     "batch-request-901-1200.jsonl",
#     "batch-request-1201-1500.jsonl",
#     "batch-request-1501-1701.jsonl",
# ]

batch_requests_jsonl = [
    "batch-request-4o-330-350.jsonl",
    "batch-request-4o-350-500.jsonl",
    "batch-request-4o-500-800.jsonl",
    "batch-request-4o-800-1100.jsonl",
    "batch-request-4o-1100-1400.jsonl",
    "batch-request-4o-1400-1710.jsonl"
]
batch_requests_status_file = "batch-requests-status-4o.json"
batch_requests_status = read_file(get_path(["prompter", batch_requests_status_file]))

TODO = "todo"
ONGOING = "ongoing"
DONE = "done"
ERROR = "error"

updated_batch_requests_status = []

# Print all batch_requests:
print(f"\n{list_of_all_batches()}\n")
try:
    # Process file upload or process ongoing
    for batch in batch_requests_status["data"]:

        if not batch["uploaded_input_file"]:    
            print(f"\nProcessing {batch["batch_input_file"]}")
            file = upload_file(batch["batch_input_file"])
            print(f"Uploaded: {file.id}")
            batch["uploaded_input_file"] = file.id

        if batch["request_status"] == ONGOING:
            print(f"\nProcessing {ONGOING} batch: {batch["batch_input_file"]}")
            batch_result = retrieve_batch_status(batch["batch_request_id"])
            print(batch_result)
            if batch_result.status == "completed":
                batch["request_status"] = DONE
            if batch_result.status == "failed" or batch_result.status == "expired": 
                batch["request_status"] = ERROR
        
        updated_batch_requests_status.append(batch)

    # If no ongoing process, process first to do
    if not any(obj.get("request_status") == ONGOING for obj in updated_batch_requests_status):
        index, first_todo = next(
            ((i, obj) for i, obj in enumerate(updated_batch_requests_status) if obj.get("request_status") == TODO),
            (None, None)
        )
        if first_todo:
            print(f"\nProcessing {TODO} batch: {first_todo["batch_input_file"]}")
            batch_request = create_batch_request(first_todo["uploaded_input_file"])
            print(f"\nCreated batch request: {batch_request}")
            updated_batch_requests_status[index]["batch_request_id"] = batch_request.id
            updated_batch_requests_status[index]["request_status"] = ONGOING

    request_json = {
        "last_updated": datetime.now().isoformat(), 
        "data": updated_batch_requests_status
    }

    write_file(get_path(["prompter", batch_requests_status_file]), request_json)
    print("done")
except Exception as error:
    print(error)

