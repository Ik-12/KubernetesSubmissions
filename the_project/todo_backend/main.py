from flask import Flask, request, redirect, jsonify
import os
import logging
import psycopg2

POSTGRES_URL = os.environ.get('POSTGRES_URL', 
                              'postgresql://postgres@localhost/postgres')

class TodoBackend:
    def __init__(self):        
        self.port = int(os.environ.get('PORT', 5005))
        
        self.conn = self.init_db()
        
        self.flask_app = Flask(__name__)
        self.setup_routes()

    def init_db(self):
        conn = psycopg2.connect(POSTGRES_URL)
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS todos (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    done BOOLEAN NOT NULL DEFAULT FALSE
                );
            """)
            conn.commit()
        return conn

    def add_todo(self, name):
        with self.conn.cursor() as cur:
            cur.execute("INSERT INTO todos (name, done) VALUES (%s, FALSE) RETURNING id;", (name,))
            self.conn.commit()
            return cur.fetchone()[0] # type: ignore

    def get_todos(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT id, name, done FROM todos ORDER BY id;")
            rows = cur.fetchall()
            return [{"id": r[0], "name": r[1], "done": r[2]} for r in rows]

    def setup_routes(self):
        @self.flask_app.route('/todos', methods=['GET', 'POST'])
        def todo():
            if request.method == 'POST':
                todo_text = request.form.get('todo')
                if not todo_text and request.is_json and request.json is not None:
                    todo_text = request.json.get('todo')

                if not todo_text:
                    self.flask_app.logger.warning("Missing todo text in request")
                    return jsonify({"error": "Missing todo"}), 400

                if len(todo_text) > 140:
                    self.flask_app.logger.warning(f"Failed to add todo item {repr(todo_text)}. \
                                                  Length exceeds limit of 140 characters")
                    return jsonify({"error": "Todo must be 140 characters or less"}), 400

                todo_id = self.add_todo(todo_text)
                self.flask_app.logger.info(f"Added todo item {repr(todo_text)} with id {todo_id}")
                return redirect("/")

            elif request.method == 'GET':
                return jsonify({"todos": self.get_todos()})
            else:
                return jsonify({"error": "Method not allowed"}), 405

    def run(self):
        self.flask_app.logger.info(f"Backend started in port {self.port}")
        self.flask_app.logger.info(f"Using Postgres at: {POSTGRES_URL}")
        self.flask_app.run(host='0.0.0.0', port=self.port)

backend_app = TodoBackend()
flask_app = backend_app.flask_app

if __name__ == '__main__':
    flask_app.logger.setLevel(logging.INFO)
    backend_app.run()
else:
    import logging
    gunicorn_logger = logging.getLogger('gunicorn.error')
    flask_app.logger.handlers = gunicorn_logger.handlers
    flask_app.logger.setLevel(gunicorn_logger.level)
    flask_app.logger.info(f"Backend started in port {backend_app.port}")
