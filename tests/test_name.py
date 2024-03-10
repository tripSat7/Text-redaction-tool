import unittest
import censoror as testObj
import os

class NameTestCase(unittest.TestCase):

    def test_censor_names(self):
        text_with_names = "John Doe went to New York."
        entity_types = {
            'names': ['PERSON'],
            'dates': [], 
            'phones': [],
            'address': []
        }
        censored = testObj.censor_info(text_with_names, entity_types)
        self.assertNotIn("John Doe", censored)
        self.assertIn("█" * len("John Doe"), censored)


if __name__ == "__main__":
    unittest.main()
