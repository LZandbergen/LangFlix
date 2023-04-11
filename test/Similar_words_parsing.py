import pysrt as srt
import translate as tr
import spacy
import re

sp_nlp = spacy.load("es_core_news_md")
en_nlp = spacy.load("en_core_web_md")

en_file = "Money.Heist.S01E01.XviD-AFG-eng.srt"
sp_file = "La.casa.de.papel.S01E01.WEBRip.Netflix.srt"

en_subs = srt.open(en_file)
sp_subs = srt.open(sp_file)

# Create a list to store common words between English and Spanish subtitles
common_words = []

# Create a translator object using the translate package
translator = tr.Translator(to_lang="en")

# Set buffer (in milliseconds) around start and end times of each English subtitle when trying to find matching Spanish subtitles
buffer = 500

# Set maximum number of similar words to check for each translated Spanish word
max_similar_words = 3

# Loop through each English subtitle line
for en_sub in en_subs:
    # Remove any text within brackets or angle brackets from subtitle text
    en_text = re.sub("[\(\<].*?[\)\>]", "", en_sub.text)

    # Use spaCy to tokenize and tag parts of speech for each subtitle line
    en_doc = en_nlp(en_text)

    # Find Spanish subtitles that are spoken within a similar timeframe (plus/minus buffer) as the current English subtitle
    matching_sp_subs = [sub for sub in sp_subs if sub.start <= en_sub.end.shift(milliseconds=buffer) and sub.end >= en_sub.start.shift(milliseconds=-buffer)]

    # Concatenate text from all matching Spanish subtitles
    sp_text = " ".join([re.sub("[\(\<].*?[\)\>]", "", sub.text) for sub in matching_sp_subs])

    # Use spaCy to tokenize and tag parts of speech for concatenated Spanish subtitle text
    sp_doc = sp_nlp(sp_text)

    # Find common words between English and Spanish subtitles by translating Spanish words to English, finding their base form (lemma), and checking semantically similar words against the English subtitles
    for token in sp_doc:
        translation_lemma = en_nlp(translator.translate(token.text).lower())[0].lemma_
        translation_token_vector_id=en_nlp.vocab.vectors.key2row[en_nlp.vocab.strings[translation_lemma]]
        most_similar=en_nlp.vocab.vectors.most_similar(translation_token_vector_id.reshape(1,-1),n=max_similar_words)
        most_similar_words=[en_nlp.vocab.strings[w] for w in most_similar[0][0]]
        if any([w in [t.lemma_ for t in en_doc] for w in most_similar_words]):
            common_words.append(translation_lemma)

# Rank common words by their frequency of occurrence in the Spanish language using spaCy's built-in word frequency data
ranked_words = sorted(common_words, key=lambda x: -sp_nlp.vocab[x].prob)

# Print ranked list of common words between English and Spanish subtitles (after translation, lemmatization, and checking semantically similar words)
print(ranked_words)