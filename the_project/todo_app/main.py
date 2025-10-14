from flask import Flask
import os
import logging

class TodoApp:
    def __init__(self):        
        self.port = int(os.environ.get('PORT', 5000))
        self.flask_app = Flask(__name__)
        self.setup_routes()

    def setup_routes(self):
        @self.flask_app.route('/')
        def home():
            return f"Server started in port {self.port}"

    def run(self):
        self.flask_app.logger.info(f"Server started in port {self.port}")
        self.flask_app.run(host='0.0.0.0', port=self.port)

todo_app = TodoApp()
flask_app = TodoApp().flask_app

if __name__ == '__main__':
    todo_app.run()
else:
    gunicorn_logger = logging.getLogger('gunicorn.error')
    flask_app.logger.handlers = gunicorn_logger.handlers
    flask_app.logger.setLevel(gunicorn_logger.level)
    flask_app.logger.info(f"Server started in port {todo_app.port}")
