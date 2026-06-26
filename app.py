import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from prometheus_flask_exporter import PrometheusMetrics
import logging
from pythonjsonlogger import jsonlogger

logger = logging.getLogger("devops-app")
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter("%(asctime)s %(levelname)s %(message)s")
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

db = SQLAlchemy()

# Define the model once, at module level — not inside create_app()
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)

def create_app():
    
    app = Flask(__name__)
    metrics = PrometheusMetrics(app)
    

    DB_USER = os.environ.get("DB_USER", "postgres")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")
    DB_HOST = os.environ.get("DB_HOST", "db")
    DB_NAME = os.environ.get("DB_NAME", "devops_app")

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
    )
    db.init_app(app)

    @app.route("/")
    def home():
        return jsonify(message="Hello! This is my first DevOps learning app.")

    @app.route("/health")
    def health():
        return jsonify(status="ok")

    @app.route("/tasks", methods=["GET"])
    def get_tasks():
        tasks = Task.query.all()
        return jsonify([{"id": t.id, "title": t.title} for t in tasks])

    @app.route("/tasks", methods=["POST"])
    def add_task():
        data = request.get_json()
        new_task = Task(title=data["title"])
        db.session.add(new_task)
        db.session.commit()
        logger.info("Task created", extra={"task_id": new_task.id, "title": new_task.title})
        return jsonify({"id": new_task.id, "title": new_task.title}), 201

    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False, use_reloader=False)