<<<<<<< HEAD
import logging
import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"), format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger(__name__)

db = SQLAlchemy()

class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    age = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email, "age": self.age}


def create_app():
    app = Flask(__name__)
    database_url = os.getenv("DATABASE_URL", "sqlite:///students.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

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
            student = Student(name=data["name"], email=data["email"], age=data["age"])
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
        return jsonify([s.to_dict() for s in Student.query.order_by(Student.id).all()]), 200

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
            logger.exception("Failed to update student id=%s", student_id)
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
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
=======
import os
import logging

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    "sqlite:///students.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "age": self.age
        }


@app.get("/healthcheck")
def healthcheck():
    return jsonify({"status": "ok"})


@app.post("/api/v1/students")
def create_student():
    data = request.get_json()

    if not data or not all(k in data for k in ["name", "email", "age"]):
        return jsonify({"error": "name, email and age are required"}), 400

    student = Student(
        name=data["name"],
        email=data["email"],
        age=data["age"]
    )

    try:
        db.session.add(student)
        db.session.commit()
        logger.info("Student created: %s", student.id)
    except Exception:
        db.session.rollback()
        return jsonify({"error": "student already exists"}), 409

    return jsonify(student.to_dict()), 201


@app.get("/api/v1/students")
def get_students():
    students = Student.query.all()
    return jsonify([s.to_dict() for s in students])


@app.get("/api/v1/students/<int:id>")
def get_student(id):
    student = db.session.get(Student, id)

    if not student:
        return jsonify({"error": "student not found"}), 404

    return jsonify(student.to_dict())


@app.put("/api/v1/students/<int:id>")
def update_student(id):
    student = db.session.get(Student, id)

    if not student:
        return jsonify({"error": "student not found"}), 404

    data = request.get_json()

    student.name = data.get("name", student.name)
    student.email = data.get("email", student.email)
    student.age = data.get("age", student.age)

    db.session.commit()

    return jsonify(student.to_dict())


@app.delete("/api/v1/students/<int:id>")
def delete_student(id):
    student = db.session.get(Student, id)

    if not student:
        return jsonify({"error": "student not found"}), 404

    db.session.delete(student)
    db.session.commit()

    return "", 204


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000))
    )
>>>>>>> d3ea701 (add REST API and Dockerization)
