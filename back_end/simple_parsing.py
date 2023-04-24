import pysrt as srt
import translate as tr
import spacy
import re
from wordfreq import zipf_frequency
import time
# Time when starting the run, to determine how long it took at the end
start = time.time()


def load_parser(target_language="es", native_language="en"):
    """ Loads NLP parser and translator object, input should be string of language code.
    Returns nlp object and translator object """
    if native_language == "en":
        nlp = spacy.load("en_core_web_sm")
    translator = tr.Translator(to_lang=target_language)
    return nlp, translator


def load_subtitles(target_language_file="La.casa.de.papel.S01E01.WEBRip.Netflix.srt", native_language_file="Money.Heist.S01E01.XviD-AFG-eng.srt"):
    """ Inputs: paths to srt subtitle files for language parsing
     Output: Target subtitle file, Native subtitle file """
    try:
        native_subs = srt.open(native_language_file)
    except:
        print("native language subtitle file does not exist")
        return 0

    try:
        target_subs = srt.open(target_language_file)
    except:
        print("target language subtitle file does not exist")
        return 0

    return target_subs, native_subs


word_freq_dict = dict()
noun_translations = []

# Returns a word's zipf frequency in a certain langauge, as a number between 0 and 8
# Returns 0.0 if there is no frequency for the word


def get_word_frequency(word, language):
    # see more at https://pypi.org/project/wordfreq/
    supported_languages = ['en', 'es', 'fr', 'nl', 'de']
    if language not in supported_languages:
        raise ValueError("Given language {} isn't supported".format(language))
    word_freq = zipf_frequency(word, language, wordlist='best', minimum=0.0)
    return word_freq


def is_word_spoken(subs, word):
    if len(subs) == 0:
        return False
    else:
        strings = [sub.text for sub in subs]
    return any(word in text for text in strings)

nlp, translator = load_parser()
en_subs, sp_subs = load_subtitles()

for en_sub in en_subs:
    expression = re.compile("[\(\<].*?[\)\>]")
    en_text = expression.sub("", en_sub.text)
    en_doc = nlp(en_text)

    # Looks for English words that are nouns and creates data to work with
    for en_word in en_doc:
        # print(en_word)
        if en_word.pos_ == "NOUN" and not en_word.text.isupper():
            en_word_str = en_word.text.lower()
            # returns string of translation of en word
            sp_word = translator.translate(en_word.text).lower()

            # Removes extra information in parentheses after the translation
            if " (" in sp_word:
                sp_word = sp_word[0: sp_word.index(" (")]
                print(" REMOVED (  ", sp_word)

            # Search for subtitles in spanish file around that time
            subs = sp_subs.slice(starts_after=en_sub.start -
                                 2000, ends_before=en_sub.end + 2000)

            # Adds a word with its frequency to the dictionary if it is an actual translation
            if (en_word_str != "unknown" and len(sp_word) > 1 and
                    en_word_str != sp_word and " " not in sp_word and is_word_spoken(subs, sp_word)):
                word_frequency = get_word_frequency(sp_word, 'es')
                word_freq_dict[sp_word] = word_frequency
                noun_translations.append((sp_word, en_word))

print("Dictionary with word frequencies\n", word_freq_dict)
print("\nList of nouns and their translations\n", noun_translations)

# Determine how long the script took to run
end = time.time()
total_time = end - start
print("\n Time it took to run:" + str(total_time))
