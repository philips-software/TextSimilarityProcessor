"""Koninklijke Philips N.V., 2019 - 2020. All rights reserved.
script to conduct sanity test"""
import os
import unittest
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "test"))
from test_resource import TestResource # pylint: disable=E0611
from verify_path import FunctionalTestVerification # pylint: disable=E0401
from subprocess_calls import call_subprocess


class SanityTestVerification(unittest.TestCase):
    """
    class to consolidate the sanity tests
    """
    verify_func_obj = FunctionalTestVerification()

    @classmethod
    def tearDown(cls):
        """"Deletes the files created: merged, recommendation and duplicate."""
        if os.path.exists(TestResource.recommendation_file_path):
            os.remove(TestResource.recommendation_file_path)
        if os.path.exists(TestResource.duplicate_id_file_path):
            os.remove(TestResource.duplicate_id_file_path)
        if os.path.exists(TestResource.merged_file_path):
            os.remove(TestResource.merged_file_path)
        if os.path.exists(TestResource.brief_report_path):
            os.remove(TestResource.brief_report_path)

    def test_execute_sanity_suite(self):
        """
        Function which executes the sanity test
        """
        input_file = os.path.join(os.path.abspath(os.path.join(__file__, os.pardir, os.pardir)),
                                  "test_resource", "Testcases.xlsx")
        call_subprocess('python3 -m similarity --p "%s" --u 0 --c "1,2" --n "8"' % input_file)
        self.verify_func_obj.verify_functional_test()
        print("Sanity test is COMPLETED & PASSED")


if __name__ == '__main__':
    unittest.main()
