from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

# A simple route to test if the app is working
@app.route('/')
def home():
    """
    This is the main route for the application.
    It returns a JSON response to confirm the app is running.
    """
    return jsonify({
        "message": "Hello from your Flask app on Vercel!",
        "status": "success"
    })

# New route to serve the flashcard data from data.json
@app.route('/flashcards')
def get_flashcards():
    """
    This route reads the flashcard data from the data.json file
    and returns it as a JSON object.
    """
    # Construct the full path to the data.json file
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data.json')
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "data.json file not found"}), 404

# The entry point for Vercel
# This is required for Vercel to know where to find your app
# The name 'app' is the standard Vercel entry point
if __name__ == '__main__':
    app.run(debug=True)
