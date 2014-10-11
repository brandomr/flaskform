# all the imports

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

from wtforms import Form, BooleanField, TextField, PasswordField, validators, TextAreaField

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

WTF_CSRF_ENABLED = True
app.secret_key = 'you-will-never-guess'

class corpus(Form):
    corpustext = TextAreaField()

@app.route('/')
@app.route('/flaskform', methods=['GET', 'POST'])
def flaskform(name=None):
    form = corpus()
    if request.method == 'POST':
    	base_text = request.form['corpustext'] 
    	manipulated_text = len(base_text)
    	session['base_text'] = base_text
    	session['manipulated_text'] = manipulated_text
    	return redirect(url_for('output', base_text=base_text, manipulated_text=manipulated_text))
    return render_template('flaskform.html', 
                           title='flaskform',
                           form=form)

@app.route('/output', methods=['GET', 'POST'])
def output():
	base_text = session['base_text']
	manipulated_text = session['manipulated_text']
	return render_template('output.html', title='flaskform', base_text=base_text, manipulated_text=manipulated_text)
                         
app.debug = True            
                           
if __name__ == '__main__':
    app.run()