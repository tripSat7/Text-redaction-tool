import argparse
import glob
import os
import re
from langcodes import Language
import spacy
from spacy.matcher import Matcher
from spacy.tokens import Doc, Span
import sys
from collections import defaultdict
import warnings
warnings.filterwarnings("ignore")

CENSOR_CHAR = '█'

censorName=0
censorAddress=0
censorPhone=0
censorDate=0

# Defining entity types for censoring
ENTITY_TYPES = {
    'names': ['PERSON'],
    'dates': ['DATE', 'TIME'],
    'phones': ['CARDINAL'],
    'address': ['ORG', 'FAC', 'GPE']
}

def ensure_spacy_model():
    try:
        return spacy.load("en_core_web_md")
    except IOError:
        print("Downloading necessary SpaCy model...")
        spacy.cli.download("en_core_web_md")
        return spacy.load("en_core_web_md")

language_processor = ensure_spacy_model()

# Adding custom pattern to match dates in "mm/dd/yyyy" format
matcher = Matcher(language_processor.vocab)
pattern = [{"SHAPE": "dd"}, {"ORTH": "/"}, {"SHAPE": "dd"}, {"ORTH": "/"}, {"SHAPE": "dddd"}]
matcher.add("DATE_FORMAT", [pattern])

# Defining custom component to merge detected dates into a single token
@spacy.Language.component("merge_date_tokens")
def merge_date_tokens(doc):
    with doc.retokenize() as retokenizer:
        for match_id, start, end in matcher(doc):
            match_span = doc[start:end]
            retokenizer.merge(match_span)
    return doc

# Adding the custom component to the spacy pipeline
language_processor.add_pipe("merge_date_tokens", after="ner")

# Setting up and parsing command-line arguments
def configure_parser():
    argument_parser  = argparse.ArgumentParser(description="Text censoring tool")
    argument_parser .add_argument("--input", nargs='+', help="Input file(s) pattern(s)")
    argument_parser .add_argument("--output", help="Output directory for censored files")
    argument_parser .add_argument("--stats", help="Statistics output file or stderr/stdout")
    argument_parser .add_argument("--names", action="store_true", help="Censor names")
    argument_parser .add_argument("--dates", action="store_true", help="Censor dates")
    argument_parser .add_argument("--phones", action="store_true", help="Censor phone numbers")
    argument_parser .add_argument("--address", action="store_true", help="Censor addresses")
    return argument_parser .parse_args()


def replace_entity_with_censor(text, start, end, censor_char):
    # Replaces a specified entity in the text with the censor character.

    return text[:start] + censor_char * (end - start) + text[end:]


# Processing the text to censor specified entity types
def censor_info(text, entity_types):
    global censorName, censorAddress, censorPhone, censorDate
    # Reset counters for each text processing call
    censorName=0
    censorAddress=0
    censorPhone=0
    censorDate=0
    doc = language_processor(text)

    # Defining regular expression pattern for phone numbers
    phone_pattern = re.compile(r'\+\d{1,3}(?:[-\s()]?\d{1,3}[-\s()]?){3,5}\d{1,5}')

    censored_text = text
    
    for ent in doc.ents:
        if ent.label_ in entity_types['names']:
            start = ent.start_char
            end = ent.end_char
            censored_text = replace_entity_with_censor(censored_text, start, end, CENSOR_CHAR)
            censorName+=1
        
        if ent.label_ in entity_types['dates']:
            start = ent.start_char
            end = ent.end_char
            censored_text = replace_entity_with_censor(censored_text, start, end, CENSOR_CHAR)
            censorDate+=1
        
        if ent.label_ in entity_types['address']:
            start = ent.start_char
            end = ent.end_char
            censored_text = replace_entity_with_censor(censored_text, start, end, CENSOR_CHAR)
            censorAddress+=1

        if ent.label_ in entity_types['phones']:
            start = ent.start_char
            end = ent.end_char
            censored_text = replace_entity_with_censor(censored_text, start, end, CENSOR_CHAR)
            censorPhone+=1

    for token in doc:
        if phone_pattern.search(token.text):
        # Replacing phone number with censor
            start = token.idx
            end = start + len(token.text)
            censored_text = censored_text[:start] + CENSOR_CHAR * len(token.text) + censored_text[end:]
            censorPhone+=1

    return censored_text

# Generating summary statistics of the censorship process
def generate_statistics(censored_texts):
    stats = defaultdict(int)
    stats["Name"]=censorName
    stats["Address and Country"]=censorAddress
    stats["Date"]=censorDate
    stats["Numerical Value"]=censorPhone
    return stats

def main():
    args = configure_parser()
    if args.output and not os.path.exists(args.output):
        os.makedirs(args.output)
    # Collect censored texts and statistics
    censored_texts = []
    clearFile=True # Flag to clear the stats file before writing for the first time
    
    # Processing each file specified in the input patterns
    for input_pattern in args.input:
        for input_file in glob.glob(input_pattern):
            
            with open(input_file, 'r', encoding='utf-8') as file:
                text = file.read()
                censored_text = censor_info(text, ENTITY_TYPES)
                censored_texts.append(censored_text)

                # Write censored text to output directory
                output_file = os.path.join(args.output, os.path.splitext(os.path.basename(input_file))[0]  + '.censored')
                with open(output_file, 'w', encoding='utf-8') as outfile:
                    outfile.write(censored_text)

                # Generate statistics
                statistics = generate_statistics(censored_texts)

                # Write statistics to file or stdout/stderr
                if args.stats:
                    if args.stats == 'stderr':
                        for key, value in statistics.items():
                            print(f"{key}: {value}", file=sys.stderr)
                    elif args.stats == 'stdout':
                        print("---Statistics for "+ input_file)
                        for key, value in statistics.items():
                            print(f"{key}: {value}")
                    else:
                        if(clearFile):
                            clearFile=False
                            with open(args.stats, 'w', encoding='utf-8') as stats_file:
                                pass
   
                        with open(args.stats, 'a', encoding='utf-8') as stats_file:
                            stats_file.write("---Statistics for "+ input_file+"\n")
                            for key, value in statistics.items():
                                stats_file.write(f"{key}: {value}\n")
                            stats_file.write("\n")

if __name__ == "__main__":
    main()
