import pysrt as srt
import translate as tr
import spacy
import re

en_nlp = spacy.load("en_core_web_sm")
en_file = "Money.Heist.S01E01.XviD-AFG-eng.srt"
en_subs = srt.open(en_file)

translator = tr.Translator(to_lang="es")

for en_sub in en_subs[0:5]:
    expression = re.compile("[\(\<].*?[\)\>]")
    en_text = expression.sub("", en_sub.text)
    en_doc = en_nlp(en_text)

    for word in en_doc:
        if word.pos_ == "NOUN":
            translation = translator.translate(str(word))
            print(word, translation)


