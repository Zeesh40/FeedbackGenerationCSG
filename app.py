from flask import Flask, render_template, request, jsonify
from feedback import generate_feedback  

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

# Route to process feedback input
@app.route('/process_feedback', methods=['POST'])
def process_feedback():
    data = request.get_json()
    criteria = data.get("criteria", [])
    order = data.get("order", "adaptive")
    feedback = generate_feedback(criteria, order)
    return jsonify({"feedback": feedback})


if __name__ == '__main__':
    app.run(debug=True)
