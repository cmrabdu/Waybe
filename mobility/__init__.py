import os
from flask import Flask, render_template
import webbrowser
app = Flask(__name__)
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config.from_mapping(
            SECRET_KEY='dev',
            DATABASE=os.path.join(app.root_path, 'poudlard.sqlite'),
        )

    from . import city
    app.register_blueprint(city.bp)

    app.add_url_rule('/', endpoint='index')

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/base')
    def base():
        return render_template('base.html')

    @app.route('/about')
    def about():
        return render_template('about.html', HelloWorld='Hello World')

    @app.route('/noah')
    def noah():
        return render_template('noah.html',noah='hello world')

    @app.route('/abdullah')
    def abdullah():
        return render_template('abdullah.html',abdullah='hello world')

    
    @app.route('/houari')
    def houari():
        return render_template('houari.html',houari='hello world')


    @app.route('/guillaume')
    def guillaume():
        return render_template('guillaume.html',guillaume='hello world')

    return app 

