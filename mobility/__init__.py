from flask import Flask, render_template
import os

app = Flask(__name__)

# Configuration
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.root_path, 'poudlard.sqlite'),
)

# Ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

# Routes
@app.route('/')
def base():
    return render_template('base.html')

@app.route('/about')
def about():
    return render_template('about.html', HelloWorld='Hello World')

@app.route('/noah')
def noah():
    return render_template('noah.html', noah='hello world')

@app.route('/abdullah')
def abdullah():
    return render_template('abdullah.html', abdullah='hello world')

@app.route('/houari')
def houari():
    return render_template('houari.html', houari='hello world')

@app.route('/guillaume')
def guillaume():
    return render_template('guillaume.html', guillaume='hello world')

if __name__ == "__main__":
    app.run(debug=True)
