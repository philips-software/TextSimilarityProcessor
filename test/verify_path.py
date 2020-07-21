"""Koninklijke Philips N.V., 2019 - 2020. All rights reserved."""

import os
import unittest
import pandas as pd
from test.test_resource import TestResource


def verify_file_path():
    """This function checks the required files are being generated
    or not"""
    if (os.path.exists(TestResource.merged_file_path) and
            os.path.exists(TestResource.recommendation_file_path) and
            os.path.exists(TestResource.duplicate_id_file_path)):
        return True
    return False


class FunctionalTestVerification(unittest.TestCase):
    """
    class consolidates the functional test verification
    """
    def verify_functional_test(self, new_text=False):
        """ This function verifies the result populated from the functional test """
        if verify_file_path():
            __data_duplicate = pd.read_excel(TestResource.golden_duplicate_id_file_path)

            if new_text:
                __data_merged = pd.read_excel(TestResource.golden_new_merged_file_path)
                __data_recomend = pd.read_csv(TestResource.golden_new_recommendation_file_path)
            else:
                __data_merged = pd.read_excel(TestResource.golden_merged_file_path)
                __data_recomend = pd.read_csv(TestResource.golden_recommendation_file_path)

            act_df_recomend = pd.read_csv(TestResource.recommendation_file_path)
            act_df_merged = pd.read_excel(TestResource.merged_file_path)
            act_df_duplicated = pd.read_excel(TestResource.duplicate_id_file_path)
            self.assertEqual(True, __data_recomend['SIMILARITY'].equals(act_df_recomend['SIMILARITY']),
                             "Actual and recommended Similarity Index data matches")
            self.assertEqual(True, __data_recomend['UNIQ ID'].equals(
                act_df_recomend['UNIQ ID']),
                             "Actual and recommended ['UNIQ ID'] data matches")
            self.assertEqual(True, __data_recomend['POTENTIAL MATCH'].equals(act_df_recomend['POTENTIAL MATCH']),
                             "Actual and recommended ['POTENTIAL MATCH'] data matches")
            self.assertEqual(True, __data_merged.equals(act_df_merged), "Actual and merged data matches")
            self.assertEqual(True, __data_duplicate.equals(act_df_duplicated),
                             "Actual and duplicated data matches")
        else:
            self.assertEqual(True, verify_file_path, "output files are not generated")
