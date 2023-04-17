import pysrt as srt
import translate as tr
import spacy
import re
from wordfreq import zipf_frequency

en_nlp = spacy.load("en_core_web_sm")
en_file = "Money.Heist.S01E01.XviD-AFG-eng.srt"
en_subs = srt.open(en_file)

translator = tr.Translator(to_lang="es")

for en_sub in en_subs[0:50]:
    expression = re.compile("[\(\<].*?[\)\>]")
    en_text = expression.sub("", en_sub.text)
    en_doc = en_nlp(en_text)

    for word in en_doc:
        if word.pos_ == "NOUN":
            translation = translator.translate(str(word))
            print(word, translation)

# Returns a word's zipf frequency in a certain langauge, as a number between 0 and 8
# Returns 0.0 if there is no frequency for the word
def get_word_frequency(word, language):
    supported_languages = ['en' , 'es', 'fr', 'nl'] #see more at https://pypi.org/project/wordfreq/
    if language not in supported_languages:
        raise ValueError("Given language {} isn't supported".format(language))
    word_freq = zipf_frequency(word, language, wordlist= 'best' , minimum = 0.0)
    return word_freq
print(get_word_frequency('dinero' , 'es'))
