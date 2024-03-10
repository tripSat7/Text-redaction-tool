import unittest
import os

class TestFileExistence(unittest.TestCase):

    def test_censoror_file_exists(self):
        file_path = './censoror.py'

        # Assert that the file exists at the given path
        self.assertTrue(os.path.exists(file_path), f"File '{file_path}' does not exist.")


if __name__ == "__main__":
    unittest.main()