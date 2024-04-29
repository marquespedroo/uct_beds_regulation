from crdf_web import app,database
from crdf_web.models import User, Post
import logging

logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    app.logger.info('Esta é uma mensagem de informação.')
    app.logger.warning('Esta é uma mensagem de aviso.')
    app.logger.error('Esta é uma mensagem de erro.')
    app.logger.critical('Esta é uma mensagem crítica.')
    return 'Verifique os logs para ver as mensagens registradas.'  


if __name__ == '__main__':
    app.run(debug=False)

# with app.app_context():
#     database.drop_all()
#     database.create_all()
    

