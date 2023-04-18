import wordfreq
import json
import pysrt as srt
import re
import spacy

sub_filename = "/home/lzandbergen/Documents/NML/LangFlix/test/La.casa.de.papel.S01E01.WEBRip.Netflix.srt"
nlp = spacy.load('es_core_news_sm')
LANGUAGE = 'es'

sub_file = srt.open(sub_filename)
word_dict = {}

for sub in sub_file:
    expression = re.compile("[\(\<].*?[\)\>]")
    en_text = expression.sub("", sub.text)
    doc = nlp(en_text)
    for word in doc:
        if len(word.text) > 1:
            freq = wordfreq.word_frequency(word.text, 'es')
            zipf = wordfreq.zipf_frequency(word.text, 'es')
            word_dict[word.text.lower()] = [freq, zipf]

json = json.dumps(word_dict)
with open(sub_filename + "dict", "w") as f:
    f.write(json)
