'''
Sentence Uncommonifier
By Justin Sun(@host008 on github)

takes a sentence and replaces all the common words with uncommon words

thats about it

test sentence: "The quick brown fox jumps over the lazy dog"
'''
# imports

# from py_thesaurus import Thesaurus(no longer works)
from nltk.corpus import wordnet
import nltk
from wordfreq import word_frequency
import logging

# nltk setup
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('omw-1.4')

# words to ignore
ignore_words = 'a an the and but or for of at i'.split(' ')
# functions
'''
def find_uncommon_synonym(word: str) -> str:
    try:
        thesaurus = Thesaurus(word)
        thesaurus_entries: list = thesaurus.get_synonyms()
    except:
        return word # if the word is not in the thesaurus, return the word
    if len(thesaurus_entries) < 1: # if the word has no synonyms, return the word
        return word
    else:
        least_common_word: str = word
        for entry in thesaurus_entries:
            if word_frequency(entry, 'en') < word_frequency(least_common_word, 'en'):
                least_common_word = entry
        return least_common_word
'''
def convert_pos(pos: str) -> str:
    if pos == 'JJ':
        return wordnet.ADJ
    elif pos == 'NN':
        return wordnet.NOUN
    elif pos == 'RB':
        return wordnet.ADV
    elif pos == 'VB':
        return wordnet.VERB
    else:
        return ''
def find_uncommon_synonym(word: str, context: str) -> str:
    
    synonyms: list = []
    partofspeech: str = ''
    
    # find the part of speech of the word
    nltk_tokens: list = nltk.word_tokenize(context)
    nltk_tags: list = nltk.pos_tag(nltk_tokens)
    nltk_tags_dict: dict = dict(nltk_tags)
    if word in nltk_tags_dict:
        partofspeech = nltk_tags_dict[word]
    
    for syn in wordnet.synsets(word, pos=convert_pos(partofspeech)):
        for l in syn.lemmas():
            synonyms.append(l.name())
        
    
    if word in ignore_words: # if the word is in the ignore list, return the word
        return word
    
    else:
        if len(synonyms) < 1: # if the word has no synonyms, return the word
            return word
        
        elif len(synonyms) == 1: # if the word has only one synonym, return the synonym
            return synonyms[0].replace('_', ' ')
        
        else:
            least_common_word: str = word
            for synonym in synonyms:
                if word_frequency(synonym, 'en') < word_frequency(least_common_word, 'en'):
                    least_common_word = synonym
            return least_common_word.replace('_', ' ')

def uncommonify_sentence(sentence: str) -> str:
    words: list = sentence.split(' ')
    uncommonified_words: list = []
    for word in words:
        uncommonified_words.append(find_uncommon_synonym(word, sentence))
    return ' '.join(uncommonified_words)

# main
if __name__ == '__main__':
    sentence: str = input('Enter a sentence: ')
    print(uncommonify_sentence(sentence))