from flask import Flask, render_template, flash, redirect, url_for, session, jsonify
from flask_mail import Mail, Message
from werkzeug.utils import redirect
import json
from forms import ContactMeForm
import os
from dotenv import load_dotenv
from flask_talisman import Talisman

load_dotenv()

app = Flask(__name__)

csp = {
    'default-src': [
        '\'self\''
    ],
    'style-src': [
        '\'self\'',
        'https://cdn.jsdelivr.net',
        'https://cdnjs.cloudflare.com',
        'https://fonts.googleapis.com',
        'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0',
        '\'unsafe-inline\''  # Added for smooth scrolling styles
    ],
    'script-src': [
        '\'self\'',
        'https://cdn.jsdelivr.net',
        'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0',
        'https://cdnjs.cloudflare.com',
        '\'unsafe-inline\''  # Added for smooth scrolling script
    ],
    'font-src': [
        '\'self\'',
        'https://cdnjs.cloudflare.com',
        'https://cdn.jsdelivr.net',
        'https://fonts.gstatic.com'
    ]
}

Talisman(app, content_security_policy=csp)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
app.config['MAIL_PORT'] = os.getenv("MAIL_PORT")
app.config['MAIL_USE_TLS'] = os.getenv("MAIL_USE_TLS")
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_DEFAULT_SENDER")
app.config['MAIL_DEBUG'] = True

mail = Mail(app)


@app.route('/')
def home_page():
    # Load all data for the single page
    with open('data/experience.json') as f:
        experience_list = json.load(f)

    with open('data/projects.json', 'r') as f:
        projects = json.load(f)

    form = ContactMeForm()

    return render_template('base.html',
                           experiences=experience_list,
                           projects=projects,
                           form=form)


@app.route('/contact', methods=['POST'])
def handle_contact():
    form = ContactMeForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        subject = form.subject.data or 'NO SUBJECT'
        message = form.message.data or 'No message'

        # Email to you
        msg = Message(subject=f"New Contact: {subject}",
                      sender=email,
                      recipients=['sanskritiverma.1807@gmail.com'],
                      body=f"From: {name} <{email}>\n\nMessage:\n{message}")

        try:
            mail.send(msg)
            return jsonify(success=True, title="Thank you for your message!", detail="I'll get back to you soon.")

        except Exception as e:
            return jsonify({'success': False, 'message': 'Sorry, there was an error sending your message.'})

    # Return validation errors
    errors = {}
    for field, field_errors in form.errors.items():
        errors[field] = field_errors
    return jsonify({'success': False, 'errors': errors})


if __name__ == "__main__":
    app.run(debug=True, port=5001)