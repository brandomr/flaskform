# all the imports

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

from wtforms import Form, BooleanField, TextField, PasswordField, validators, TextAreaField

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)



class corpus(Form):
    text = TextAreaField()

@app.route('/')
@app.route('/flaskform', methods=['GET', 'POST'])
def flaskform(name=None):
    form = corpus()
    return render_template('flaskform.html', 
                           title='flaskform',
                           form=form)
                           
app.debug = True            
                           
if __name__ == '__main__':
    app.run()