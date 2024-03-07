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

@app.route('/statisque')
def stats():
    return render_template('stats.html', stats='hello world')

@app.route('/request')
def request():
    return render_template('request.html', abdullah='hello world')



if __name__ == "__main__":
    app.run(debug=True)
