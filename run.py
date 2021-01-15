import logging

from piatrix_app import app

if __name__ == '__main__':
    logging.basicConfig(filename='app.log', level=logging.WARNING)
    app.run()
