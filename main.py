from flask import Flask, render_template, url_for, redirect
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from forms import ContactForm
from flask_mail import Mail, Message
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///messages.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'maksimov4598@gmail.com'
app.config['MAIL_DEFAULT_SENDER'] = 'maksimov4598@gmail.com'
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
Bootstrap(app)
CKEditor(app)
db = SQLAlchemy(app)
admin = Admin(app)
mail = Mail(app)


class Form(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(1000), nullable=False)


class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    link = db.Column(db.String(100), nullable=False)


class Skill(db.Model):
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True)
    skill = db.Column(db.String(50), nullable=False)


class Degree(db.Model):
    __tablename__ = 'degrees'
    id = db.Column(db.Integer, primary_key=True)
    degree = db.Column(db.String(50))
    organization = db.Column(db.String(100))
    period = db.Column(db.String(50))


admin.add_view(ModelView(Form, db.session))
admin.add_view(ModelView(Project, db.session))
admin.add_view(ModelView(Skill, db.session))
admin.add_view(ModelView(Degree, db.session))

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    all_skills = Skill.query.all()
    all_degrees = Degree.query.all()
    return render_template('about.html', skills=all_skills, degrees=all_degrees)


@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/projects')
def get_projects():
    all_posts = Project.query.all()
    return render_template('projects.html', projects=all_posts)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        new_message = Form(
            name=form.name.data,
            email=form.email.data,
            message=form.message.data
        )
        db.session.add(new_message)
        db.session.commit()
        msg = Message(
            subject=f'Thank you for contacting me, {new_message.name}',
            body=f'Hello, {new_message.name}, thank you for contacting me! I will send you an answer very soon!',
            recipients=[new_message.email]
        )
        mail.send(msg)
        return redirect(url_for('success'))
    return render_template('contact.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)