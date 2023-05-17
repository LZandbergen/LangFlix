import pysrt
import translate as tr
import spacy
import re
from wordfreq import zipf_frequency
import time
from os import path

def load_parser(target_language="es", native_language="en"):
    """ Loads NLP parser and translator object, input should be string of language code.
    Returns nlp object and translator object """
    if native_language == "en":
        nlp = spacy.load("en_core_web_sm")
    translator = tr.Translator(to_lang=target_language)
    return nlp, translator


def load_subtitles(target_language_file=path.join("back_end","La.casa.de.papel.S01E01.WEBRip.Netflix.srt"), native_language_file=path.join("back_end", "Money.Heist.S01E01.XviD-AFG-eng.srt")):
    """ Inputs: paths to srt subtitle files for language parsing
     Output: Target subtitle file, Native subtitle file """
    try:
        native_subs = pysrt.open(native_language_file)
    except:
        print("native language subtitle file does not exist")
        return 0

    try:
        target_subs = pysrt.open(target_language_file)
    except:
        print("target language subtitle file does not exist")
        return 0

    return target_subs, native_subs


def is_word_spoken(subs, word):
    if len(subs) == 0:
        return False
    else:
        strings = [sub.text for sub in subs]
    if any(word in text for text in strings) != any(word in sub.text for sub in subs):
        print(f"word: {word}", strings)
        print(any(word in text for text in strings))
        print(any(word in sub.text for sub in subs))
    return any(word in text for text in strings)

def parse_subtitle_text(sub):
    expression = re.compile("[\(\<].*?[\)\>]")
    return expression.sub("", sub.text)

def process_subtitles(x_subs, en_subs, language_abbreviation, save_file = "modified_moneyheist_s01e01.srt"):
    nlp, translator = load_parser(target_language=language_abbreviation)
    word_freq_dict = dict()
    noun_translations = []

    for i, en_sub in enumerate(en_subs):
        en_text = parse_subtitle_text(en_sub)
        en_doc = nlp(en_text)

        # Looks for English words that are nouns and creates data to work with
        for en_word in en_doc:
            # print(en_word)
            if en_word.pos_ == "NOUN" and not en_word.text.isupper():
                en_word_str = en_word.text.lower()
                # returns string of translation of en word in wanted foreign language x
                x_word = translator.translate(en_word.text).lower()

                # Removes extra information in parentheses after the translation
                if " (" in x_word:
                    x_word = x_word[0: x_word.index(" (")]

                # Search for subtitles in spanish file around that time
                subs = x_subs.slice(starts_after=en_sub.start -
                                    2000, ends_before=en_sub.end + 2000)

                # Adds a word with its frequency to the dictionary if it is an actual translation
                if (en_word_str != "unknown" and len(x_word) > 1 and
                        en_word_str != x_word and " " not in x_word and is_word_spoken(subs, x_word)):
                    
                    #Zipf frequency is a number between 0 and 8 (0.0 if there is no frequency for the word)
                    # See more at https://pypi.org/project/wordfreq/
                    word_frequency = zipf_frequency(x_word, language_abbreviation, wordlist='best', minimum=0.0)
                    word_freq_dict[x_word] = word_frequency
                    noun_translations.append((x_word, en_word))

                    #Adds information to the line in the srt file for processing
                    en_subs[i].text = en_text + f"###{en_word}:{x_word}:{word_frequency}###"
    
    #Save modifications of added information to a new srt file
    # en_subs.save(path.join('back_end', save_file))
    en_subs.save(save_file)
    return word_freq_dict, noun_translations
    
def main():
    # Time when starting the run, to determine how long it took at the end
    start = time.time()


    files_list = [["subtitles/FRENCH_Détox_Off.the.Hook.French.S01E01.srt", "subtitles/FRENCH_Détox_Off.the.Hook.English.S01E01.srt", "fr"],
     ["subtitles/GERMAN_How.to.Sell.Drugs.Online.Fast.S01E01.German.srt", "subtitles/GERMAN_How.To.Sell.Drugs.Online.Fast.S01E01.English.srt", "de"],
     ["subtitles/SPANISH_Machos.Alfa.Spanish.S01E01.srt", "subtitles/SPANISH_Machos.Alfa.English.S01E01.srt", "es"],]
    
    for x_location, en_location, foreign_language in files_list:
        
        # foreign_language = 'es' #supported languages = 'en', 'es', 'fr', 'nl', 'de'
        x_subs, en_subs = load_subtitles(x_location, en_location) #x refers to the foreign language
        word_freq_dict, noun_translations = process_subtitles(x_subs, en_subs, foreign_language, save_file=f"subtitles/{foreign_language}_modified.srt")
        
        print("Dictionary with word frequencies\n", word_freq_dict)
        print("\nList of nouns and their translations\n", noun_translations)

        # Determine how long the script took to run
        end = time.time()
        total_time = end - start
        print("\n Time it took to run:" + str(total_time))

if __name__ == "__main__":
    main()