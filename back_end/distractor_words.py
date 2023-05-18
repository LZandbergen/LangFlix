import json
import pysrt
import spacy
import re
from wordfreq import zipf_frequency
import random


def get_alternate_words(frequency=5.0, tolerance=0.2, sample_size=3, filename="/home/lzandbergen/Documents/NML/LangFlix/back_end/nouns_dict.json"):
    # Load synonyms from the JSON file
    with open(filename) as f:
        synonyms = json.load(f)

    keys_within_range = []
    # Iterate over each key-value pair in the synonyms dictionary
    for key, value in synonyms.items():
        # Check if the absolute difference between the value and target frequency is within the tolerance
        if abs(value - frequency) <= tolerance:
            keys_within_range.append(key)

    # Return a random sample of keys within the desired frequency range
    return random.sample(keys_within_range, sample_size)


def parse_subtitle_text(sub):
    # Remove expressions within parentheses or angle brackets from the subtitle text
    expression = re.compile("[\(\<].*?[\)\>]")
    return expression.sub("", sub.text)


def create_dictionary(language='es', file_name="back_end/La.casa.de.papel.S01E01.WEBRip.Netflix.srt", save_name="subtitles/distractor_dict.json"):
    # Open the subtitle file
    subs = pysrt.open(file_name)
    # Create an empty dictionary to store nouns and their frequencies
    noun_dict = {}
    if language == "es":
        # Load the Spanish language model for spaCy
        nlp = spacy.load("es_core_news_sm")
    elif language == 'de':
        nlp = spacy.load("de_core_news_sm")
    elif language == 'fr':
        nlp = spacy.load("fr_core_news_sm")

    expression = re.compile("[\(\<].*?[\)\>]")

    for sub in subs:
        # Extract the subtitle text and remove expressions within parentheses or angle brackets
        text = expression.sub("", sub.text)
        # Process the subtitle text with spaCy
        doc = nlp(text)
        for word in doc:
            # Check if the word is a noun and not in uppercase
            if word.pos_ == "NOUN" and not word.text.isupper():
                string = word.text.lower()
                # Store the noun and its Zipf frequency in the dictionary
                noun_dict[string] = zipf_frequency(
                    string, language, wordlist='best', minimum=0.0)

    # Dump the noun dictionary to a JSON file
    print(noun_dict)
    print(f"dictionary length: {len(noun_dict)}")
    with open(save_name, 'w') as file:
        json.dump(noun_dict, file)


files_list = [["fr", "subtitles/FRENCH_Détox_Off.the.Hook.French.S01E01.srt", "FRENCH_Detox_S01E01_Dict.json"],
              ["fr", "subtitles/FRENCH_Détox_Off.the.Hook.French.S01E02.srt", "FRENCH_Detox_S01E02_Dict.json"],
              ["de", "subtitles/GERMAN_How.to.Sell.Drugs.Online.Fast.S01E01.German.srt", "GERMAN_Drugs_Online_S01E01_Dict.json"],
              ["de", "subtitles/GERMAN_How.to.Sell.Drugs.Online.Fast.S01E02.German.srt", "GERMAN_Drugs_Online_S01E02_Dict.json"],
              ["es", "subtitles/SPANISH_Machos.Alfa.Spanish.S01E01.srt", "SPANISH_Machos_Alpha_S01E01_Dict.json"],
              ["es", "subtitles/SPANISH_Machos.Alfa.Spanish.S01E02.srt", "SPANISH_Machos_Alpha_S01E02_Dict.json"]]

# for language, file_name, save_name in files_list:
create_dictionary("es", "subtitles/SPANISH_Machos.Alfa.Spanish.S01E02.srt", "SPANISH_Machos_Alpha_S01E02_Dict.json")