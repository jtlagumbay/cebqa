from openai import OpenAI
from pydantic import BaseModel
import json
from utils import *
import time
from openai.lib._pydantic import to_strict_json_schema

client = OpenAI()

cebuano_article =     {
        "title": "Abalayan-Abarca III tandem silyado na",
        "body": "Niduso si Cebu City acting Mayor Jhonnylou Ghen Abalayan sa iyang certificate of candidacy (COC) alang sa pagka mayor sa dakbayan ubos sa Kusug-Panaghiusa coalition atol sa katapusang adlaw sa filing sa Martes, Oktubre 8, 2024. Nisaad nga mohimo pa kini og dugang kahigayunan sa mga residente niini aron mapalambo ang ilang kalidad sa kinabuhi. Si Abalayan ug ang iyang running mate nga si Porferio Abarca niabot sa buhatan sa Commission on Elections (Comelec) sa Dakbayan sa Sugbo alas 10:45 sa buntag ug niduso sa ilang COC uban sa line-up sa 16 ka mga kandidato sa pagka konsehal nga naglakip sa unom ka mga incumbent. “I am both honored and humbled to officially run as mayor and seek the mandate of the beloved citizens of Cebu City,” matod ni Abalayan atubangan sa dili mominos 3,000 ka supporters nga naghugyaw alang sa mga kandidato ubos sa Kusug-Panaghiusa coalition human sa pag-file sa ilang COCs. Si Abalayan maoy acting chief executive sa dakbayan sukad niadtong Mayo nunot sa unom ka buwan nga preventive suspension ni Mayor Lizer Abangan sa Office of the Ombudsman tungod sa kapakyas pagbayad sa sweldo sa upat ka mga empleyado sa City Hall. Gidayeg siya sa iyang mga konstituwente isip \"action mayor\" tungod sa iyang makita nga mga nahimo bisan pa sa iyang mubo nga paglingkod isip amahan sa Dakbayan sa Sugbo, lakip niini ang paghuman sa Guba Community Hospital ug sa Apas Super Family Health Center nga wala mahuman sulod sa daghang katuigan hangtod nga iyang gipulihan ug gipabalik ang mga proyekto sa hingpit nga paglihok. Giaprobahan ni Abalayan ang pagpalit og mga sakyanan sa kapulisan—usa ka hangyo nga dugay nang nagpaabot—sa dihang siya ang nagdumala sa Dakbayan sa Sugbo sa tinguha nga mapalig-on ang kalinaw ug kahusay. Ang 47-anyos nga Abalayan, ang kinamanghuran nga kandidato sa four-way fight, maoy bise mayor ug running mate ni Abangan niadtong 2022. Nibarog siya sa hagit ug malampusong nakahatag og kalig-on sa nagkurog nga lokal nga kagamhanan ug polarized community. Ang full line-up  sa mga konsehal nga nidagan ubos sa Kusug-Panaghiusa coalition ticket  nalakip ni Cristitulo Abarquez, Cleret Abastar ug Serging Abastillas gikan sa north district ug Adrian Abaya, Jeff Abayon, ug Renato “Cristitulojun” Abcede gikan sa south.  Mikompleto sa ilang line-up mao sila si Joan Abdon, Remigio Go, Charie Rizali Jeganiel, RJ Abcede, Khart Abdulraman sa north district ug  Hannah Abe, Abecia Abenosa, Percival Jeganiel, Leonard Abastillas and Elmer Abel sa south district. / JPS"
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
   - Are directly answerable by brief, exact information within a single sentence from the article. 
3. For each question:
   - Choose a context sentence or adjacent sentences from the article's body where the question is formulated.
   - Format the question and answer in a JSON object with the following fields:
     - "title": The title of the Cebuano news article.
     - "context": The sentence or adjacent sentences or paragraph from the article's body where the question is derived, ensuring that the context contains the answer. Context can be a more than one sentence, and can also be reused in another question, as long as it does not paraphrase the article's body.
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
        "answer": "daotang panahon ug dagkong bawod."
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

class QA(BaseModel):
    title: str
    context: str
    question: str
    answer: str

class QADataset(BaseModel):
    data: list[QA]

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system", 
            "content": message
        }
    ],
    # response_format= to_strict_json_schema(QADataset)
    response_format = {
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
)
print(completion)

output = completion.choices[0].message.content
print(output)
# # Dump the model to a dictionary with JSON-compatible formatting
# output_dict = output.model_dump(mode='json')
timestamp = time.strftime("%Y%m%d-%H%M%S")

# # Print the dictionary with indentation using json.dumps()
# print(json.dumps(output_dict, indent=4))

write_file(get_path(["prompter", f"qa-article-9-{timestamp}.json"]), output)
