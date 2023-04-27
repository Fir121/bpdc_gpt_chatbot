import flask
from flask import render_template, session, request
from flask_session import Session

app = flask.Flask(__name__)
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/', methods=['GET'])
def home():
    code = request.args.get("code")
    #if code is None:
    return render_template("index.html")

if __name__ == "__main__":
    app.run()