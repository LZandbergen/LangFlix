from wordfreq import word_frequency
from wordfreq import zipf_frequency
from wordfreq import get_frequency_dict

# Returns a word's zipf frequency in a certain langauge, as a number between 0 and 8
# Returns 0.0 if there is no frequency for the word
def get_word_frequency(word, language):
    supported_languages = ['en' , 'es', 'fr', 'nl'] #see more at https://pypi.org/project/wordfreq/
    if language not in supported_languages:
        raise ValueError("Given language {} isn't supported".format(language))
    word_freq = zipf_frequency(word, language, wordlist= 'best' , minimum = 0.0)
    return word_freq
print(get_word_frequency('dinero' , 'es'))

# Get a dictionary of word frequencies for the Spanish language
dict = get_frequency_dict('es', wordlist='best')
print(len(dict))

#Doesn't work yet!
#Get a word that belongs to a frequency 
test_f = 1.0232929922807536e-08
words = [k for k, v in dict.items() if v == test_f]
#print(words)