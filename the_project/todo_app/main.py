from flask import Flask, send_file, render_template_string
import os
import logging
import requests
import threading
import time

IMAGE_URL = "https://picsum.photos/1200"
IMAGE_CACHE_PATH = "/tmp/img-cache/cached_image.jpg"
REFRESH_INTERVAL = 600 # seconds 

class TodoApp:
    def __init__(self):        
        self.port = int(os.environ.get('PORT', 5000))
        self.flask_app = Flask(__name__)
        self.setup_routes()
        
        self.image_lock = threading.Lock()
        self.start_image_updater()
        
        self.todos = ["Clean the house", "Write code", "Read a book"]

    def setup_routes(self):
        @self.flask_app.route('/', methods=['GET', 'POST'])
        def home():
            from flask import request, redirect, url_for
            if request.method == 'POST':
                todo_text = request.form.get('todo')
                if todo_text:
                    self.todos.append(todo_text)
                return redirect(url_for('home'))

            # Display the image and todo form
            html = """
            <html>
            <body>
                <h2>The ToDo App</h2>
                <img src="/image" width="400"/>
                <p>DevOps with Kubernetes 2025</p>
                <form method="post">
                    <input type="text" name="todo" placeholder="Enter todo item" required>
                    <input type="submit" value="Add">
                </form>
                <h3>Todo Items:</h3>
                <ul>
                    {% for item in todos %}
                        <li>{{ item }}</li>
                    {% endfor %}
                </ul>
            </body>
            </html>
            """
            return render_template_string(html, todos=self.todos)

        @self.flask_app.route('/image')
        def image():
            # Serve the image file
            with self.image_lock:
                if os.path.exists(IMAGE_CACHE_PATH):
                    return send_file(IMAGE_CACHE_PATH, mimetype='image/jpeg')
                else:
                    return "Image not found", 404

    def update_image(self):
        def needs_update():
            if not os.path.exists(IMAGE_CACHE_PATH):
                return True
            mtime = os.path.getmtime(IMAGE_CACHE_PATH)
            return (time.time() - mtime) > REFRESH_INTERVAL

        while True:
            # Use logging instead of print, and always get the logger from the Flask app
            logger = self.flask_app.logger
            
            if needs_update():
                logger.info("Checking for image update...")
                try:
                    resp = requests.get(IMAGE_URL, timeout=10)
                    if resp.status_code == 200:
                        with self.image_lock:
                            with open(IMAGE_CACHE_PATH, "wb") as f:
                                f.write(resp.content)
                        logger.info("Updated image from picsum.photos")
                    else:
                        logger.warning(f"Failed to fetch image: {resp.status_code}")
                except Exception as e:
                    logger.error(f"Error updating image: {e}")
            else:
                logger.info("Image is up-to-date; no need to refresh.")
                
            time.sleep(REFRESH_INTERVAL)

    def start_image_updater(self):
        t = threading.Thread(target=self.update_image, daemon=True)
        t.start()

    def run(self):
        self.flask_app.logger.info(f"Server started in port {self.port}")
        self.flask_app.run(host='0.0.0.0', port=self.port)

todo_app = TodoApp()
flask_app = todo_app.flask_app

if __name__ == '__main__':
    flask_app.logger.setLevel(logging.INFO)
    todo_app.run()
else:
    gunicorn_logger = logging.getLogger('gunicorn.error')
    flask_app.logger.handlers = gunicorn_logger.handlers
    flask_app.logger.setLevel(gunicorn_logger.level)
    flask_app.logger.info(f"Server started in port {todo_app.port}")
