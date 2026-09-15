import os
import tempfile
import unittest

from app import create_app, db


class StudentApiTestCase(unittest.TestCase):
    def setUp(self):
        self.db_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.db_file.close()
        self.app = create_app()
        self.app.config.update(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI=f"sqlite:///{self.db_file.name}",
        )
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
        os.unlink(self.db_file.name)

    def test_healthcheck(self):
        response = self.client.get("/healthcheck")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "ok")

    def test_student_crud(self):
        response = self.client.post("/api/v1/students", json={"name": "Sandeep", "email": "sandeep@example.com", "age": 22})
        self.assertEqual(response.status_code, 201)
        student_id = response.json["id"]

        self.assertEqual(self.client.get(f"/api/v1/students/{student_id}").status_code, 200)
        self.assertEqual(self.client.get("/api/v1/students").status_code, 200)
        self.assertEqual(self.client.put(f"/api/v1/students/{student_id}", json={"age": 23}).status_code, 200)
        self.assertEqual(self.client.delete(f"/api/v1/students/{student_id}").status_code, 204)


if __name__ == "__main__":
    unittest.main()
