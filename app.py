from flask import Flask, redirect, render_template, flash, url_for, session
from flask_bootstrap import Bootstrap5
from forms import LoginForm

# create the app
app = Flask(__name__)
app.config[
    "SECRET_KEY"
] = 'h+u5-sNA2%Fr&3"y"9nQEn==rfLjfKB{$RGShJ"$2I`d&j[5-J79:RJZoQJ('
# app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'lumen'
bootstrap = Bootstrap5(app)


@app.route("/")
def index():
    flash("Please input at least one DHCP entity description below.", "success")
    return render_template("index.html")


@app.route("/secret")
def secret():
    return render_template("secret.html")


if __name__ == "__main__":
    app.run(debug=True)
