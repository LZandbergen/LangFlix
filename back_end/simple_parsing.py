import pysrt
import translate as tr
import spacy
import re
from wordfreq import zipf_frequency
import time
from os import path
from distractor_words import get_alternate_words
import json

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

    # Casefold lowers the word, but also changes certain letters to give more results
    lowered_word = word.casefold()
    return any(lowered_word in text.casefold() for text in strings)

def parse_subtitle_text(sub):
    expression = re.compile("[\(\<].*?[\)\>]")
    new = expression.sub("", sub.text)
    return new

def process_subtitles(x_subs, en_subs, language_abbreviation, distractor_file=False, save_file = "modified_moneyheist_s01e01.srt"):
    nlp, translator = load_parser(target_language=language_abbreviation)
    word_freq_dict = dict()
    noun_translations = []
    word_translation_dict = dict()

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

                # Search for subtitles in foreign file around that time
                subs = x_subs.slice(starts_after=en_sub.start -
                                    2000, ends_before=en_sub.end + 2000)
                
                # if not is_word_spoken(subs, x_word):
                #     print(f"word:{en_word_str}, translation:{x_word}, x_subs_index: {[item.index for item in subs]}")

                # Adds a word with its frequency to the dictionary if it is an actual translation
                if (en_word_str != "unknown" and len(x_word) > 1 and
                        en_word_str != x_word and " " not in x_word and is_word_spoken(subs, x_word)):
                    
                    #Zipf frequency is a number between 0 and 8 (0.0 if there is no frequency for the word)
                    # See more at https://pypi.org/project/wordfreq/
                    word_frequency = zipf_frequency(x_word, language_abbreviation, wordlist='best', minimum=0.0)
                    word_freq_dict[x_word] = word_frequency
                    word_translation_dict[x_word] = en_word
                    noun_translations.append((x_word, en_word))

                    # Find distractor words to use for exercises
                    if distractor_file != False:
                        try:
                            distractors = get_alternate_words(frequency=word_frequency, sample_size=2, filename=distractor_file)
                            en_subs[i].text = en_text + f"###{en_word}:{x_word}:{word_frequency}:[{', '.join(distractors)}]###"
                        except:
                            en_subs[i].text = en_text + f"###{en_word}:{x_word}:{word_frequency}###"    
                    else:
                        #Adds information to the line in the srt file for processing
                        en_subs[i].text = en_text + f"###{en_word}:{x_word}:{word_frequency}###"    
    
    #Save modifications of added information to a new srt file
    # en_subs.save(path.join('back_end', save_file))
    en_subs.save(save_file)
    return word_freq_dict, noun_translations, word_translation_dict
    
def main():
    # x_location = "subtitles/GERMAN_How.to.Sell.Drugs.Online.Fast.S01E01.German.srt"
    # en_location = "subtitles/GERMAN_How.To.Sell.Drugs.Online.Fast.S01E01.English.srt"
    # foreign_language = "de"

    files_list = [#["subtitles/FRENCH_Détox_Off.the.Hook.French.S01E01.srt", "subtitles/FRENCH_Détox_Off.the.Hook.English.S01E01.srt", "fr", "FRENCH_Detox_S01E01_Dict_tran.json"],
        #["subtitles/FRENCH_Détox_Off.the.Hook.French.S01E02.srt", "subtitles/FRENCH_Détox_Off.the.Hook.English.S01E02.srt", "fr", "FRENCH_Detox_S01E02_Dict_tran.json"],
        #["subtitles/GERMAN_How.to.Sell.Drugs.Online.Fast.S01E01.German.srt", "subtitles/GERMAN_How.To.Sell.Drugs.Online.Fast.S01E01.English.srt", "de", "GERMAN_Drugs_Online_S01E01_Dict_tran.json"],
        ["subtitles/GERMAN_How.to.Sell.Drugs.Online.Fast.S01E02.German.srt", "subtitles/GERMAN_How.To.Sell.Drugs.Online.Fast.S01E02.English.srt", "de", "GERMAN_Drugs_Online_S01E02_Dict_tran.json"],
        ["subtitles/SPANISH_Machos.Alfa.Spanish.S01E01.srt", "subtitles/SPANISH_Machos.Alfa.English.S01E01.srt", "es", "SPANISH_Machos_Alpha_S01E01_Dict_tran.json"],
        ["subtitles/SPANISH_Machos.Alfa.Spanish.S01E02.srt", "subtitles/SPANISH_Machos.Alfa.English.S01E02.srt", "es", "SPANISH_Machos_Alpha_S01E02_Dict_tran.json"]]
    
    for x_location, en_location, foreign_language, distractor_file in files_list:
        # Time when starting the run, to determine how long it took at the end
        start = time.time()

        save_location = x_location.split("/")[1]

        # foreign_language = 'es'
        x_subs, en_subs = load_subtitles(x_location, en_location) #x refers to the foreign language
        word_freq_dict, noun_translations, word_translation_dict = process_subtitles(x_subs, en_subs, foreign_language, distractor_file=distractor_file, save_file=f"subtitles/MODIFIED_{save_location}")
        
        print("Dictionary with word frequencies\n", word_freq_dict)
        print("\nList of nouns and their translations\n", noun_translations)
        print("Dictionary with word translations = \n", word_translation_dict)

        for key, value in word_translation_dict.items():
            word_translation_dict[key] = str(value)

        with open(distractor_file, "w") as outfile:
            json.dump(word_translation_dict, outfile)
        # Determine how long the script took to run
        end = time.time()
        total_time = end - start
        print("\n Time it took to run:" + str(total_time))

if __name__ == "__main__":
    main()