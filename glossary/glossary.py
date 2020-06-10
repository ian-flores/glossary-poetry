from yaml import load, FullLoader
from textdistance import cosine
from pkg_resources import resource_stream

stream = resource_stream(__name__, 'data/glossary.yml')
raw = load(stream, Loader=FullLoader)
Terms = {term['slug']: term for term in raw}

__language__ = 'en'

def get_languages_available():
    lang_dict = {}

    for term in Terms.items():
        keys = list(term[1].keys())
        for key in keys:
            if key != 'slug' and key != 'ref':
                try:
                    lang_dict[key] =  lang_dict[key] + 1
                except KeyError:
                    lang_dict[key] = 1
                except:
                    print('Error in getting languages')

    return lang_dict

def set_language(language, verbose=False):
    langs_available = get_languages_available()

    if language not in langs_available.keys():
        if verbose:
            print('Currently we don\'t support this language.\nFeel free to submit definitions to this language at https://github.com/gvwilson/glossary')
        return None
    else:
        global __language__
        if verbose:
            print(f'Current Language: {__language__}\nNew Language: {language}')
        __language__ = language

def __search_word__(slug):
    '''Look up a definition in a glossary by slug.'''
    definition = Terms.get(slug)
    return definition.get(__language__)

def __known_words__():
    '''Report all known definition slugs as a set.'''
    return Terms.keys()

def __search_similar_word__(slug):
    similarity_dict = {}

    for term in __known_words__():
        similarity_dict[term] = cosine.normalized_similarity(slug, term)
    
    return max(similarity_dict, key = similarity_dict.get)

def define(slug):
    try:
        similar_word = __search_similar_word__(slug)
        word_definition = __search_word__(similar_word)
        
        return word_definition['def']
    except:
        print('We couldn\'t find this word in the dictionary')