from unittest import TestCase, main
import company_data
import ratings_data
import variable_weighting_data
import data


class TestExtractors(TestCase):
    
    def test_exracted_data_must_be_dictionary(self):
        self.assertEqual(type(company_data.extractData()),dict)
        self.assertEqual(type(ratings_data.getRatingsData()),dict)
        self.assertEqual(type(ratings_data.getScoresData()),dict)
        self.assertEqual(type(variable_weighting_data.getWeightingData()),dict)




if __name__ == "__main__":
    main()

