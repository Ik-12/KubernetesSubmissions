from flask import Flask
import os

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
        print(f"Server started in port {self.port}")
        self.flask_app.run(host='0.0.0.0', port=self.port)

todo_app = TodoApp()
flask_app = TodoApp().flask_app

if __name__ == '__main__':
    todo_app.run()