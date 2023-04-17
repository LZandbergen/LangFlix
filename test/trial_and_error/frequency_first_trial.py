from wordfreq import word_frequency
from wordfreq import get_frequency_dict

# Calculate the frequency of the word 'dinero' in the Spanish language
f = word_frequency('dinero', 'es', wordlist='best', minimum=0.0)
print(f)

# Get a dictionary of word frequencies for the Spanish language
dict = get_frequency_dict('es', wordlist='best')
print(len(dict))

#Doesn't work yet!
#Get a word that belongs to a frequency 
test_f = 1.0232929922807536e-08
words = [k for k, v in dict.items() if v == test_f]
print(words)