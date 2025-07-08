from crypt import methods
from pyexpat.errors import messages
from flask import Flask,render_template,flash
from flask_mail import Mail, Message
from forms import ContactMeForm
import os
from dotenv import load_dotenv

app=Flask(__name__)
load_dotenv()

app.config['SECRET_KEY']=os.getenv('SECRET_KEY')
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT"))
app.config['MAIL_USE_TLS'] = os.getenv("MAIL_USE_TLS") == 'True'
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_DEFAULT_SENDER")

mail=Mail(app)

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/Experience')
def experience_page():
    return  render_template('Experience.html')

@app.route('/project')
def project_page():
    return render_template('project.html')

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
        return render_template('success.html')

    return  render_template('contact_me.html',form=form)


if __name__ == "__main__":
    app.run()

