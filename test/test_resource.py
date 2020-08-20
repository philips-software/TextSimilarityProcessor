"""Koninklijke Philips N.V., 2019 - 2020. All rights reserved.
This file holds the test resources for testing """
import os


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
    merged_file_path = os.path.abspath(os.path.join(tst_resource_folder,
                                                    "Testcases_merged_steps_0.xlsx"))
    brief_report_path = os.path.abspath(os.path.join(tst_resource_folder,
                                                     "Testcases_brief_report.html"))
    recommendation_file_path = os.path.abspath(os.path.join(tst_resource_folder,
                                                            "Testcases_recommendation_0.xlsx"))
    duplicate_id_file_path = os.path.abspath(os.path.join(tst_resource_folder,
                                                          "Testcases_Duplicate_ID_0.xlsx"))

    golden_merged_file_path = os.path.abspath(os.path.join(tst_resource_folder,
                                                           "golden_Testcases_merged_steps.xlsx"))
    golden_merged_file_empty_report = os.path.abspath(os.path.join(tst_resource_folder,
                                                                   "golden_Testcases_merged_empty_report.csv"))
    golden_brief_report_path = os.path.abspath(os.path.join(tst_resource_folder,
                                                            "golden_Testcases_brief_report.html"))

    golden_brief_report_path_line_ter = os.path.abspath(os.path.join(
        tst_resource_folder, "golden_Testcases_merged_empty_report_brief.html"))

    brief_report_path_line_ter = os.path.abspath(os.path.join(
        tst_resource_folder, "golden_Testcases_merged_empty_report_brief_report.html"))

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
