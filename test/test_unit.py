""" This file does the Unit test of the "Text similarity processor
core cosine algorithm """
import unittest
from collections import Counter
import similarity_processor.similarity_core as cc


class MyUnitTestCase(unittest.TestCase):
    """This class verifies the individual functionality of the units:
    get_cosine()
    text_to_vector()
    check_ tolerance()
    methods with valid and invalid inputs, which verifies the function behaviour"""

    def test_get_positive_cosine(self):
        """This method checks the value returned by the cosine_core.get_cosine()
        for vector 1, vector 2: Input vector from the texts to be compared - positive cosine """
        positive_cosine = cc.get_cosine(Counter({"hello": 16, "Language": 30, "python": 66}),
                                        Counter({"Mac": 9, "MANGO": 27, "python": 88, "hello": 5}))
        self.assertEqual(0.8562387195638202, positive_cosine, "Value should not be equal to 0")

    def test_get_negative_cosine(self):
        """This method checks the value returned by the cosine_core.get_cosine()
        for vector 1, vector 2: Input vector from the texts to be compared - negative cosine value"""
        negative_cosine = cc.get_cosine(Counter({"hello_World": 99}),
                                        Counter({"TEST": 888}))
        self.assertEqual(0.0, negative_cosine, "Value should be 0.0")

    def test_get_cosine_same(self):
        """This method checks the value returned by the cosine_core.get_cosine()
        for vector 1, vector 2: Input vector from the texts to be compared"""
        positive_cosine = cc.get_cosine(Counter({"hello": 16, "Language": 30, "python": 66}),
                                        Counter({"hello": 16, "Language": 30, "python": 66}))
        self.assertEqual(1.0, positive_cosine, "Value should not be equal to 0")

    def test_get_cosine_none(self):
        """This method checks the value returned by the cosine_core.get_cosine()
        for vector 1, vector 2: Input vector from the texts to be compared"""
        _cosine = cc.get_cosine(Counter({"": 0}),
                                Counter({"": 0}))
        self.assertEqual(0.0, _cosine, "Value should be equal to 0")

    def test_text_to_invalid_vector(self):
        """This method checks the value returned by the cosine_core.text_to_vector()
        for converting text to vector for invalid input """
        negative_text = None
        try:
            negative_text = cc.text_to_vector(1234567.988766)
        except TypeError as err:
            print('Error: ', str(err))
        self.assertIsNone(negative_text, "Vector should not be generated")

    def test_text_to_valid_vector(self):
        """This method checks the value returned by the cosine_core.text_to_vector()
        for converting text to vector for valid input """
        text = "What is generator in Python with example Python generators \
                are a simple, A Counter is a container that"
        positive_text = cc.text_to_vector(text)
        self.assertEqual(Counter, type(positive_text),
                         "Counter vector should be generated from text")


if __name__ == '__main__':
    unittest.main()
