from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, jsonify
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, BooleanField, RadioField, IntegerField, FormField, SubmitField
from wtforms.validators import InputRequired, Email, DataRequired
from wtforms.fields.html5 import EmailField

app = Flask(__name__)


@app.route('/home')
def dashboard():
    return render_template('home.html')

#register class
class RegisterForm(Form):
    name = StringField('Name:', [validators.DataRequired(),validators.Length(min=1, max=50)])
    email = EmailField('Email:', validators=[DataRequired()])    
    phone = StringField('Phone', validators=[DataRequired()])      
    age = StringField('Age:', [validators.DataRequired(),validators.Length(min=2, max=2)])
    Gender = RadioField('Gender:', choices=[('M','Male'),('F','Female'),('O','Other')], validators= [InputRequired()])
    terms_conditions = BooleanField('Agree to terms and conditions')


@app.route('/', methods=['GET', 'POST'])
def register():
    try:
        form = RegisterForm(request.form)
        if request.method =='POST' and form.validate():                      
            
            age = form.age.data           
            

            flash('Validation successful','success')

            return redirect(url_for('http://jsonplaceholder.typicode.com/photos/'+age))
        return render_template('register.html', form=form)
    except Exception as e:
        print(e)
        # return not_found()
        flash('Some error occured','danger')

        return render_template('register.html', form=form)


#error handler
@app.errorhandler(404)
def not_found(error = None):
    
    message='Not Found '+request.url

    resp = message    

    return resp
	
		
if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True,host='0.0.0.0')

