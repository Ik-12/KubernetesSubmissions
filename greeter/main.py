import os

from flask import Flask
MESSAGE = os.environ.get("MESSAGE", "Hello, World!")

class Greeter:
    def __init__(self):
        self.port = int(os.environ.get("PORT", 5008))
        self.flask_app = Flask(__name__)
        self.setup_routes()

    def setup_routes(self):
        @self.flask_app.route("/greeter")
        def hello():
            resp = f"{MESSAGE}"
            return resp

        @self.flask_app.route("/")
        def ready():
            if self.conn is None:
                self.conn = self.init_db()

            if self.conn is not None:
                return "OK", 200
            else:
                return "Service unavailable", 503

    def run(self):
        self.flask_app.logger.info(f"Server started in port {self.port}")
        self.flask_app.run(host="0.0.0.0", port=self.port)

greeter = Greeter()
flask_app = greeter.flask_app

if __name__ == "__main__":
    greeter.run()
