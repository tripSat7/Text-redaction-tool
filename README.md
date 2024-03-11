# cis6930sp24-assignment1
Name : Saatvik Tripathy\
e-mail id : saatvik.tripathy@ufl.edu\
UFID : 12326074

# Assignment Description
Assignment 1 is designed to delve into the realms of natural language processing (NLP) and data privacy, focusing on the automated redaction of sensitive information from text documents. It employs advanced NLP techniques for the identification and categorization of personal data, including names, dates, phone numbers, and addresses, ensuring their effective censorship in compliance with privacy regulations. Alongside, it offers a statistical analysis feature that generates insightful metrics about the censored entities, providing a comprehensive overview of data sensitivity and redaction efficiency. This assignment not only enhances understanding and skills in text processing and data privacy but also addresses real-world needs for data protection in various sectors such as legal documentation, customer service, and academic research.

# How to install
To install the necessary packages for this project, navigate to the root of the project directory and run : pipenv install .

# How to run
To run the main program, use the following command : pipenv run python censoror.py --input '*.txt' --names --dates --phones --address --output 'files/' --stats stdout


https://github.com/tripSat7/cis6930sp24-assignment1/assets/117186874/b9b43e62-de58-4fb1-a879-74cb9d274f85

# Functions
- ## main() :
  The `main()` function manages the censorship process for text files, parsing user inputs to determine which entity types (names, dates, addresses, and phone numbers) to censor. It reads files matching the input patterns, applies censorship through the `censor_info` function, and saves the censored content to a specified output directory. Additionally, it compiles and outputs censorship statistics to either the console, a file, or standard error, based on user preference. This function ensures that all specified files are processed accordingly, and it maintains a clear separation between original and censored content while providing insights into the censorship process.

- ## configure_parser() :
  The `configure_parser()` function sets up a command-line interface for the text censorship tool, enabling users to specify their preferences and requirements through various arguments. It allows users to define multiple input file patterns for processing, designate an output directory for the censored files, and choose a method for reporting censorship statistics (file, standard output, or standard error). Additionally, it can toggle the censorship of specific entity types such as names, dates, phone numbers, and addresses through corresponding flags. This function returns the parsed arguments, making it easy to tailor the tool's behavior to the user's needs.

- ## censor_info() :
  The `censor_info()` function processes a given text to censor specified entity types—names, dates, phone numbers, and addresses—based on user preferences.The function updates counters for each type of censored entity and replaces any entity matching the provided types with a predefined censor character, altering the text accordingly. Phone numbers are specifically targeted with a regular expression pattern for additional censorship. This function dynamically censors content, providing a customizable approach to hiding sensitive information within texts, and returns the modified text with specified entities censored.

- ## generate_statistics() :
  The `generate_statistics()` function compiles and returns statistics on the censorship process, including counts of each type of entity censored. This function facilitates the evaluation of the censoring tool's activity, offering a quantitative breakdown that can be used for reporting or analysis purposes.

- ## ensure_spacy_model() : 
  The `ensure_spacy_model()` function checks if the necessary SpaCy language model (en_core_web_md) is loaded. If not, it attempts to download and reload it. This step is crucial for text processing and entity recognition tasks within the project.

- ## Spacy Custom Component: merge_date_tokens(doc) :
  Registered as a custom component with Spacy, this function aims to detect and merge date entities in the mm/dd/yyyy format into a single token within the document, enhancing the accuracy of subsequent entity recognition and censorship.

- ## replace_entity_with_censor() :
  This is a utility function designed to replace specified portions of the text (denoted by start and end indices) with a censorship character. This function streamlines the process of hiding sensitive information within the text.

# Test Functions
- ## test_censoror_file_exists() :
  The `test_censoror_file_exists()` function is a unit test that checks the existence of the `censoror.py` file. It verifies the file's presence at a specified path, failing with a message if absent. This ensures the critical `censoror.py` is correctly located within the project.

- ## test_censor_names() :
  The `test_censor_names()` function tests the `censor_info()` method in the censoror module to ensure it effectively censors names in a text. It checks whether "John Doe" is replaced with censorship characters ("█") of the same length, confirming the method's capability to obscure names without altering text length. The test verifies the accuracy of name censorship, ensuring personal information is securely hidden within the text.

- ## test_censor_phone_numbers() :
  The `test_censor_phone_numbers()` function tests the `censor_info()` function in the `censoror` module to ensure it can censor phone numbers correctly in a given text. It checks if the first three digits of a phone number are replaced with censorship characters ("█"), while the rest of the number remains uncensored. This test case verifies that the function can selectively obscure parts of a phone number, demonstrating its precision in handling sensitive data within text content.

- ## test_censor_dates() :
  The `test_censor_dates()` function tests the functionality of the `censor_info()` function from the censoror module, specifically focusing on its ability to censor dates within a text. By utilizing unittest.mock.patch to mock the behavior of the language_processor, this test simulates the identification of a date entity within a sample text and verifies that the censor_info function replaces the identified date with the appropriate number of censorship characters ("█"). The goal is to ensure that dates are accurately detected and obscured, demonstrating the function's capability to protect date information in text data.

- ## test_censor_address() :
  The `test_censor_address()` function tests the functionality of the `censor_info()` function from the censoror module, with a focus on its capability to conceal parts of an address within a given string. By setting specific entity types to censor ('ORG', 'FAC', and 'GPE'), the test verifies if the function effectively censors components of an address—like street names and city names—while leaving other parts, such as numerical addresses, uncensored. This test checks for the presence of both censored and uncensored parts in the processed text to confirm the function's precision in selectively obscuring address details as defined by the entity types.

# Bugs and Assumptions :
During the development of the text censoring project, several challenges and assumptions were encountered, particularly in the aspects of natural language processing, text pattern recognition, and system integration:

- ## Spacy Model Loading:
  One critical assumption was that the Spacy language model en_core_web_md would be available and correctly installed in the execution environment. This assumption led to errors in environments where the model was not pre-installed, necessitating error handling to download the model if not found.

- ## Text Entity Recognition:
  The project relies heavily on SpaCy's named entity recognition (NER) to identify and censor specific types of entities like names, dates, addresses, and phone numbers. It was assumed that SpaCy's NER would accurately identify these entities across various text formats and structures. However, inaccuracies in entity recognition were observed due to NER model limitations, leading to either over-censoring or under-censoring of text.

- ## Phone Number Recognition:
  The regular expression for phone number recognition was designed to match a wide range of phone number formats. However, this approach assumed a standardization that does not always apply, especially in informal texts or texts with non-standard phone number representations, leading to missed or incorrect censoring.

- ## Performance on Large Texts:
  Initial assumptions did not fully consider the performance implications of processing very large text files. As a result, the first versions of the project did not optimize for memory usage or execution time, which could lead to inefficient processing for bulk censoring tasks.

- ## Unicode and Encoding Issues:
  Assumptions were made about text encoding, particularly assuming UTF-8 encoding for all input and output. This did not account for texts with different encodings or special characters that could lead to errors or unexpected behavior in text processing.


Overall, the project highlighted the importance of considering a wide range of scenarios and edge cases in text processing applications, particularly those involving natural language understanding and user interaction through command-line interfaces. Continuous testing was crucial in identifying and addressing these issues.









