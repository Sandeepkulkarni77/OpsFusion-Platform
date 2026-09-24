import logging
import os

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(name)s %(message)s"
)
logger = logging.getLogger(__name__)

db = SQLAlchemy()


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    age = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "age": self.age
        }


def create_app(test_config=None):
    app = Flask(__name__)

    database_url = os.getenv("DATABASE_URL", "sqlite:///students.db")

    if test_config:
        app.config.update(test_config)
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = database_url

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    Migrate(app, db)

    @app.get("/healthcheck")
    def healthcheck():
        try:
            db.session.execute(db.text("SELECT 1"))
            return jsonify({"status": "ok"}), 200
        except Exception:
            logger.exception("Database healthcheck failed")
            return jsonify({"status": "unhealthy"}), 503

    @app.post("/api/v1/students")
    def create_student():
        data = request.get_json(silent=True) or {}

        if not all(k in data for k in ("name", "email", "age")):
            return jsonify({"error": "name, email and age are required"}), 400

        try:
            student = Student(
                name=data["name"],
                email=data["email"],
                age=data["age"]
            )

            db.session.add(student)
            db.session.commit()

            logger.info("Created student id=%s", student.id)

            return jsonify(student.to_dict()), 201

        except Exception:
            db.session.rollback()
            logger.exception("Failed to create student")
            return jsonify({"error": "student could not be created"}), 409

    @app.get("/api/v1/students")
    def get_students():
        return jsonify(
            [s.to_dict() for s in Student.query.order_by(Student.id).all()]
        ), 200

    @app.get("/api/v1/students/<int:student_id>")
    def get_student(student_id):
        student = db.session.get(Student, student_id)

        if not student:
            return jsonify({"error": "student not found"}), 404

        return jsonify(student.to_dict()), 200

    @app.put("/api/v1/students/<int:student_id>")
    def update_student(student_id):
        student = db.session.get(Student, student_id)

        if not student:
            return jsonify({"error": "student not found"}), 404

        data = request.get_json(silent=True) or {}

        for field in ("name", "email", "age"):
            if field in data:
                setattr(student, field, data[field])

        try:
            db.session.commit()
            logger.info("Updated student id=%s", student_id)
            return jsonify(student.to_dict()), 200

        except Exception:
            db.session.rollback()
            logger.exception(
                "Failed to update student id=%s",
                student_id
            )
            return jsonify({"error": "student could not be updated"}), 409

    @app.delete("/api/v1/students/<int:student_id>")
    def delete_student(student_id):
        student = db.session.get(Student, student_id)

        if not student:
            return jsonify({"error": "student not found"}), 404

        db.session.delete(student)
        db.session.commit()

        logger.info("Deleted student id=%s", student_id)

        return "", 204

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000"))
    )
