import flask
from flask import render_template, session, request, abort, send_from_directory, jsonify
import backend
# implement /video, /contrib and /admin
app = flask.Flask(__name__)

@app.route('/', methods=['GET','POST'])
def main_page():
    if request.method == "POST":
        request_content = request.json
        request_content = backend.none_parser(request_content)
        if request_content is None:
            abort(400)
        chat_id = request_content.get("chat_id")
        if chat_id is None:
            chain,chat_id = backend.create_chain()
        else:
            chain = backend.load_chain(chat_id)
        message = request_content.get("message")
        if message is None:
            return abort(400)
        message_response = backend.return_output(message, chain, chat_id)
        return jsonify({"message":message_response})

    return render_template("index.html", chat_id=backend.create_chain()[1])

@app.route('/get_code', methods=['GET'])
def get_new_convo():
    return jsonify({"chat_id":backend.create_chain()[1]})

@app.route('/feedback', methods=['POST'])
def log_feedback():
    chat_id = request.json["chat_id"]
    backend.log_feedback(chat_id)
    return {"status":"success"}

@app.route('/assets/<path:path>')
def send_report(path):
    return send_from_directory('assets', path)

if __name__ == "__main__":
    app.run()