def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
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

    @app.route('/')
    def base():
        return render_template('base.html')

    @app.route('/about')
    def about():
        return render_template('about.html', HelloWorld='Bonjour tout le monde')

    @app.route('/statistique')
    def stats():
        return render_template('stats.html', stats='bonjour le monde')

    @app.route('/request')
    def request():
        return render_template('request.html', data='bonjour le monde')

    return app
