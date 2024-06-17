import unittest
from operationalize.tasks.task import RatingTask

class TestRatingTask(unittest.TestCase):

    def setUp(self):
        self.rating_task = RatingTask(name="Test Rating Task")

    def test_ratings_are_appended_correctly(self):
        self.rating_task.submit_rating(5)
        self.rating_task.submit_rating(3)
        self.assertIn(5, self.rating_task.ratings)
        self.assertIn(3, self.rating_task.ratings)
        self.assertEqual(len(self.rating_task.ratings), 2)

    def test_store_ratings_correctly_writes_to_file(self):
        self.rating_task.submit_rating(4)
        self.rating_task.store_ratings()
        with open("ratings.json", "r") as file:
            content = file.read()
        self.assertIn("4", content)
