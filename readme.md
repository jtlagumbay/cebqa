# Cebuano Question Answering System 

Contains scripts and notebooks used for preparing the dataset and training the model.

Arranged in the following directories:
1. Scraper
   > contains files for scraping list of articles and their content
2. Pseudonymizer
   > contains files for pseudonymizing articles.
3. Prompter
   > contains files for prompting GPT for dataset generation
4. Data
   > contains json files containing the final dataset used in each step.

## Steps for running
1. [Skip] Create virtual environment: `python3.12 -m venv venv`
2. Run venv: `source  venv3-12/bin/activate`
3. Install dependencies: `pip3 install -r requirements.txt`
4. To run a script, run `python <folder_name>/<script_name>`. Example: `scraper/article_url_parser` 
5. Add path of module to environment: export PYTHONPATH:<path of folder>/utils.py `export PYTHONPATH=$PYTHONPATH:/Users/jhoannaricalagumbay/School/cebqa/utils.py`
6. `brew install tcl-tk` 
7. `brew install python-tk`
## Contact
For questions, please contact:

**Jhoanna Rica Lagumbay**\
BS Computer Science IV\
University of the Philippines Cebu\
jtlagumbay@up.edu.ph