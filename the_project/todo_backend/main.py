from flask import Flask, request, redirect, jsonify
import os
import logging

class TodoBackend:
    def __init__(self):        
        self.port = int(os.environ.get('PORT', 5005))
        self.flask_app = Flask(__name__)
        self.setup_routes()
        
        self.todos = []

    def setup_routes(self):
        @self.flask_app.route('/todos', methods=['GET', 'POST'])
        def todo():
            if request.method == 'POST':
                todo_text = request.form.get('todo')
                self.flask_app.logger.info("POST new todo: %s", todo_text)
                
                if not todo_text and request.is_json and request.json is not None:
                    todo_text = request.json.get('todo')
                if todo_text:
                    self.todos.append(todo_text)
                    return redirect("/")
                
                return jsonify({"error": "Missing todo"}), 400
            
            elif request.method == 'GET':
                self.flask_app.logger.info("GET todos: %s", self.todos)
                
                return jsonify({"todos": self.todos})
            else:
                return jsonify({"error": "Method not allowed"}), 405

    def run(self):
        self.flask_app.logger.info(f"Backend 2.2 started in port {self.port}")
        self.flask_app.run(host='0.0.0.0', port=self.port)

backend_app = TodoBackend()
flask_app = backend_app.flask_app

if __name__ == '__main__':
    flask_app.logger.setLevel(logging.INFO)
    backend_app.run()
else:
    gunicorn_logger = logging.getLogger('gunicorn.error')
    flask_app.logger.handlers = gunicorn_logger.handlers
    flask_app.logger.setLevel(gunicorn_logger.level)
    flask_app.logger.info(f"Backend started in port {backend_app.port}")
