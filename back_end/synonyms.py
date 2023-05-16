import json
import pysrt
import spacy
import re
from wordfreq import zipf_frequency
import random

def get_alternate_words(frequency=5.0, tolerance=0.2, sample_size=3, filename="/home/lzandbergen/Documents/NML/LangFlix/back_end/nouns_dict.json"):
    with open(filename) as f:
        synonyms = json.load(f)
    
    keys_within_range = []
    for key, value in synonyms.items():
        if abs(value - frequency) <= tolerance:
            keys_within_range.append(key)

    return random.sample(keys_within_range, sample_size)

def parse_subtitle_text(sub):
    expression = re.compile("[\(\<].*?[\)\>]")
    return expression.sub("", sub.text)

def create_dictionary(language='es', filename="/home/lzandbergen/Documents/NML/LangFlix/back_end/La.casa.de.papel.S01E01.WEBRip.Netflix.srt"):
    subs = pysrt.open(filename)
    noun_dict = {}
    if language == "es":
        nlp = spacy.load("es_core_news_sm")
    
    for sub in subs:
        text = parse_subtitle_text(sub)
        doc = nlp(text)
        for word in doc:
            if word.pos_ == "NOUN" and not word.text.isupper():
                string = word.text.lower()
                noun_dict[string] = zipf_frequency(string, language, wordlist='best', minimum=0.0)
    
    with open("nouns_dict.json", 'w') as file:
        json.dump(noun_dict, file)

print(get_alternate_words())
