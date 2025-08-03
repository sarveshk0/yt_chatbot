from flask import Flask, request, jsonify
from flask_cors import CORS
from rag_pipeline import ask_from_video
import os
app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()

    video_url = data.get("video_url")
    question = data.get("question")

    if not video_url or not question:
        return jsonify({"error": "Missing video_url or question"}), 400

    try:
        answer = ask_from_video(video_url, question)
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))  # Ensure port is defined
