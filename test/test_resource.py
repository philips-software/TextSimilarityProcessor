"""Koninklijke Philips N.V., 2019 - 2020. All rights reserved.
This file holds the test resources for testing """
import os
from os import listdir
from os.path import isfile, join


class TestResource:
    """This test class stores data required to test the functionality
    skipping from the presentation layer to IO layer"""
    # pylint: disable=too-few-public-methods
    testcase_id = 0
    teststeps_id = str("1,2")
    sim_range = str("60,100")
    var = 0
    get_new_text = "this should not get called"
    command_unique_id = "0"
    command_colint = "1,2"
    num_row = "8"

    tst_resource_folder = os.path.join(os.path.dirname(__file__), os.pardir, "test_resource")
    par_dir = os.path.join(os.path.dirname(__file__), os.pardir)

    file_path = os.path.abspath(os.path.join(tst_resource_folder, "Testcases.xlsx"))

    golden_merged_file_path = os.path.abspath(os.path.join(tst_resource_folder,
                                                           "golden_Testcases_merged_steps.xlsx"))
    golden_merged_file_empty_report = os.path.abspath(os.path.join(tst_resource_folder,
                                                                   "golden_Testcases_merged_empty_report.csv"))
    golden_brief_report_path = os.path.abspath(os.path.join(tst_resource_folder,
                                                            "golden_Testcases_brief_report.html"))

    golden_brief_report_path_line_ter = os.path.abspath(os.path.join(
        tst_resource_folder, "golden_Testcases_merged_empty_report_brief.html"))

    golden_recommendation_file_path = os.path.abspath(
        os.path.join(tst_resource_folder, "golden_Testcases_recommendation.xlsx"))
    golden_duplicate_id_file_path = os.path.abspath(os.path.join(
        tst_resource_folder, "golden_Testcases_Duplicate_ID.xlsx"))

    golden_new_merged_file_path = os.path.abspath(
        os.path.join(tst_resource_folder, "golden_new_Testcases_merged_steps.xlsx"))
    golden_new_recommendation_file_path = os.path.abspath(
        os.path.join(tst_resource_folder, "golden_new_Testcases_recommendation.csv"))

    log_file_path = os.path.abspath(os.path.join(par_dir, "similarity", "text_similarity.log"))
    empty_file_path = os.path.abspath(os.path.join(par_dir, "test_resource", "empty_testcase.xlsx"))

    @staticmethod
    def get_list_files():
        """ Function to get the list of files the resource folder"""
        onlyfiles = [f for f in listdir(os.path.join(os.path.dirname(__file__), os.pardir, "test_resource"))
                     if isfile(join(os.path.join(os.path.dirname(__file__), os.pardir, "test_resource"), f))]
        return onlyfiles

    @staticmethod
    def get_newfiles():
        """ Function to get the files other than the reference files"""
        golden_files = ["empty_testcase.xlsx", "golden_new_Testcases_merged_steps.xlsx",
                        "golden_new_Testcases_recommendation.csv", "Testcases.xlsx",
                        "golden_Testcases_brief_report.html", "golden_Testcases_Duplicate_ID.xlsx",
                        "golden_Testcases_merged_empty_report.csv", "golden_Testcases_merged_empty_report_brief.html",
                        "golden_Testcases_merged_steps.xlsx", "golden_Testcases_recommendation.xlsx", "cmd_help.txt"]
        return list(set(TestResource.get_list_files()) - set(golden_files))

    @staticmethod
    def clean_unnecessary_files():
        """Function to remove the files other than the reference files"""
        if TestResource.get_newfiles():
            for element in TestResource.get_newfiles():
                if os.path.exists(os.path.join(os.path.dirname(__file__), os.pardir, "test_resource", element)):
                    os.remove(os.path.join(os.path.dirname(__file__), os.pardir, "test_resource", element))

    @staticmethod
    def get_result_(file_starts):
        """ Function to return file name when sub string name is given"""
        prefixed = [filename for filename in os.listdir(os.path.join(os.path.dirname(__file__),
                                                                     os.pardir, "test_resource"))
                    if filename.startswith(file_starts)]
        if not len(prefixed) == 1:
            str1 = None
            print("unable to identify file")
        else:
            str1 = ''.join(prefixed)
        return os.path.join(os.path.dirname(__file__), os.pardir, "test_resource", str1)
