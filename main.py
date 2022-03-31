from flask import Flask, flash, get_flashed_messages, render_template, redirect, request, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email
from datetime import datetime
import os
import smtplib

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("flask_key")
Bootstrap(app)

send_mail = os.environ.get("send_mail")
password = os.environ.get("mail_password")
receive_mail = os.environ.get("receive_mail")

class ContactForm(FlaskForm):
    name = StringField(label="", validators=[DataRequired()])
    number = StringField(label="")
    email = EmailField(label="", validators=[DataRequired(), Email()])
    message = TextAreaField(label="", validators=[DataRequired()])
    submit = SubmitField(label="Send a Message")

@app.context_processor
def inject_year():
    year = datetime.now().year
    return dict(year=year)

@app.route("/")
def home():
    form = ContactForm()
    return render_template("index.html", form=form)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    get_flashed_messages()
    if request.method == "POST":
        flash("Thank you! Your message has been sent. I'll reply as soon as possible.")
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=send_mail, password=password)
            connection.sendmail(
                from_addr=send_mail,
                to_addrs=receive_mail,
                msg=f"Subject: New Message From Your Website\n\nFrom: {request.form['name']}\n"
                    f"Email: {request.form['email']}\nNumber: {request.form['number']}\nMessage: "
                    f"{request.form['message']}")
            return redirect(url_for("home"))



if __name__ == "__main__":
    app.run(debug=True)