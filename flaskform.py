# all the imports

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

from wtforms import Form, BooleanField, TextField, PasswordField, validators, TextAreaField

from sklearn.externals import joblib

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

WTF_CSRF_ENABLED = True
app.secret_key = 'you-will-never-guess'

class corpus(Form):
    corpustext = TextAreaField()

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

@app.route('/')
@app.route('/flaskform', methods=['GET', 'POST'])
def flaskform(name=None):
    session.clear()
    form = corpus()
    clf = joblib.load('pickle/doc_tagger.pkl')

    if request.method == 'POST':
    	base_text = request.form['corpustext'] 
    	extracted_text = sorted(uniq(get_entitylist(np.array([base_text]),0)))
    	tagged_text = clf.predict(np.array([base_text]))
    	session['base_text'] = base_text
    	session['extracted_text'] = extracted_text
    	session['tagged_text'] = tagged_text
    	return redirect(url_for('output', base_text=base_text, extracted_text=extracted_text, tagged_text=tagged_text))
    return render_template('flaskform.html', 
                           title='flaskform',
                           form=form)

@app.route('/output', methods=['GET', 'POST'])
def output():
	base_text = session['base_text']
	extracted_text = (session['extracted_text'])
	tagged_text = (session['tagged_text'])
	return render_template('output.html', title='flaskform', base_text=base_text, extracted_text=extracted_text, tagged_text=tagged_text)
                         
app.debug = True            
                           
if __name__ == '__main__':
    app.run()