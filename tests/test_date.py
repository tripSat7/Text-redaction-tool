from unittest.mock import MagicMock, patch
import unittest
import censoror as testObj

class DateTestCase(unittest.TestCase):

    @patch('censoror.language_processor')
    def test_censor_dates(self, mock_nlp):
        # Configure the mock to simulate expected behavior
        mock_ent = MagicMock(text="12/25/2020", label_="DATE", start_char=16, end_char=26)
        mock_doc = MagicMock(ents=[mock_ent])
        mock_nlp.return_value = mock_doc

        sample_text = "The event is on 12/25/2020."
        entity_types = {'names': [], 'dates': ['DATE'], 'phones': [], 'address': []}
        censored_text = testObj.censor_info(sample_text, entity_types)

        expected_censored = "The event is on ██████████."
        self.assertEqual(censored_text, expected_censored, "Date was not censored as expected.")

if __name__ == "__main__":
    unittest.main()
