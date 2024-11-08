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
   - Choose a context sentence or paragraph from the article’s body where the question is formulated.
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
        title: "Biyahe paingon sa mga lalawigan sa CV gisuspenso",
        context: "Daghang biyahe sa barko nga gikan sa Cebu ang gipasuspenso tungod sa daotang panahon ug dagkong bawod."
        question: "Nganong gisuspenso ang biyahe sa barko gikan sa Cebu?",
        answer_text: "Daotang panahon ug dagkong bawod."
        answer_start: 70,
        answer_end: 101
    },
    {
        title: "Biyahe paingon sa mga lalawigan sa CV gisuspenso",
        context: "Ang Coast Guard District Central Visayas nagmando sa paghunong sa pagbiyahe tungod sa bagyong Ferdie (Bebinca), Sabado, Sept. 14, 2024."
        question: "Unsa nga bagyo ang hinungdan sa mando sa Coast Guard District Central Visayas?",
        answer_text: "Bagyong Ferdie"
        answer_start: 88,
        answer_end: 101,
    },
    {
        title: "Biyahe paingon sa mga lalawigan sa CV gisuspenso",
        context: "Ang Coast Guard District Central Visayas nagmando sa paghunong sa pagbiyahe tungod sa bagyong Ferdie (Bebinca), Sabado, Sept. 14, 2024."
        question: "Kanus-a maigo si Bagyong Ferdie?",
        answer_text: "Bagyong Ferdie"
        answer_start: 114,
        answer_end: 135,
    },
    // insert 17 more Question Answer objects
]


### Here is the Cebuano news article JSON object. Use this for generating the question and answer dataset:
{
        "title": "Oliva way klarong molansar, posters iyang gipatangtang",
        "body": "<p>Gipatangtang ni Mandaue City treasurer Regal Oliva ang mga poster sa kadalanan sa dakbayan nga nagpakita sa iyang hulagway taliwala sa huhungihong nga modagan siya sa umaabot nga eleksyon sa Mayo sunod tuig. </p><p>Gihangop ni Oliva ang maong lakang nga padayon pa niyang gikonsiderar apan ang pagdumala sa panalapi sa dakbayan sa Mandaue maoy mas mahinungdanon’g katungdanan alang kaniya sa pagka karon. </p><p>Karong bag-o, adunay mga poster sa kadalanan sa siyudad nga nagpakita sa iyang imahe, hinungdan nga mitumaw ang espekulasyon nga siya modagan sa 2025 midterm elections. </p><p>Agi’g tubag, gimando ni Oliva nga tangtangon una ang mga poster gumikan kay wa pa siyay final nga desisyon mahitungod niini. </p><p>Sa miaging Huwebes, Septiyembre 12, 2024, miasoy si Oliva sa mga tigbalita nga taliwala sa awhag kaniya sa ubang mga partido ug nagkalain-laing sektor nga modagan, ang iyang posisyon karon isip tig kolekta og buhis ug pagdumala sa panudlanan sa syudad mamahimong mas gikinahanglan kaysa sa lehislatibo nga posisyon.</p><p>“If I decide to run, it will be a personal decision, not because of others who might have their own motives,” matod ni Oliva. </p><p>Sa miaging mga taho, si Oliva niingon nga iyang hagiton si incumbent Mandaue City Lone District Rep. Emmarie “Lolypop” Quano-Dizon sa umaabot nga piniliay.</p><p>Kini nga espekulasyon nitumaw human gipasanginlan ni Oliva ang kongresista nga maoy nisuway sa pagbalhin kaniya ngadto sa Navotas City.</p><p>Taliwala niini, subling gipamatud-an ni Oliva nga wala pa siyay hingpit nga desisyon kalabot sa iyang kandidatura.</p><p>Gipasabot ni Oliva nga ang mga poster diin anaa ang iyang dagway mahimong binuhatan sa mga tawo nga nag-awhag kaniya sa pagdagan.</p><p>“There are so many parties and sectors in the community urging me to run, so that might be why the posters were posted,” si Oliva nagkanayon.</p><p>Namatikdan niya nga samtang gipasalamatan niya ang suporta gikan sa iyang mga higala, samtang ang gugma ug pagdasig labi ka daghan, gihangyo niya nga tangtangon kini nga mga poster tungod kay wala pa siya makahukom sa pagdagan karong umaabot eleksyon.</p><p>Matud niya nga sanglit pipila pa ka bulan una pa moabot ang adlaw sa piniliay, mahinungdanon nga adunay pagtahod sa tukma nga panahon alang sa ingon niini nga mga inisyatibo.</p><p>“I’m sorry, but I had them taken down because I don’t want to be seen as a traditional politician with my face all over the city,” saysay sa Mandaue City treasurer. </p><p>Gihatagan niya og gibug-aton nga adunay tukma nga panahon alang sa mga materyales sa kampanya, ug sayo pa kaayo alang sa ingon nga mga pasundayag.</p><p>Nakahukom si Oliva nga i-recycle ang mga materyales gikan sa gitangtang nga mga poster ug tarpaulin.</p><p>Siya mismo ang mipalit niini ug gidonar kini ngadto sa mga underprivileged nga mga miyembro sa komunidad aron magamit sa lainlaing mga panginahanglan, lakip ang pag-ayo sa balay.</p><p>“I am calling on all Mandauehanons to help remove and turnover these posters/tarpaulins to me. It would be wonderful if they are not damaged, as I plan to recycle the tarpaulins into reusable bags for the women’s sector in our community. The wooden frames can also be repurposed to support the housing needs of our less fortunate communities. Let’s continue to promote and nurture sustainability within our city”, matod ni Oliva sa iyang Facebook post niadtong Septiyembre 11. </p><p>Hatagan niya og reward si bisan kinsa nga mouli sa mga posters ngadto sa iyang buhatan sa City Hall nga P100 alang sa poster nga naay frame ug P25 alang sa poster lang. / <strong>CAV</strong>, <strong>TPT</strong></p>"
    }

