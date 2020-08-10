"""Koninklijke Philips N.V., 2019 - 2020. All rights reserved.
This file does the functional test of the "Text similarity
from IO layer as well as UI later """
import os
import unittest
import subprocess
from test.test_resource import TestResource
from test.verify_path import FunctionalTestVerification
from similarity_processor.similarity_io import SimilarityIO
# Below codes are comments as they cannot be executed in CI
# from tkinter import Tk
# from similarity_processor.similarity_ui import TextSimilarityWindow


class MyFunctionalTestCase(unittest.TestCase):
    """ This test class verifies the Text similarity index processing to cover
    similarity_io.py and similarity_core.py file with a test resources
    which simulates the user input file with defined formats required / allowed by the tool """
    verify_func_obj = FunctionalTestVerification()
    @classmethod
    def tearDown(cls):
        """"Deletes the files created: merged, recommendation and duplicate."""
        if os.path.exists(TestResource.merged_file_path):
            os.remove(TestResource.merged_file_path)
        if os.path.exists(TestResource.recommendation_file_path):
            os.remove(TestResource.recommendation_file_path)
        if os.path.exists(TestResource.duplicate_id_file_path):
            os.remove(TestResource.duplicate_id_file_path)
        if os.path.exists(TestResource.brief_report_path):
            os.remove(TestResource.brief_report_path)

    def test_below_ui(self):
        """ Test function which injects the user input data skipping the
        presentation later to the IO layer to check the underlying functionality """

        cosine = SimilarityIO(TestResource.file_path,
                              TestResource.testcase_id, TestResource.teststeps_id, TestResource.sim_range,
                              TestResource.num_row, TestResource.var, TestResource.get_new_text)
        cosine.orchestrate_similarity()
        self.verify_func_obj.verify_functional_test()

    # # Below codes are comments as they cannot be executed in CI
    # def test_from_ui_new_text(self):
    #     """Test function which injects the user input data at the presentation later
    #     to check the end to end functionality"""
    #     window = Tk()
    #     win = TextSimilarityWindow(window)
    #     win.check_is_new_text.invoke()
    #     win.path_t.insert(0, str(TestResource.file_path))
    #     win.uniq_id_t.insert(0, 0)
    #     win.steps_t.insert(0, "1,2")
    #     win.new_text.insert(0, "a3 d4")
    #     win.submit.invoke()
    #     window.quit()
    #     self.verify_func_objs.verify_functional_test(True)

    def test_from_command_line(self):
        """Test function which provides input using command line interface"""
        script = os.path.abspath(os.path.join(TestResource.par_dir,
                                              "similarity_processor", "similarity_cmd.py"))
        cmd = 'python %s --p "%s" --u "%s" --c "%s" --n "%s"' % (
            script, TestResource.file_path,
            TestResource.command_unique_id, TestResource.command_colint, TestResource.num_row)
        os.system(cmd)
        self.verify_func_obj.verify_functional_test()

    def test_invalid_file(self):
        """Function test the empty file/ incorrect data/ extra sheet in the input file"""
        text_check = 'Input data is incorrect/ file is invalid/It has more than one sheet'
        flag = False
        cos_io_obj = SimilarityIO(TestResource.empty_file_path,
                                  TestResource.command_unique_id, TestResource.command_colint, TestResource.num_row, 0)
        cos_io_obj.orchestrate_similarity()
        line = subprocess.check_output(["tail", "-1", TestResource.log_file_path])
        line = line.decode("UTF-8")
        if text_check in line:
            flag = True
        self.assertEqual(True, flag, "Validating empty input file from log file")


if __name__ == '__main__':

    unittest.main()
