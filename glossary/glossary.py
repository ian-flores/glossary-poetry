import os
import yaml
import textdistance

with open(os.path.join(os.path.dirname(__file__), 'glossary.yml'), 'r') as reader:
    raw = yaml.load(reader, Loader=yaml.FullLoader)
    Terms = {term['slug']: term for term in raw}
    

def search_word(slug):
    '''Look up a definition in a glossary by slug.'''
    return Terms.get(slug)

def known_words():
    '''Report all known definition slugs as a set.'''
    return Terms.keys()

def search_similar_word(slug):
    similarity_dict = {}

    for term in known_words():
        similarity_dict[term] = textdistance.cosine.normalized_similarity(slug, term)
    
    return max(similarity_dict, key = similarity_dict.get)

def define(slug):
    try:
        word_definition = search_word(slug)
        
        if word_definition is None:
            similar_word = search_similar_word(slug)
            word_definition = search_word(similar_word)
        
        return word_definition
    except:
        print('We couldn\'t find this word in the dictionary')