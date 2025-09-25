from flask import Flask, jsonify, request

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

# A route that takes a name as a URL parameter
@app.route('/greet/<name>')
def greet(name):
    """
    A route to greet a user by name.
    """
    return jsonify({
        "message": f"Hello, {name}!",
        "status": "success"
    })

# The entry point for Vercel
# This is required for Vercel to know where to find your app
# The name 'app' is the standard Vercel entry point
if __name__ == '__main__':
    app.run(debug=True)
