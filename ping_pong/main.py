from flask import Flask
import os
import logging

class PingPongApp:
    def __init__(self):
        self.port = int(os.environ.get('PORT', 5001))
        self.pong_count = 0
        self.flask_app = Flask(__name__)
        self.setup_routes()

    def setup_routes(self):
        @self.flask_app.route('/pingpong')
        def pong():
            resp = f"pong {self.pong_count}"
            self.pong_count += 1
            
            return resp

    def run(self):
        self.flask_app.logger.info(f"Server started in port {self.port}")
        self.flask_app.run(host='0.0.0.0', port=self.port)

ping_pong_app = PingPongApp()
flask_app = ping_pong_app.flask_app

if __name__ == '__main__':
    ping_pong_app.run()

