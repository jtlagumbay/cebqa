from openai import OpenAI
from pydantic import BaseModel
import json
from utils import *
import time
from openai.lib._pydantic import to_strict_json_schema

client = OpenAI()

cebuano_article =     {
        "title": "Abando midangop sa SC",
        "body": "Ang gitaktak nga mayor, Brody Abando, nangayo og interbensyon sa Supreme Court (SC) aron babagan ang Commission on Elections (Comelec) sa pagpatuman sa dismissal order sa Office of the Ombudsman batok kaniya. Si Abando nisang-at og petisyon alang sa Certiorari, Prohibition, and Injunction atubangan sa SC niadtong Miyerkules, Oktubre 9, 2024, nga naghagit sa Comelec Resolution No. 1104-A, nga nagmando sa hinanaling pagkansela sa mga certificates of candidacy (COCs) sa mga kandidato nga nag-atubang og administratibo nga mga kaso bisan sa wala pa mahimong pinal ang desisyon. Ang Ombudsman, sa desisyon nga pinetsahan og Septiyembre 26, nitaktak kang Abando sa serbisyo human siya napamatud-ang sad-an sa grave misconduct tungod sa pagtugot sa padayong operasyon sa usa ka cement batching plant nga way gikinahanglang business ug environmental permits. Si City Administrator Jamaal Adrian Abangad nitug-an sa mga tigbalita niadtong Miyerkules nga si Abando nangayo og legal recourse susama sa kang Abangan. Ang legal nga lakang ni Abando susama sa gihimo sa dismissal nga mayor nga si Cedie Abangan nga niduso usab og petisyon sa SC aron hunongon ang iyang pagkataktak ug pagkadiskwalipikasyon sa serbisyo niadtong Oktubre 7.“The petition for certiorari under Rule 65 of the Supreme Court is a remedy available to the mayor, who stands to be injured by the implementation of this Comelec resolution. Mayor Brody and Mayor Lizer Abangan are in similar situations regarding this Comelec resolution’s application,” matod ni Abangad. Si Abangad miingon nga ang desisyon batok kaniya dili pa pinal, ug samtang ilang gitahod ang hukom sa Ombudsman, ilang gihagit ang dihadiha nga executory nga kinaiya sa desisyon ilabi na ang paglakip niini sa disqualification penalty. Ang pagkanselar sa iyang COC makapugong sa pagbotar ni Abando sa 2025 elections, usa ka lakang nga gihulagway ni Abangad nga usa ka “irreparable” injury sa mayor ug sa katawhan sa Mandaue City. “The disqualification penalty is not like dismissal. If the decision is reversed, the mayor could receive back wages for the time lost. But once disqualified, there’s no turning back, his name will be removed from the ballots, and the people’s choice in the election will be disregarded,” dugang ni Abangad. Ang legal team ni Abando nangayo og Temporary Restraining Order (TRO) o Writ of Preliminary Injunction gikan sa SC aron mapugngan ang Comelec sa pagpatuman sa resolusyon sa dili pa ang pag-imprinta sa mga balota nga gikatakdang sugdan karong Nobiyembre 15. Kung wala ang TRO, mahimong tangtangon sa Comelec ang ngalan ni Abando sa balota nga permanenteng makaapekto sa iyang kandidatura. Nikuwestiyon si Abando niadtong Martes sa  resolusyon sa Comelec kinsa nangatarongan nga nakalapas kini sa due process nga gigarantiya ubos sa 1987 Constitution. Iyang gihulagway ang resolusyon nga “unconstitutional” ug gimarkahan ang mga lihok sa Comelec nga “ridiculous”  ingon nga ang usa ka desisyon nga dili pinal kinahanglan dili magdala sa ingon ka grabe nga silot. “Now sa kani nga resolution asa naman ang hustisya ani? Is it just? Is it fair? That immediate executory judgment is not final,” dason ni Abando. Nangayo sab siya og dinaliang motion alang sa pagpahigayon og special raffle. Ang resolusyon naglakip sa mga probisyon alang sa dinaliang pagkansela sa COC alang sa mga kandidato nga gisilotan og disqualification sa Ombudsman bisan pa kon ang desisyon nakaabot na sa finality. Si Abando niingon nga ang maong resolusyon nagdaot sa katungod sa katawhan sa pagpili sa ilang mga lider sa usa ka demokratikong piniliay nga maoy labing importante. Sa wala pa moabot ang dismissal order, si Abando nagsilbi usab sa iyang usa ka tuig nga pagkasuspenso nga walay bayad nga gipahamtang kaniya sa Ombudsman sukad niadtong Agusto 12. Gisuspenso sa Ombudsman si Abando tungod sa grave misconduct ug conduct prejudicial to the best interest of the service tungod sa pagtudlo kang Abanto Abao isip officer-in-charge sa City Social Welfare Services Office niadtong 2022, nga matod pa sa Ombudsman. / CAV   "
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

completion = client.beta.chat.completions.parse(
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

output = completion.choices[0].message.parsed
print(output)
# Dump the model to a dictionary with JSON-compatible formatting
output_dict = output.model_dump(mode='json')
timestamp = time.strftime("%Y%m%d-%H%M%S")

# Print the dictionary with indentation using json.dumps()
print(json.dumps(output_dict, indent=4))

write_file(get_path(["prompter", f"qa-article-8-{timestamp}.json"]), output_dict)
