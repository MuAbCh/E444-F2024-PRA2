from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = StringField('What is your UofT email?', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        old_email = session.get('email')
        name = form.name.data
        email = form.email.data
        
        # Check if the email contains 'utoronto'
        if 'utoronto' in email:
            # Flash message if email has changed
            if old_email is not None and old_email != email:
                flash('Looks like you have changed your email!')
            
            # Flash message if name has changed
            if old_name is not None and old_name != name:
                flash('Looks like you have changed your name!')
            
            # Update session data
            session['name'] = name
            session['email'] = email
            
            return redirect(url_for('index'))
        else:
            flash('Please enter a valid UofT email address.')

    return render_template('index.html', form=form, name=session.get('name'), email=session.get('email'))

