import os
from flask import Flask, render_template
import webbrowser
app = Flask(__name__)

@app.route('/base')
def base():
    return render_template('base.html')

@app.route('/about')
def about():
    return render_template('about.html', HelloWorld='Hello World')

@app.route('/noah')
def noah():
    return render_template('noah.html',noah='hello world')

@app.route('/guillaume')
def guillaume():
    return render_template('guillaume.html',guillaume='hello world')

if __name__ == '__main__':
    URL = 'http://127.0.0.1:5000/base'
    webbrowser.open_new_tab(URL)
    app.run(debug=True)

