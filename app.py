from flask import Flask, render_template, flash, redirect, url_for,session
from flask_mail import Mail, Message
from werkzeug.utils import redirect
import json
from forms import ContactMeForm
import os
from dotenv import load_dotenv
from flask_talisman import Talisman


app=Flask(__name__)
mail=Mail(app)
Talisman(app)

load_dotenv()

app.config['SECRET_KEY']=os.getenv('SECRET_KEY')
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT"))
app.config['MAIL_USE_TLS'] = os.getenv("MAIL_USE_TLS") == 'True'
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_DEFAULT_SENDER")





@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/Experience')
def experience_page():
    with open('data/experience.json') as f:
        experience_list = json.load(f)
    return render_template('Experience.html', experiences=experience_list)



@app.route('/project')
def project_page():
    with open('data/projects.json', 'r') as f:
        projects = json.load(f)
    return render_template('project.html', projects=projects)


@app.route('/contact_me',methods=['GET','POST'])
def contact_me_page():
    form =  ContactMeForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        subject =form.subject.data or 'NO SUBJECT'
        message = form.message.data or 'No message'
        # Email to you
        msg = Message(subject=f"New Contact: {subject}",
                      sender=email,
                      recipients=['sanskritiverma.1807@gmail.com'],
                      body=f"From: {name} <{email}>\n\nMessage:\n{message}")

        mail.send(msg)

        flash('Thank you for your message!', 'success')
        return redirect(url_for('success_page'))

    return  render_template('contact_me.html',form=form,name=session.get('name'),email=session.get('email'),subject=session.get('subject'),message=session.get('message'))

@app.route('/success',methods=['GET'])
def success_page():
    return render_template('success.html')


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run()

