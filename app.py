import flask
from flask import render_template, session, request, abort, send_from_directory, jsonify
import backend

app = flask.Flask(__name__)

@app.route('/', methods=['GET','POST'])
def main_page():
    if request.method == "POST":
        request_content = request.json
        request_content = backend.none_parser(request_content)
        if request_content is None:
            abort(400)
        fname = request_content.get("fname")
        if fname is None:
            chain,fname = backend.create_chain()
        else:
            chain = backend.load_chain(fname)
        message = request_content.get("message")
        if message is None:
            return abort(400)
        message_response = chain.run(message) # error handle here
        backend.save_chain(chain, fname)
        return jsonify({"message":message_response})

    return render_template("index.html", fname=None)

@app.route('/get_code', methods=['GET'])
def get_new_convo():
    return jsonify({"fname":backend.create_chain()[1]})

@app.route('/assets/<path:path>')
def send_report(path):
    return send_from_directory('assets', path)

if __name__ == "__main__":
    app.run()