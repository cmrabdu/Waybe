import os
import tempfile
import unittest

from mobility import create_app



class TestUser(unittest.TestCase):

    def setUp(self):
        # generate a temporary file for the test db
        self.db_fd, self.db_path = tempfile.mkstemp()
        # create the testapp with the temp file for the test db
        self.app = create_app({'TESTING': True, 'DATABASE': self.db_path})
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.db = get_db()

        # read in SQL for populating test data
        with open(os.path.join(os.path.dirname(__file__), "schema_test.sql"), "rb") as f:
            self.db.executescript(f.read().decode("utf8"))

    def tearDown(self):
        # closing the db and cleaning the temp file
        close_db()
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def test_search_by_email(self):
        # unit test against the test db.
        # some function that get cities by postal code
        villes = some_package.some_search_code_postal(4000)
        self.assertEqual(len(villes), 1)
        self.assertEqual(villes[0]["nom"], 'Liège')


if __name__ == '__main__':
    unittest.main(verbosity=2)