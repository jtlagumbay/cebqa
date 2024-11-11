# Pseudonymizer

Replaces names of person with another name.

The stop_words.tsv contains words that are tagged as person by the NER model but is not a name of a person. Example: "Jr", "Atty". These words should not be pseudonymized.



## Dependencies
This pseudonymizer uses [CebuaNER](https://github.com/mebzmoren/CebuaNER/tree/main) model by Pilar et al. (2023).