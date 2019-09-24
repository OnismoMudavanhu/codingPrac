from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, jsonify
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, BooleanField, RadioField, IntegerField, FormField, SubmitField
from wtforms.validators import InputRequired, Email, DataRequired
from wtforms.fields.html5 import EmailField
from passlib.hash import sha256_crypt
import json
import datetime
import time
import uuid
import pygal

#for api
import pymysql
from flask import jsonify
#from db_config import mysql
from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)

# config mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'brandprotector'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# init
mysql =MySQL(app)

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

    # submit = SubmitField("Send")
    

    # def validate_phone(form, field):
    #     if len(field.data) > 10:
    #         raise ValidationError('Phone must be less than 50 characters')

    # def validate_phone(form, field):
    #     if len(field.data) > 16:
    #         raise ValidationError('Invalid phone number.')
    #     try:
    #         input_number = phonenumbers.parse(field.data)
    #         if not (phonenumbers.is_valid_number(input_number)):
    #             raise ValidationError('Invalid phone number.')
    #     except:
    #             input_number = phonenumbers.parse("+1"+field.data)
    #             if not (phonenumbers.is_valid_number(input_number)):
    #                 raise ValidationError('Invalid phone number.')

#register 

@app.route('/', methods=['GET', 'POST'])
def register():
    try:
        form = RegisterForm(request.form)
        if request.method =='POST' and form.validate():                      
            
            age = form.age.data           

            # # Create cursor
            # cur = mysql.connection.cursor()
            # # execute query
            # cur.execute("INSERT INTO users(name, email,username,password) VALUES(%s,%s,%s,%s )",(name, email, username, password))

            # # commit to db
            # mysql.connection.commit()

            # # close connection
            # cur.close()

            flash('Validation successful','success')

            return redirect(url_for('http://jsonplaceholder.typicode.com/photos/'+age))
        return render_template('register.html', form=form)
    except Exception as e:
        print(e)
        # return not_found()
        flash('Some error occured','danger')

        return render_template('register.html', form=form)

# login
@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            # Get Form Fields
            username = request.form['username']
            password_candidate = request.form['password']

            # create cursor
            cur = mysql.connection.cursor()

            # Get user by username
            result = cur.execute("SELECT * FROM users WHERE username=%s", [username])

            if result > 0:
                # Get stored hash
                data = cur.fetchone()
                password = data['password']
                #thinking of using it to fill created_by field in products table
                admin_id = data['ID']
                # compare passwords
                if sha256_crypt.verify(password_candidate, password):
                    # passed
                    session['logged_in'] =True
                    session['username'] = username
                    session['ID'] = admin_id

                    flash('You are now logged in as '+ session['username'], 'success')
                    # to check if i managed to get the user id flash(admin_id,'success')
                    return redirect(url_for('dashboard'))
                else:
                    error = 'Invalid login'
                    return render_template('login.html', error=error)

                    # close conn
                    cur.close()
            else:
                error = 'Username not found'
                return render_template('login.html', error = error)
                
        return render_template('login.html')
    except Exception as e:
        print(e)
        return not_found()


#error handler
@app.errorhandler(404)
def not_found(error = None):
    
    message='Not Found '+request.url

    resp = message
    

    return resp

		
		
if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True,host='0.0.0.0')

