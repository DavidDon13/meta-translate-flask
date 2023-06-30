from flask import Flask, request, jsonify
from translator import Translator
import logging

app = Flask(__name__)
translator = Translator()


@app.route("/api/translate", methods=["POST"])
def translate():
    if not request.is_json:
        return jsonify({"error": "Bad Request, JSON data expected"}), 400

    data = request.get_json()

    if "messages" not in data:
        return (
            jsonify(
                {"error": 'Bad Request, "messages" field is required in request data'}
            ),
            400,
        )

    messages = data["messages"]
    if not isinstance(messages, list):
        return (
            jsonify(
                {"error": 'Bad Request, "messages" field must be a list of messages'}
            ),
            400,
        )

    translated_messages = translator.translate(messages)
    return jsonify(translated_messages)


@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({"status": "Model is ready"}), 200


if __name__ == "__main__":
    logging.info("Starting app...")
    app.run(debug=True)
    # listen to connections from anywhere
    app.run(debug=True, host='0.0.0.0')
