from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')



if __name__ == '__main__':
    app.run(debug=True)
