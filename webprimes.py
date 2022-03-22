import time
from math import sqrt
from unicodedata import name
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config["SECRET_KEY"] = 'A3F22234FDFSF54342EAAA23'

bootstrap = Bootstrap(app)

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    upperlimit = IntegerField('Please enter an integer upper limit for the prime numbers search:', 
    validators=[DataRequired()])
    submit = SubmitField('Submit')

def PrimeNumberCalculation(n):
    start_time = time.time()
    if(n > 2):
        prime = [*range(2, n)]
        x = 2
        while (x * x < n):
            if (x < sqrt(n)):
                for i in range(x * x, n, x):
                    if i in prime:
                        prime.remove(i)
            x += 1
    
        number_of_elements = len(prime)
        return number_of_elements, prime, start_time

@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        form=NameForm()
        number_of_elements, primes, start_time = PrimeNumberCalculation(form.upperlimit.data)
        first10elements=primes[:10]
        last10elements=primes[-10:]
        if number_of_elements < 20:
            return render_template('form', name=form.name.data, 
            upperlimit=form.upperlimit.data, number_of_elements=number_of_elements, 
            primes=primes, runtime=(time.time() - start_time), form=form)
        else:
            return render_template('form_post_alt.html', name=form.name.data, 
            upperlimit=form.upperlimit.data, number_of_elements=number_of_elements,
            first10elements=first10elements, last10elements=last10elements,
            runtime=(time.time() - start_time), form=form)
    else:
        form = NameForm()
        return render_template('forms.html', form=form)

if __name__ == '__main__':
    app.debug = True
    app.run()