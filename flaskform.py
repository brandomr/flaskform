#flask imports
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

#form imports
from wtforms import Form, BooleanField, TextField, PasswordField, validators, TextAreaField

#sci kit learn imports (for the classifier)
from sklearn.externals import joblib

#urllib for url encoding
import urllib 

#custom entity extraction file
import entities

#importing numpy to create array
import numpy as np


#create the application
app = Flask(__name__)
app.config.from_object(__name__)

#set up the secret key
WTF_CSRF_ENABLED = True
app.secret_key = 'you-will-never-guess'

#create a form called corpus with a text area called corpus text
class corpus(Form):
    corpustext = TextAreaField()


@app.route('/')
@app.route('/flaskform', methods=['GET', 'POST'])
def flaskform(name=None):
    
    #clears cookies so the same user can run n-times
    session.clear()
    
    #sets the form as the corpus form
    form = corpus()
    
    #unpickles the classifier as clf
    clf = joblib.load('pickle/doc_tagger.pkl')

    if request.method == 'POST':
    	base_text = request.form['corpustext'] 
    	extracted_text = sorted(entities.uniq(entities.get_entitylist(np.array([base_text]),0)))
    	tagged_text = clf.predict(np.array([base_text]))
    	session['base_text'] = urllib.quote_plus(base_text.encode('utf-8'))
    	session['extracted_text'] = extracted_text
    	session['tagged_text'] = tagged_text
    	return redirect(url_for('output', base_text=base_text, extracted_text=extracted_text, tagged_text=tagged_text))
    return render_template('flaskform.html', 
                           title='flaskform',
                           form=form)

@app.route('/output', methods=['GET', 'POST'])
def output():
	base_text = urllib.unquote_plus(session['base_text'].decode('utf-8'))
	print base_text
	extracted_text = (session['extracted_text'])
	tagged_text = (session['tagged_text'])
	return render_template('output.html', title='flaskform', base_text=base_text, extracted_text=extracted_text, tagged_text=tagged_text)
                         
app.debug = True            
                           
if __name__ == '__main__':
    app.run()