""" This file does the  test of the "Text similarity processor
from IO layer as well as cmdliner """

import os
import unittest
import subprocess
from test.test_resource import TestResource
import numpy as np
from cosine_source.cosine_io import CosineIO
from cosine_source.cosine_io import is_nan


class IoTestCase(unittest.TestCase):
    """ This test class verifies the Text similarity index processing to cover
    cosine_io.py and cosine_core.py and cosine_cmd.py """

    def test_isnan(self):
        """ Function to test isnan """
        self.assertEqual(False, is_nan(345), "Validating isnan function for a float val")
        self.assertEqual(True, is_nan(np.nan), "Validating isnan function for a nan val")
        self.assertEqual(False, is_nan("test"), "Validating isnan function for a string val")

    def validate_input(self, path, similarity, uniqid, colint, log_loc, msg):
        """Function test the incorrect path input file"""
        text_check = msg
        flag = False
        cos_io_obj = CosineIO(path, similarity, uniqid, colint, 0)
        cos_io_obj.orchestrate_cosine()
        line = subprocess.check_output(['tail', log_loc, TestResource.log_file_path])
        line = line.decode('UTF-8')
        if text_check in line:
            flag = True
        self.assertEqual(True, flag, "Validating %s log file"%str(msg))

    def test_input_validation(self):
        """ Function to test the input arguments """
        self.validate_input(os.path.abspath(os.path.join(
            TestResource.tst_resource_folder, "Testcases.xls")), TestResource.similarity_index,
                            TestResource.testcase_id, TestResource.teststeps_id, "-1", 'File path is invalid')

        self.validate_input(TestResource.file_path, 101,
                            TestResource.command_unique_id, TestResource.command_colint, "-3",
                            'Similarity index is not less than 100')

        self.validate_input(TestResource.file_path, 0,
                            TestResource.command_unique_id, TestResource.command_colint, "-3",
                            'Similarity index is not less than 100')

        self.validate_input(TestResource.file_path, TestResource.command_similarity,
                            10, TestResource.command_unique_id, "-3",
                            'Either or both unique id and col of interest out of range')

        self.validate_input(TestResource.file_path, TestResource.command_similarity,
                            TestResource.command_unique_id, "1,7", "-3",
                            'Either or both unique id and col of interest out of range')

        self.validate_input(TestResource.file_path, TestResource.command_similarity,
                            TestResource.command_unique_id, "test, x", "-3",
                            'Input data is not an integer')

        self.validate_input(TestResource.file_path, TestResource.command_similarity,
                            TestResource.command_unique_id, "1,2,3,4,5", "-3",
                            'Either or both unique id and col of interest out of range')


if __name__ == '__main__':

    unittest.main()
