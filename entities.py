import nltk
import numpy as np
#tokenizes and chunks for entity extraction
def extract_entities(text):
    entities = []
    for sentence in nltk.sent_tokenize(text):
        #tokenizes into sentence
        
        chunks = nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sentence)))
        #tokenizes into words, then tags by parts of speech, then uses nltk's built in chunker
        
        entities.extend([chunk for chunk in chunks if hasattr(chunk, 'node')])
        #iterates through the text and pulls any chunks that are nodes--these are the entities
        
    return entities

#function takes two arguments, a list and the item you want entities for in that list. For example, with this corpora, select a given
#item i for analysis--in this case i is just a document in the doc library already brought in
def get_entitylist(list, i):
    entitylist = []
    for entity in extract_entities(list[i]):
        #calls extract_entities on the given text
        item = '[' + entity.node + '] ' + ' '.join(c[0] for c in entity.leaves())
        #gets the entity node type and joins it with the leaf--basically the entity name in this case
        entitylist.append(item)
        #appends to the entitylist object
    return entitylist

#prints each item in a list on it's own line
def printbyline(list):
    for item in list:
        print item
        
#uniq is a function to return only unique items for a given list
def uniq(input):
    output = []
    for x in input: 
        if x not in output:
            output.append(x)
    return output