from openai import OpenAI
from pydantic import BaseModel
import json

client = OpenAI()

cebuano_article=    {
        "title": "Biyahe paingon sa mga lalawigan sa CV gisuspenso",
        "body": "<p>Ang mga biyahe sa barko paingon sa Bohol, Camotes, Leyte, Negros, Siquijor gipasuspenso, pahibawo sa Coast Guard District Central Visayas. </p><p>Daghang biyahe sa barko nga gikan sa Cebu ang gipa­suspenso tungod sa daotang pana­hon ug dagkong bawod.</p><p>Ang Coast Guard District Central Visayas nagmando sa paghunong sa pagbiyahe tungod sa bagyong Ferdie (Bebinca), Sabado, Sept. 14, 2024. </p><p>Mabalik sa normal nga operasyon kon molurang ang dautang panahon.</p><p>Nagpagawas og travel advisory para sa mga barko nga adunay gross tonnage nga 250 ug ubos, nga nakaapekto sa mga rota gikan sa Negros Oriental, Kasadpang Bohol, Sidlangan Bohol, Camotes, ug Siquijor. Dugang pa, ang mga barko nga adunay gross tonnage nga 15 ug ubos dili tugotan nga molarga gikan sa Amihanang Cebu, Sentral Cebu ug Habagatang Cebu.</p><p>Ang Cebu Port Authority (CPA) mipahibalo pinaagi sa ilang Facebook page mahitungod sa mga kanseladong biyahe gikan sa Cebu padulong sa Bohol.</p><p>Si CPA public information officer Mary Knoll Lague-Bolasa, sa iyang chat message sa SunStar Cebu, nitambag sa mga pasahero angayan nga mopauli lang una ug magpaabot sa mga bag-ong update.</p><p>“Mga stranded passengers mao na among i-turn over to concerned LGU (local government unit) aron moagi og shelter kay bawal magtambay ang mga stranded passengers sa pantalan, labi na kusog ang hangin ug balod,” matod pa ni Lague-Bolasa. / <strong>JPS</strong>, <strong>PNA</strong></p>"
    }

message = """
 ### Task Objective:
You are a Cebuano Factoid Extractive Question and Answering Dataset Generation Agent. Your task is to create a dataset of fact-based (factoid) questions that can be answered using short spans of text found directly within a given Cebuano news article. These questions are typically wh-questions (e.g., who, what, when, where, why) that refer to specific, identifiable facts.

### Instructions:
1. You will receive a Cebuano news article in a JSON object with the following fields:
   - "title": The given title of the news article.
   - "body": The content of the news article.
2. Create 20 unique questions that:
   - Focus on factual information.
   - Are directly answerable by brief, exact information within a single sentence or paragraph from the article. 
3. For each question:
   - Choose a context sentence or paragraph from the article's body where the question is formulated.
   - Format the question and answer in a JSON object with the following fields:
     - "title": The title of the Cebuano news article.
     - "context": The sentence or paragraph from the body where the question is derived, ensuring that the context contains the answer.
     - "question": A question based on the selected context.
     - "answer_text": The exact, brief answer found within the context.
     - "answer_start": The starting index of the answer within the context.
     - "answer_end": The ending index of the answer within the context.
4. Ensure that:
   - All questions and answers are written in Cebuano.
   - No questions are repeated.
   - Each answer accurately reflects the answer span within the context (from answer_start to answer_end).
5. Compile all JSON question-answer objects into a JSON array as the final output.
   
### Example (for formatting guidance only; use content from the new article below):
#### Example Cebuano Article
    {
        "title": "Biyahe paingon sa mga lalawigan sa CV gisuspenso",
        "body": "<p>Ang mga biyahe sa barko paingon sa Bohol, Camotes, Leyte, Negros, Siquijor gipasuspenso, pahibawo sa Coast Guard District Central Visayas. </p><p>Daghang biyahe sa barko nga gikan sa Cebu ang gipa­suspenso tungod sa daotang pana­hon ug dagkong bawod.</p><p>Ang Coast Guard District Central Visayas nagmando sa paghunong sa pagbiyahe tungod sa bagyong Ferdie (Bebinca), Sabado, Sept. 14, 2024. </p><p>Mabalik sa normal nga operasyon kon molurang ang dautang panahon.</p><p>Nagpagawas og travel advisory para sa mga barko nga adunay gross tonnage nga 250 ug ubos, nga nakaapekto sa mga rota gikan sa Negros Oriental, Kasadpang Bohol, Sidlangan Bohol, Camotes, ug Siquijor. Dugang pa, ang mga barko nga adunay gross tonnage nga 15 ug ubos dili tugotan nga molarga gikan sa Amihanang Cebu, Sentral Cebu ug Habagatang Cebu.</p><p>Ang Cebu Port Authority (CPA) mipahibalo pinaagi sa ilang Facebook page mahitungod sa mga kanseladong biyahe gikan sa Cebu padulong sa Bohol.</p><p>Si CPA public information officer Mary Knoll Lague-Bolasa, sa iyang chat message sa SunStar Cebu, nitambag sa mga pasahero angayan nga mopauli lang una ug magpaabot sa mga bag-ong update.</p><p>“Mga stranded passengers mao na among i-turn over to concerned LGU (local government unit) aron moagi og shelter kay bawal magtambay ang mga stranded passengers sa pantalan, labi na kusog ang hangin ug balod,” matod pa ni Lague-Bolasa. / <strong>JPS</strong>, <strong>PNA</strong></p>"
    }

#### Example Generated Cebuano Question Answering Dataset:
[
    {
        "title": "Biyahe paingon sa mga lalawigan sa CV gisuspenso",
        "context": "Daghang biyahe sa barko nga gikan sa Cebu ang gipasuspenso tungod sa daotang panahon ug dagkong bawod."
        "question": "Nganong gisuspenso ang biyahe sa barko gikan sa Cebu?",
        "answer_text": "Daotang panahon ug dagkong bawod."
        "answer_start": 70,
        "answer_end": 101
    },
    {
        "title": "Biyahe paingon sa mga lalawigan sa CV gisuspenso",
        "context": "Ang Coast Guard District Central Visayas nagmando sa paghunong sa pagbiyahe tungod sa bagyong Ferdie (Bebinca), Sabado, Sept. 14, 2024."
        "question": "Unsa nga bagyo ang hinungdan sa mando sa Coast Guard District Central Visayas?",
        "answer_text": "Bagyong Ferdie"
        "answer_start": 88,
        "answer_end": 101,
    },
    {
        "title": "Biyahe paingon sa mga lalawigan sa CV gisuspenso",
        "context": "Ang Coast Guard District Central Visayas nagmando sa paghunong sa pagbiyahe tungod sa bagyong Ferdie (Bebinca), Sabado, Sept. 14, 2024."
        "question": "Kanus-a maigo si Bagyong Ferdie?",
        "answer_text": "Bagyong Ferdie"
        "answer_start": 114,
        "answer_end": 135,
    },
    // insert 17 more Question Answer objects
]


### Here is the Cebuano news article JSON object. Use this for generating the question and answer dataset:
"""
message += f"{cebuano_article}"

class QA(BaseModel):
    title: str
    context: str
    question: str
    answer_text: str
    answer_start: int
    answer_end: int

class QADataset(BaseModel):
    data: list[QA]

completion = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system", 
            "content": message
        }
    ],
    response_format=QADataset
)

output = completion.choices[0].message.parsed

# Dump the model to a dictionary with JSON-compatible formatting
output_dict = output.model_dump(mode='json')

# Print the dictionary with indentation using json.dumps()
print(json.dumps(output_dict, indent=4))