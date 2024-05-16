from crdf_web import database, app
from crdf_web.models import User, Post

with app.app_context():
    @app.route('/')
    def index():
        app.logger.info('Esta é uma mensagem de informação.')
        app.logger.warning('Esta é uma mensagem de aviso.')
        app.logger.error('Esta é uma mensagem de erro.')
        app.logger.critical('Esta é uma mensagem crítica.')
        return 'Verifique os logs para ver as mensagens registradas.'

    # with app.app_context():
    #   database.drop_all()
    #   database.create_all()

    if __name__ == '__main__':
        app.run(debug=False)