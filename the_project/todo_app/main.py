from flask import Flask
import os

class TodoApp:
    def __init__(self, port: int):
        self.port = port
        self.app = Flask(__name__)
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/')
        def home():
            return f"Server started in port {self.port}"

    def run(self):
        print(f"Server started in port {self.port}")
        self.app.run(host='0.0.0.0', port=self.port)

if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    todo_app = TodoApp(port)
    todo_app.run()
