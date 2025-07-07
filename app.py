from crypt import methods

from flask import Flask,render_template,flash,redirect,url_for
from forms import ContactMeForm

app=Flask(__name__)
app.config['SECRET_KEY'] = b'46SAUCY4002'  # use b'' or os.urandom



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
        #send it via email
        flash('Thank you for your message!', 'success')
        return redirect(url_for('success_page'))

    return  render_template('contact_me.html',form=form)

@app.route('/success')
def success_page():
    return render_template('success.html')


if __name__ == "__main__":
    app.run()

