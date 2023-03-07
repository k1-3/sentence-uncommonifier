'''
Sentence Uncommonifier
By Justin Sun(@host008 on github)(This is an alt)

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
import random
# nltk setup
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('omw-1.4')

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
def find_uncommon_synonym(word: str, context: str, randomness: int = 0) -> str:
    
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
        
    else:
        if len(synonyms) < 1: # if the word has no synonyms, return the word
            return word
        
        elif len(synonyms) == 1: # if the word has only one synonym, return the synonym
            return synonyms[0].replace('_', ' ')
        
        else:
            sorted_list_by_rarity: list = [word]
            for synonym in synonyms:
                if word_frequency(synonym, 'en') < word_frequency(sorted_list_by_rarity[0], 'en'): # if the synonym is less common than the first word in the list, insert it at the beginning
                    sorted_list_by_rarity.insert(0, synonym)
                elif word_frequency(synonym, 'en') > word_frequency(sorted_list_by_rarity[-1], 'en'): # if the synonym is more common than the last word in the list, append it to the end
                    sorted_list_by_rarity.append(synonym)
                else:
                    for i in range(len(sorted_list_by_rarity)):
                        if word_frequency(synonym, 'en') > word_frequency(sorted_list_by_rarity[i], 'en'): # if the synonym is more common than the word at the current index, insert it at the current index
                            sorted_list_by_rarity.insert(i, synonym)
                            break
            if randomness == 0:
                return sorted_list_by_rarity[0].replace('_', ' ')
            if randomness > len(sorted_list_by_rarity):
                return sorted_list_by_rarity[random.randint(0, len(sorted_list_by_rarity) - 1)].replace('_', ' ') # Edge case: if the randomness is greater than the length of the list, return a random word from the list
            else:
                return sorted_list_by_rarity[random.randint(0, len())].replace('_', ' ')
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
    
    
