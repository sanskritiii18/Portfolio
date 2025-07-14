from crypt import methods
from pyexpat.errors import messages
from flask import Flask, render_template, flash, redirect, url_for,session
from flask_mail import Mail, Message
from werkzeug.utils import redirect
from wtforms.validators import email

from forms import ContactMeForm
import os
from dotenv import load_dotenv

app=Flask(__name__)
mail=Mail(app)
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
    experience_list = [
        {
            "organization": "C-DAC (Centre for Development of Advanced Computing), Pune",
            "role": "Applied AI Intern",
            "duration": "March 2025 – Present",
            "technologies": ["NLP", "Deep Learning"],
            "confidential": True

        },
        {
            "organization": "Desktop Buddha (Remote)",
            "role": "Python Developer Intern",
            "duration": "Jan 2025 – Feb 2025",
            "technologies": ["Python", "Streamlit", "PostgreSQL", "Google OAuth2.0", "Pytest", "Selenium", "Git",
                             "Jira"],
            "responsibilities": [
                "Developed core features using Streamlit and PostgreSQL",
                "Implemented Google OAuth2.0 authentication",
                "Built a feedback survey system with admin dashboard",
                "Conducted testing using Pytest and Selenium",
                "Participated in Agile sprints using Jira Scrum"
            ]
        }
    ]
    return render_template('Experience.html', experiences=experience_list)




@app.route('/project')
def project_page():
    projects = [
        {
            "title": "Data Visualization Dashboard",
            "desc": "Built using MongoDB, PyMongo, Flask, Plotly & Folium. Displays insights via interactive graphs and maps.",
            "tech": ["MongoDB", "PyMongo", "Flask", "Plotly", "Folium", "Pandas"],
            "icon": "fa-chart-line",
            "link": "http://github.com/sanskritiii18/data_visualization_dashboard"
        },
        {
            "title": "Query Optimization Dashboard",
            "desc": "Flask dashboard for analyzing MongoDB queries, execution time, and performance suggestions.",
            "tech": ["Flask", "MongoDB", "HTML", "CSS", "JavaScript"],
            "icon": "fa-database",
            "link": "https://github.com/sanskritiii18/query_processing-optimization_dashboard"
        },
        {
            "title": "Face Recognition Attendance",
            "desc": "OpenCV + Python system to detect faces and record attendance in CSV.",
            "tech": ["Python", "OpenCV", "CSV"],
            "icon": "fa-face-smile",
            "link": "https://github.com/sanskritiii18/face_recognition_attendace_system"
        },
        {
            "title": "Hinglish Interpreter App",
            "desc": "ML/NLP app that interprets mixed Hindi-English queries using tokenization and intent classification.",
            "tech": ["Python", "NLP", "Machine Learning"],
            "icon": "fa-language",
            "link": "https://github.com/sanskritiverma/hinglish-interpreter"
        },
        {
            "title": "E-Commerce App (Django)",
            "desc": "Django e-commerce platform with PostgreSQL, Chart.js dashboards, Bootstrap UI, and authentication.",
            "tech": ["Django", "PostgreSQL", "Bootstrap", "Chart.js"],
            "icon": "fa-cart-shopping",
            "link": "https://github.com/sanskritiverma/django-ecommerce"
        }
    ]
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


if __name__ == "__main__":
    app.run()

