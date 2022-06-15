import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format("postgres","Aweayo",'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    #tests for get categories endpoint

    def test_get_all_categories(self):
        res = self.client().get('/api/v1/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200) # status code is 200
        self.assertEqual(data["success"],True) # the value of success is set to True
        self.assertTrue(len(data["categories"])) # categories exist
        pass

    def test_404_for_invalid_category_endpoint(self):
        res = self.client().get('/api/v1/categories/3')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data["success"],False)
        self.assertTrue(data["error"])
        self.assertTrue(data["message"])
        pass

    def test_get_paginated_questions(self):
        res = self.client().get('/api/v1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data["success"],True)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["categories"]))
        self.assertTrue(data["current_category"])
        pass

    def test_404_page_exceeded_number_of_questions(self):
        res = self.client().get('/api/v1/questions?page=2000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data["success"],False)
        self.assertTrue(data["error"])
        self.assertTrue(data["message"])

        pass

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()