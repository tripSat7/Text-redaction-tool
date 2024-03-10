import unittest
import censoror as testObj

class PhoneTestCase(unittest.TestCase):
    def test_censor_phone_numbers(self):
        sample_text = "Reach me at 123-456-7890."
        entity_types = {'names': [], 'dates': [], 'phones': ['CARDINAL'], 'address': []}
        censored_text = testObj.censor_info(sample_text, entity_types)

        expected_censored_portion = "█" * 3
        expected_uncensored_portion = "456-7890"

        self.assertIn(expected_censored_portion, censored_text, f"Expected censored portion '{expected_censored_portion}' not found.")
        self.assertIn(expected_uncensored_portion, censored_text, f"Expected uncensored portion '{expected_uncensored_portion}' should remain.")

        expected_output = "Reach me at ███-456-7890."
        self.assertEqual(censored_text, expected_output, f"Expected output '{expected_output}' does not match actual output.")

if __name__ == "__main__":
    unittest.main()
