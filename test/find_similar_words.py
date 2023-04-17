import spacy

def get_similar_words(word):
    nlp = spacy.load('en_core_web_sm')
    word_token = nlp(word)
    similar_words = [w.text for w in word_token.similar_by_word()]
    return similar_words

doc = nlp("Hi, my name is Jack. Do you like my car")
