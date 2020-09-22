"""Koninklijke Philips N.V., 2019 - 2020. All rights reserved.
This file does the tests for "Text similarity processor from IO layer """
import os
import unittest
import subprocess
from test.test_resource import TestResource
import pandas as pd
from similarity.similarity_io import SimilarityIO


class TestSimilarityIO(unittest.TestCase):
    """ This test class verifies the Text similarity to cover similarity_io.py """

    @classmethod
    def tearDown(cls):
        """"Deletes the files created: merged, recommendation and duplicate."""
        TestResource.clean_unnecessary_files()

    def test_check_init(self):
        """ This test function tests the default arguments of similarity_io """
        similarity_obj = SimilarityIO(TestResource.file_path, TestResource.command_unique_id,
                                      TestResource.command_colint)
        self.assertEqual(similarity_obj.num_html_row, 100, "Default number of HTML rows")
        self.assertEqual(similarity_obj.is_new_text, False, "Default is new text")
        self.assertEqual(similarity_obj.filter_range, "60,100", "Default filter range")
        self.assertEqual(similarity_obj.new_text, None, "Default new text")
        self.assertEqual(similarity_obj.report_row_filter, 500000, "Default report row limiter")
        self.assertEqual(similarity_obj.data_frame, None, "Default dataframe")
        self.assertEqual(similarity_obj.uniq_header, None, "Default unique header")

    def test_check_assignment(self):
        """ This test function tests the  arguments assignment of similarity_io """
        similarity_obj = SimilarityIO("TestResource.file_path", "1",
                                      "1,2", "10,20", 10, True, "abc", 10)
        self.assertEqual(similarity_obj.file_path, "TestResource.file_path", "Path check")
        self.assertEqual(int(similarity_obj.uniq_id), 1, "Unique ID check")
        self.assertEqual(similarity_obj.col_int, "1,2", "Col of interest check")
        self.assertEqual(similarity_obj.num_html_row, 10, "Default number of HTML rows")
        self.assertEqual(similarity_obj.is_new_text, True, "Default is new text")
        self.assertEqual(similarity_obj.filter_range, "10,20", "Default filter range")
        self.assertEqual(similarity_obj.new_text, "abc", "Default new text")
        self.assertEqual(similarity_obj.report_row_filter, 10, "Default report row limiter")

    def test_html_write_df(self):
        """ This test function tests the html reporting function with non default similarity range """
        dataframe = pd.read_excel(TestResource.golden_merged_file_path, usecols='B:C')
        similarity_io_obj = SimilarityIO(None, None, None)
        similarity_io_obj.file_path = os.path.join(os.path.dirname(__file__), os.pardir, "test_resource")
        similarity_io_obj.data_frame = dataframe
        mapping = {similarity_io_obj.data_frame.columns[0]: 'Uniq ID', similarity_io_obj.data_frame.columns[1]: 'Steps'}
        similarity_io_obj.data_frame.rename(columns=mapping, inplace=True)
        similarity_io_obj.filter_range = "90,100"
        similarity_io_obj.uniq_header = "Uniq ID"  # Unique header of the input data frame
        TestResource.clean_unnecessary_files()
        processed_similarity = similarity_io_obj.process_cos_match()
        similarity_io_obj.report(processed_similarity)
        self.assertEqual(True, os.path.isfile(TestResource.get_result_("similarity_brief_report")))
        self.assertEqual(True, os.path.isfile(TestResource.get_result_("similarity_recommendation_0")))

    def wrong_range(self, filter_range, msg):
        """ This support function tests the wrong range logging """
        flag = False
        similarity_obj = SimilarityIO(TestResource.file_path, "1",
                                      "1,2", filter_range, 10, True, "abc", 10)
        similarity_obj.orchestrate_similarity()
        line = subprocess.check_output(["tail", "-1", TestResource.log_file_path])
        line = line.decode("UTF-8")
        if "Either of range value is wrong" in line:
            flag = True
        self.assertEqual(True, flag, "Validating %s log file" % str(msg))

    def test_wrong_range(self):
        """ This test function tests the wrong range values """
        self.wrong_range("1000, 20", "Range val 1 wrong +ve")
        self.wrong_range("10, 200", "Range val 2 wrong +ve")
        self.wrong_range("10, -1", "Range val 2 wrong -ve")
        self.wrong_range("-1, 10", "Range val 1 wrong -ve")

    def test_empty_report_df(self):
        """ This test function tests the logging when the report dataframe is empty """
        flag = False
        similarity_obj = SimilarityIO(TestResource.golden_merged_file_empty_report, "0",
                                      "1", "99,100", 10, True, "abc", 10)
        similarity_obj.orchestrate_similarity()
        line = subprocess.check_output(["tail", "-1", TestResource.log_file_path])
        line = line.decode("UTF-8")
        if "Nothing to write to html file" in line:
            flag = True
        self.assertEqual(True, flag, "Validating %s log file for Nothing to write to html file")

    def test_multiple_report(self):
        """ This test function tests the html reporting function with line length more than 200, to test the text
        wrap and also to test the multiple xlsx reporting by reducing the row splitter(20) """
        df_list_0 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
        df_list_1 = [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]
        similarity_obj = SimilarityIO(TestResource.golden_merged_file_empty_report, "0",
                                      "1", "0,100", 100, False, None, 20)
        TestResource.clean_unnecessary_files()

        similarity_obj.orchestrate_similarity()
        self.assertEqual(True, os.path.isfile(TestResource.get_result_(
            "golden_Testcases_merged_empty_report_recommendation_0")))
        self.assertEqual(True, os.path.isfile(TestResource.get_result_(
            "golden_Testcases_merged_empty_report_recommendation_1")))
        data_frame = (pd.read_excel(TestResource.get_result_(
            "golden_Testcases_merged_empty_report_recommendation_0")))
        self.assertEqual(list(data_frame.index).sort(), df_list_0.sort(),
                         "Validating %s log file for Nothing to write to html file")
        data_frame = (pd.read_excel(TestResource.get_result_(
            "golden_Testcases_merged_empty_report_recommendation_1")))
        self.assertEqual(list(data_frame.index).sort(), df_list_1.sort(), "Validating %s log file for Nothing to write "
                                                                          "to html file")
        act_html_report = pd.read_html(TestResource.get_result_("golden_Testcases_merged_empty_report_brief_report"))
        ref_html_report = pd.read_html(TestResource.golden_brief_report_path_line_ter)
        self.assertEqual(act_html_report[0].replace(r'\\r', '', regex=True).values.tolist(),
                         ref_html_report[0].replace(r'\\r', '', regex=True).values.tolist())
