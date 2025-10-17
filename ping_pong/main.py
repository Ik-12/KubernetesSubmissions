from flask import Flask, jsonify
import os
import logging
import psycopg2

POSTGRES_URL = os.environ.get('POSTGRES_URL', 'postgresql://postgres@localhost')

class PingPongApp:
    def __init__(self):
        self.port = int(os.environ.get('PORT', 5001))

        self.conn = self.init_db()
        self.flask_app = Flask(__name__)
        self.setup_routes()

    def init_db(self):
        conn = psycopg2.connect(POSTGRES_URL)
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS pong_counter (
                    id SERIAL PRIMARY KEY,
                    pong_count INTEGER NOT NULL
                );
            """)
            # Ensure a single row exists
            cur.execute("SELECT pong_count FROM pong_counter WHERE id=1;")
            if cur.fetchone() is None:
                cur.execute("INSERT INTO pong_counter (id, pong_count) VALUES (1, 0);")
            conn.commit()
        return conn

    def get_pong_count(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT pong_count FROM pong_counter WHERE id=1;")
            row = cur.fetchone()
            return row[0] if row else 0

    def increment_pong_count(self):
        with self.conn.cursor() as cur:
            cur.execute("UPDATE pong_counter SET pong_count = pong_count + 1 WHERE id=1;")
            self.conn.commit()

    def setup_routes(self):
        @self.flask_app.route('/pingpong')
        def pong():
            count = self.get_pong_count()
            resp = f"pong {count}"
            self.increment_pong_count()
            return resp

        @self.flask_app.route('/pings')
        def pings():
            count = self.get_pong_count()
            return jsonify({'pong_count': count})

    def run(self):
        self.flask_app.logger.info(f"Server started in port {self.port}")
        self.flask_app.logger.info(f"Using Postgres at: {POSTGRES_URL}")
        self.flask_app.run(host='0.0.0.0', port=self.port)

ping_pong_app = PingPongApp()
flask_app = ping_pong_app.flask_app

if __name__ == '__main__':
    ping_pong_app.run()

