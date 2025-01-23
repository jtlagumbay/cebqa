from utils import *
from openai import OpenAI
from pydantic import BaseModel
from openai.lib._pydantic import to_strict_json_schema

articles = read_file(get_path(["data", "cleaned-pseudonymized_articles-20241116-115334.json"]))

def create_prompt(cebuano_article):
    message = """
    ### Task Objective:
    You are a Cebuano Factoid Extractive Question and Answering Dataset Generation Agent. Your task is to create a dataset of fact-based (factoid) questions that can be answered using short spans of text found directly within a given Cebuano news article. These questions are typically wh-questions (e.g., who, what, when, where, why) that refer to specific, identifiable facts.

    ### Instructions:
    1. You will receive a Cebuano news article in a JSON object with the following fields:
    - "title": The given title of the news article.
    - "body": The content of the news article.
    2. Create 20 unique questions that:
    - Focus on factual information.
    - Are directly answerable by brief, exact information within a single sentence from the article. 
    3. For each question:
    - Choose a context sentence or adjacent sentences from the article's body where the question is formulated.
    - Format the question and answer in a JSON object with the following fields:
        - "title": The title of the Cebuano news article.
        - "context": The sentence or adjacent sentences from the article's body where the question is derived, ensuring that the context contains the answer. Context can be a more than one sentence, and can also be reused in another question, as long as it does not paraphrase the article's body.
        - "question": A question based on the selected context.
        - "answer": The exact, brief answer found within the context.
    4. Ensure that:
    - All questions and answers are written in Cebuano.
    - No questions are repeated.
    - Each context is directly a substring from the article's body. 
    - Each answer accurately reflects the answer span within the context (from answer_start to answer_end).
    5. Compile all JSON question-answer objects into a JSON array as the final output.
    
    ### Example (for formatting guidance only; use content from the new article below):
    #### Example Cebuano Article
        {
            "title": "Biyahe paingon sa mga lalawigan sa CV gisuspenso",
            "body": "Ang mga biyahe sa barko paingon sa Bohol, Camotes, Leyte, Negros, Siquijor gipasuspenso, pahibawo sa Coast Guard District Central Visayas. Daghang biyahe sa barko nga gikan sa Cebu ang gipasuspenso tungod sa daotang panahon ug dagkong bawod. Ang Coast Guard District Central Visayas nagmando sa paghunong sa pagbiyahe tungod sa bagyong Ferdie (Bebinca), Sabado, Sept. 14, 2024. Mabalik sa normal nga operasyon kon molurang ang dautang panahon. Nagpagawas og travel advisory para sa mga barko nga adunay gross tonnage nga 250 ug ubos, nga nakaapekto sa mga rota gikan sa Negros Oriental, Kasadpang Bohol, Sidlangan Bohol, Camotes, ug Siquijor. Dugang pa, ang mga barko nga adunay gross tonnage nga 15 ug ubos dili tugotan nga molarga gikan sa Amihanang Cebu, Sentral Cebu ug Habagatang Cebu. Ang Cebu Port Authority (CPA) mipahibalo pinaagi sa ilang Facebook page mahitungod sa mga kanseladong biyahe gikan sa Cebu padulong sa Bohol. Si CPA public information officer Mary Balaba Balagtas-Balaguer, sa iyang chat message sa SunStar Cebu, nitambag sa mga pasahero angayan nga mopauli lang una ug magpaabot sa mga bag-ong update. “Mga stranded passengers mao na among i-turn over to concerned LGU (local government unit) aron moagi og shelter kay bawal magtambay ang mga stranded passengers sa pantalan, labi na kusog ang hangin ug balod,” matod pa ni Balagtas-Balaguer. / JPS, PNA",
        }    

    #### Example Generated Cebuano Question Answering Dataset:
    [
        {
            "title": "Biyahe paingon sa mga lalawigan sa CV gisuspenso",
            "context": "Daghang biyahe sa barko nga gikan sa Cebu ang gipasuspenso tungod sa daotang panahon ug dagkong bawod.",
            "question": "Nganong gisuspenso ang biyahe sa barko gikan sa Cebu?",
            "answer": "daotang panahon ug dagkong bawod"
        },
        {
            "title": "Biyahe paingon sa mga lalawigan sa CV gisuspenso",
            "context": "Ang Coast Guard District Central Visayas nagmando sa paghunong sa pagbiyahe tungod sa bagyong Ferdie (Bebinca), Sabado, Sept. 14, 2024."
            "question": "Unsa nga bagyo ang hinungdan sa mando sa Coast Guard District Central Visayas?",
            "answer": "bagyong Ferdie"
        },
        // insert 18 more Question Answer objects
    ]


    ### Here is the Cebuano news article JSON object. Use this for generating the question and answer dataset:
    """
    message += f"{cebuano_article}"
    return message

class QA(BaseModel):
    title: str
    context: str
    question: str
    answer: str

class QADataset(BaseModel):
    data: list[QA]

requests = []
start = 370
end = 450

for article in articles[start:end]:
    cebuano_article = {
        "title": article["pseudonymized_title"],
        "body": article["pseudonymized_body"]
    }
    message = create_prompt(cebuano_article)
    request = {
        "custom_id": f"article-{article["id"]}", 
        "method": "POST", 
        "url": "/v1/chat/completions", 
        "body": {
            "model": "gpt-4o", 
            "messages": [
                {
                    "role": "system", 
                    "content": message
                }
            ],
            "response_format" : {
                "type": "json_schema",
                "json_schema": {
                    "name": "object",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "data": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "title": {"type": "string"},
                                        "context": {"type": "string"},
                                        "question": {"type": "string"},
                                        "answer": {"type": "string"}
                                    },
                                    "required": ["title", "context", "question", "answer"],
                                    "additionalProperties": False
                                }
                            }
                        },
                        "required": ["data"],
                        "additionalProperties": False
                    }
                }
            }
        }
    }
    requests.append(request)

# print(requests)
write_file(get_path(["prompter", f"batch-request-4o-{start}-{end}.jsonl"]), requests)
