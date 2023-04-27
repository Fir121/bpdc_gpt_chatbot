import flask
from flask import render_template, session, request, abort
import backend

app = flask.Flask(__name__)

@app.route('/', methods=['GET','POST'])
def main_page():
    if request.method == "POST":
        fname = request.form.get("fname")
        if fname is None:
            chain,fname = backend.create_chain()
        else:
            chain = backend.load_chain(fname)
        message = request.form.get("message")
        if message is None:
            return abort(400)
        message_response = chain.run(message)
        backend.save_chain(chain, fname)
        return render_template("index.html", fname=fname, message_response=message_response)

    return render_template("index.html", fname=None, message_response=None)

if __name__ == "__main__":
    app.run()