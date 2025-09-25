from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

@app.route('/')
def home():
    return """
<!doctype html>
<html>
<head><meta charset="utf-8"><title>Flashcards</title></head>
<body>
  <h1>Flashcards</h1>
  <pre id="out">loading…</pre>
  <script>
    fetch('/flashcards').then(r=>r.json()).then(d=>{
      document.getElementById('out').textContent = JSON.stringify(d,null,2);
    });
  </script>
</body>
</html>
"""


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
