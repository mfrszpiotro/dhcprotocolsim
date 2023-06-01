from flask import Flask, flash, redirect, render_template, url_for, request, session
from flask_bootstrap import Bootstrap5

from entity import Entity
from forms import LoginForm
from utils import create_triplet

# create the app
app = Flask(__name__)
app.config[
    "SECRET_KEY"
] = 'h+u5-sNA2%Fr&3"y"9nQEn==rfLjfKB{$RGShJ"$2I`d&j[5-J79:RJZoQJ('
app.config["BOOTSTRAP_BOOTSWATCH_THEME"] = "lux"
bootstrap = Bootstrap5(app)


@app.route("/", methods=["GET", "POST"])
def index():
    session.pop("descriptions", None)
    session.pop("log", None)
    if request.method == "POST":
        if request.form.get("start"):
            session["descriptions"] = [create_triplet("", 1)]
            session["log"] = "start point log "
            session["step_number"] = 1
            session["blocked"] = []
            return redirect(url_for("step"))

        if request.form.get("alt"):
            session["descriptions"] = [create_triplet("", 4)]
            return redirect(url_for("define"))

    return render_template("index.html")


@app.route("/step", methods=["GET", "POST"])
def step():
    step_number = session.get("step_number")
    blocked = session.get("blocked")
    if request.method == "POST":
        if request.form.get("simulate"):
            session.pop("_flashes", None)
            commands = [v for k, v in request.form.items() if k.startswith("e") and k.endswith(str(step_number))]
            # commands to be translated into full simulation step execution
            wasSimulated = True
            # descriptions to be blocked if entity is deadlocked in this step
            if commands and wasSimulated:
                session["step_number"] = step_number+1
                # data based on the output from the simulation:
                session["log"] = session.get("log") + "\n" + str(commands)
                session["blocked"] = [2]
            return redirect(url_for("step"))

        if request.form.get("add"):
            session.pop("_flashes", None)
            descr = list(session.get("descriptions"))
            descr.append(create_triplet("", 1))
            session["descriptions"] = descr

        if request.form.get("save"):
            return redirect(url_for("simulation"))

        if request.form.get("back"):
            return redirect(url_for("index"))

    return render_template(
        "step.html",
        page_descriptions=session.get("descriptions")[1:],
        first_triplet=session.get("descriptions")[0],
        step_number=step_number,
        blocked=blocked
    )


@app.route("/define", methods=["GET", "POST"])
def define():
    if request.method == "POST":
        if request.form.get("simulate"):
            session.pop("_flashes", None)
            entities = []
            for index in range(len(session.get("descriptions")) * 3):
                check_begin = "e{}".format(str(index + 1))
                entities.append(
                    [v for k, v in request.form.items() if k.startswith(check_begin)]
                )
            session["entities"] = entities
            return redirect(url_for("simulation"))

        if request.form.get("add"):
            session.pop("_flashes", None)
            descr = list(session.get("descriptions"))
            descr.append(create_triplet("", 4))
            session["descriptions"] = descr

        if request.form.get("back"):
            return redirect(url_for("index"))

    return render_template(
        "define.html",
        page_descriptions=session.get("descriptions")[1:],
        first_triplet=session.get("descriptions")[0],
    )


@app.route("/define/simulation", methods=["GET", "POST"])
def simulation():
    log = session.get("log", None)
    if log:
        flash(log, "success")
    if request.method == "POST":
        if request.form.get("back"):
            return redirect(url_for("index"))

    return render_template("simulation.html")


if __name__ == "__main__":
    app.run(debug=True)
