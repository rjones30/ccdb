import os

from flask import Flask, g

import ccdb
from ccdb import provider


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        SQL_CONNECTION_STRING="mysql://ccdb_user@hallddb.jlab.org/ccdb"
    )

    app = Flask(__name__)
    app.config.from_object(__name__)

    @app.before_request
    def before_request():
        g.tdb = ccdb.AlchemyProvider()
        g.tdb.connect(app.config["SQL_CONNECTION_STRING"])
        #app.jinja_env.globals['datetime_now'] = datetime.now

    @app.teardown_request
    def teardown_request(exception):
        tdb = getattr(g, 'db', None)
        if tdb:
            tdb.close()

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # # ensure the instance folder exists
    # try:
    #     os.makedirs(app.instance_path)
    # except OSError:
    #     pass

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    from ccdb.webgui.data_timeline import bp as time_line_bp
    from ccdb.webgui.dashboard import bp as dashboard_bp

    app.register_blueprint(time_line_bp)
    app.register_blueprint(dashboard_bp)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule("/", endpoint="index")

    return app


if __name__ == '__main__':
    create_app().run()
