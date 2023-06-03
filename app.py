from flask import Flask, flash, redirect, render_template, url_for, request, session
from flask_bootstrap import Bootstrap5

from entity import Entity
from utils import create_triplet, createTimestamp, writer
import testing, json, random

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
        
        if request.form.get("automatic"):
            session["descriptions"] = [create_triplet("", 1)]
            session["log"] = "start point log "
            session["step_number"] = 1
            session["blocked"] = []
            return redirect(url_for("automatic"))

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
            commands = [
                v
                for k, v in request.form.items()
                if k.startswith("e") and k.endswith(str(step_number))
            ]
            entities = []
            if step_number == 1:
                for index in range(len(commands)):
                    entities.append(Entity(index + 1))
            else:
                for serialized_entity in session["entities"]:
                    entities.append(
                        json.loads(serialized_entity, object_hook=Entity.decoder)
                    )

            simulation_result = testing.test_stepByStep(commands, entities)

            if commands and simulation_result:
                serialized_entities = []
                for entity in simulation_result[2]:
                    serialized_entities.append(json.dumps(entity, cls=Entity.Encoder))
                session["entities"] = serialized_entities

                session["step_number"] = step_number + 1
                session["log"] = session.get("log") + "\n" + simulation_result[0]
                session["blocked"] = simulation_result[1]
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
        blocked=blocked,
    )

@app.route("/define/automatic", methods=["GET", "POST"])
def automatic():
    if request.method == "POST":
        if request.form.get("simulate"):
            entities = []
            num_ent = int(request.form.get("entities"))
            num_step = int(request.form.get("steps"))
            for index in range(num_ent):
                entities.append(Entity(index+1))
            
            for step_number in range(num_step):
                options_actions = ['SEND "MESSAGE" TO ', 'LISTEN "MESSAGE" FROM ', "SKIP", "FINISH"]
                options_dest = []
                for index in range(num_ent):
                    options_dest.append(index+1)

                commands = []
                for index in range(num_ent):
                    string_builder = str(random.choice(options_actions))
                    if string_builder.startswith(("SEND", "LISTEN")):
                        string_builder = string_builder + str(random.choice(options_dest))
                    commands.append(string_builder+'\n')

                simulation_result = testing.test_stepByStep(commands, entities)
                session["log"] = session.get("log") + "\n" + simulation_result[0]

            return redirect(url_for("simulation"))

        if request.form.get("back"):
            return redirect(url_for("index"))

    return render_template("automatic.html")

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
            testing.test_3entityTranslation()
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
    if not log:
        return redirect(url_for("index"))

    if request.method == "POST":
        if request.form.get("back"):
            return redirect(url_for("index"))

    return render_template("simulation.html")


if __name__ == "__main__":
    app.run(debug=True)
