from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired
from wtforms.validators import Email, ValidationError
import secrets


def custom_email_validator(form, field):
    personal_domains = ['gmail.com', 'yahoo.com']  # Add more personal domains as needed
    email = field.data.lower()
    domain = email.split('@')[-1]
    if domain in personal_domains:
        raise ValidationError('Personal email domains are not allowed.')


class MyForm(FlaskForm):
    fName = StringField('First Name', validators=[DataRequired()])
    lName = StringField('Last Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), custom_email_validator])
    submit = SubmitField("Verify")


app = Flask(__name__)
# add a secret key for your app
app.secret_key = "your-secret-key"

# Configuration for Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'your-email-sender'
app.config['MAIL_PASSWORD'] = "your-app-password"
mail = Mail(app)


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "GET":
        form = MyForm()
        return render_template("index.html", form=form)

    form = MyForm()
    if form.validate_on_submit():
        # send email to the user to verify
        first_name = request.form['fName']
        second_name = request.form['lName']
        email = request.form['email']

        # creating a unique token to verify
        token = secrets.token_urlsafe(16)
        # you add the database mechanism in here
        send_verification_email(first_name, second_name, email, token)

        flash('Email has been sent successfully!', 'success')
        return redirect(url_for("home"))
    else:
        # do not send anything and only prompt the user to re-write the email
        print("Not Validated")
    return render_template("index.html", form=form)


# sending the e-mail
def send_verification_email(fName, lName, email, token):
    msg = Message('Email Verification', sender="ranahafez17@gmail.com", recipients=[email])
    msg.body = f"Hello {fName} {lName},\n\t Please check link to verify your email address: http://127.0.0.1:5000/verify?token={token}"
    mail.send(msg)


@app.route("/verify")
def verify():
    """method for verification"""
    # you can add here the verification mechanism
    # checking if the token matches in the database
    flash('Email has been Verified!', 'success')
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
