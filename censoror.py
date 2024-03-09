import argparse
import glob
import os
import re
import spacy
from spacy.matcher import Matcher
from spacy.tokens import Doc, Span
import sys
from collections import defaultdict
import warnings
warnings.filterwarnings("ignore")

# Define censor character
CENSOR_CHAR = '█'

# Define entity types for censoring
ENTITY_TYPES = {
    'names': ['PERSON'],
    'dates': ['DATE', 'TIME'],
    'phones': ['CARDINAL'],
    'address': ['ORG', 'FAC', 'GPE']
}

censorName=0
censorAddress=0
censorPhone=0
censorDate=0

nlp = spacy.load("en_core_web_md")
# print(nlp.get_pipe("ner").labels)


# Add custom pattern to match dates in "mm/dd/yyyy" format
matcher = Matcher(nlp.vocab)
pattern = [{"SHAPE": "dd"}, {"ORTH": "/"}, {"SHAPE": "dd"}, {"ORTH": "/"}, {"SHAPE": "dddd"}]
matcher.add("DATE_FORMAT", [pattern])

# Define custom component to merge detected dates into a single token
@spacy.Language.component("merge_date_tokens")
def merge_date_tokens(doc):
    with doc.retokenize() as retokenizer:
        for match_id, start, end in matcher(doc):
            match_span = doc[start:end]
            retokenizer.merge(match_span)
    return doc

nlp.add_pipe("merge_date_tokens", after="ner")


def parse_arguments():
    parser = argparse.ArgumentParser(description="Text censoring tool")
    parser.add_argument("--input", nargs='+', help="Input file(s) pattern(s)")
    parser.add_argument("--output", help="Output directory for censored files")
    parser.add_argument("--stats", help="Statistics output file or stderr/stdout")
    parser.add_argument("--names", action="store_true", help="Censor names")
    parser.add_argument("--dates", action="store_true", help="Censor dates")
    parser.add_argument("--phones", action="store_true", help="Censor phone numbers")
    parser.add_argument("--address", action="store_true", help="Censor addresses")
    return parser.parse_args()

def censor_text(text, entity_types):
    global censorName, censorAddress, censorPhone, censorDate
    censorName=0
    censorAddress=0
    censorPhone=0
    censorDate=0
    doc = nlp(text)

    # Define regular expression pattern for phone numbers
    phone_pattern = re.compile(r'\+\d{1,3}(?:[-\s()]?\d{1,3}[-\s()]?){3,5}\d{1,5}')

    censored_text = text
    # print(doc.ents)
    
    for ent in doc.ents:
        #print(ent.text+ " "+ ent.label_)
        if ent.label_ in entity_types['names']:
            start = ent.start_char
            end = ent.end_char
            censored_text = censored_text[:start] + CENSOR_CHAR * (end - start) + censored_text[end:]
            censorName+=1
        
        if ent.label_ in entity_types['dates']:
            start = ent.start_char
            end = ent.end_char
            censored_text = censored_text[:start] + CENSOR_CHAR * (end - start) + censored_text[end:]
            censorDate+=1
        
        if ent.label_ in entity_types['address']:
            start = ent.start_char
            end = ent.end_char
            censored_text = censored_text[:start] + CENSOR_CHAR * (end - start) + censored_text[end:]
            censorAddress+=1

        if ent.label_ in entity_types['phones']:
            start = ent.start_char
            end = ent.end_char
            censored_text = censored_text[:start] + CENSOR_CHAR * (end - start) + censored_text[end:]
            censorPhone+=1

    for token in doc:
        if phone_pattern.search(token.text):
        # Replace phone number with censor characters
            start = token.idx
            end = start + len(token.text)
            censored_text = censored_text[:start] + CENSOR_CHAR * len(token.text) + censored_text[end:]
            censorPhone+=1

    return censored_text

def generate_statistics(censored_texts):
    statistics = defaultdict(int)
    statistics["Name"]=censorName
    statistics["Address and Country"]=censorAddress
    statistics["Date"]=censorDate
    statistics["Numerical Value"]=censorPhone
    return statistics

def main():
    args = parse_arguments()
    if args.output and not os.path.exists(args.output):
        os.makedirs(args.output)
    # Collect censored texts and statistics
    censored_texts = []
    clearFile=True
    for input_pattern in args.input:
        for input_file in glob.glob(input_pattern):
            with open(input_file, 'r', encoding='utf-8') as file:
                text = file.read()
                censored_text = censor_text(text, ENTITY_TYPES)
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
