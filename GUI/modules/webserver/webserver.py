from flask import Flask


def create_app():
    app = Flask(__name__)

    from main import bp_main
    app.register_blueprint(bp_main)

    from modules import bp_modules
    app.register_blueprint(bp_modules)

    app.run(host='localhost', port='5000')


create_app()
