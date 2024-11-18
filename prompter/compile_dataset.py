from utils import *
from openai import OpenAI
import json
import time
import re

client = OpenAI()

def retrieve_result_content(file_id):
    print(f"\nRetrieve result content\n")
    file_response = client.files.content(file_id)
    lines = file_response.text.splitlines()
    return lines

def retrieve_batch_status(batch_id):
    print(f"\nRetrieving batch status\n")
    return client.batches.retrieve(batch_id)

batch_request = read_file(get_path(["prompter", "batch-requests-status.json"]))

qas_dataset = []
error_article = []

for request in batch_request["data"]:
    print(f"\n\nProcessing batch request {request["batch_request_id"]}\n\n")
    
    request_data = []
    article_range = re.search(r'(\d+-\d+)', request["batch_input_file"]).group(1) if re.search(r'(\d+-\d+)', "batch-request-21-300.jsonl") else None
    batch = retrieve_batch_status(request["batch_request_id"])
    outputs = retrieve_result_content(batch.output_file_id)

    # Process output for each article
    for output in outputs:
        try:
            data = json.loads(output)
            request_data.append(data)

            article_id = data["custom_id"].split('-')[1]

            print(f"\nProcessing article {article_id}")

            qas_raw = data["response"]["body"]["choices"][0]["message"]["content"]

            qas_data = json.loads(qas_raw)["data"]

            # Processing each question-answer per article
            for i, qa in enumerate(qas_data):
                qa_id = f"{int(article_id):05}-{(i+1):03}"
                print(f"\tProcessing question {qa_id}")
                
                qa['article_id'] = article_id
                qa['qa_id'] = qa_id
                qas_dataset.append(qa)
        except Exception as e:
            print(e)
            error_article.append(article_id)

    write_file(get_path(["prompter", f"batch-result-{article_range}.json"]), request_data)


timestamp = time.strftime("%Y%m%d-%H%M%S")
write_file(get_path(["prompter", f"qas-dataset-{timestamp}.json"]), qas_dataset)
write_file(get_path(["prompter", f"qas-dataset-error-{timestamp}.json"]), error_article)
print(f"Finished processing. \nTotal of {len(qas_dataset)} successfully parsed questions. \nTotal of {len(error_article)} error articles.")
    