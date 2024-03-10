import unittest
import censoror as testObj

class AddressTestCase(unittest.TestCase):

    def test_censor_address(self):
        sample_text = "He lives at 1234 Main St, Springfield."
        entity_types = {
            'names': [],
            'dates': [],
            'phones': [],
            'address': ['ORG', 'FAC', 'GPE']
        }
        censored_text = testObj.censor_text(sample_text, entity_types)

        
        expected_censored_parts = [
            "1234",  
            "█" * len("Main St"),
            "█" * len("Springfield") 
        ]

        for part in expected_censored_parts:
            self.assertIn(part, censored_text, f"Expected censored part '{part}' not found in censored text.")


if __name__ == "__main__":
    unittest.main()
