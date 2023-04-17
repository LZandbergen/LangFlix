import pysrt as srt
import translate as tr
import spacy
import re
from wordfreq import zipf_frequency
import time
# Grab Currrent Time Before Running the Code
start = time.time()

en_nlp = spacy.load("en_core_web_sm")
en_file = "Money.Heist.S01E01.XviD-AFG-eng.srt"
en_subs = srt.open(en_file)

translator = tr.Translator(to_lang="es")
word_freq_dict = dict()
noun_translations = []

# Returns a word's zipf frequency in a certain langauge, as a number between 0 and 8
# Returns 0.0 if there is no frequency for the word
def get_word_frequency(word, language):
    supported_languages = ['en' , 'es', 'fr', 'nl'] #see more at https://pypi.org/project/wordfreq/
    if language not in supported_languages:
        raise ValueError("Given language {} isn't supported".format(language))
    word_freq = zipf_frequency(word, language, wordlist= 'best' , minimum = 0.0)
    return word_freq

for en_sub in en_subs[0:50]:
    expression = re.compile("[\(\<].*?[\)\>]")
    en_text = expression.sub("", en_sub.text)
    en_doc = en_nlp(en_text)

    for en_word in en_doc:
        if en_word.pos_ == "NOUN":
            en_word_str = en_word.text.lower()
            sp_word = translator.translate(en_word.text).lower() #returns string of translation of en word

            #Removes extra information in parentheses after the translation
            if " ("  in sp_word:
                sp_word = sp_word[ 0 : sp_word.index(" (")]
                print(" REMOVED (  ", sp_word)

            #Adds a word with its frequency to the dictionary if it is an actual translation
            if (en_word_str != "unknown" and len(sp_word) > 1 and 
                en_word_str != sp_word and " " not in sp_word):
                word_frequency = get_word_frequency(sp_word, 'es')
                word_freq_dict[sp_word] = word_frequency
                noun_translations.append((sp_word, en_word_str))

print("Dictionary with word frequencies\n", word_freq_dict)
print("\nList of nouns and their translations\n", noun_translations)

# Grab Currrent Time After Running the Code
end = time.time()

#Subtract Start Time from The End Time
total_time = end - start
print("\n Time it took to run:"+ str(total_time))