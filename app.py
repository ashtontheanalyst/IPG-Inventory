from flask import Flask, render_template

# Init app
app = Flask(__name__)

# Test home
@app.route("/")
def home():
    return render_template('home.html')

# Run the App
if __name__ == '__main__':
    app.run(debug=True)