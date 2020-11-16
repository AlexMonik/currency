from flask import Flask, render_template
import logging
from api import api
from flask_jwt_extended import JWTManager
# from testApi.config import APP_ENV


logging.basicConfig(filename='scrapping_data_logs.log',
                    level=logging.DEBUG,
                    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')

logger = logging.getLogger()


def create_app():
    # logger.info(f'Starting app in {APP_ENV} environment')
    app_ = Flask(__name__)
    app_.config.from_object('config')
    api.init_app(app_)
    app_.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
    JWTManager(app_)

    @app_.route('/')
    def index():
        return render_template('index.html')

    return app_


if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', debug=True, port=5050)
