from flask import Flask, render_template, request, jsonify
from feedback import generate_feedback  # Import function from feedback.py

app = Flask(__name__, template_folder='templates')

# Route for homepage
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

# Route for feedback page
@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

# New route to process feedback input
@app.route('/process_feedback', methods=['POST'])
def process_feedback():
    data = request.json  # Receive JSON dictionary from frontend

    if not data:
        return jsonify({"feedback": "No valid criteria provided."})  # Handle empty input

    feedback = generate_feedback(data)  # Generate structured feedback
    return jsonify({"feedback": feedback})  # Return response as JSON

if __name__ == '__main__':
    app.run(debug=True)