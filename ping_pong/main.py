from flask import Flask
import os
import logging

class PingPongApp:
    def __init__(self):
        self.port = int(os.environ.get('PORT', 5001))
        
        # Set up logging pong count
        self.pong_count = 0
        self.log_file = os.environ.get('PONG_COUNT_FILE_PATH', 
                                       '/tmp/pong_log/pong_count')
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        self.write_pong_count()

        self.flask_app = Flask(__name__)
        self.setup_routes()

    def setup_routes(self):
        @self.flask_app.route('/pingpong')
        def pong():
            resp = f"pong {self.pong_count}"
            self.write_pong_count()
                
            self.pong_count += 1
                
            return resp
        
    def write_pong_count(self):
        try:
            with open(self.log_file, "w") as f:
                f.write(str(self.pong_count))
        except Exception as e:
            self.flask_app.logger.error(f"Error writing pong count: {e}")

    def run(self):
        self.flask_app.logger.info(f"Server started in port {self.port}")
        self.flask_app.logger.info(f"Pong count file path: {self.log_file}")
        
        self.flask_app.run(host='0.0.0.0', port=self.port)

ping_pong_app = PingPongApp()
flask_app = ping_pong_app.flask_app

if __name__ == '__main__':
    ping_pong_app.run()

