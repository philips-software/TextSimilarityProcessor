"""Koninklijke Philips N.V., 2019 - 2020. All rights reserved.
This file does the  test of the Text similarity processor logging and command line """

import os
import unittest
import filecmp
import subprocess
from datetime import datetime
from test.test_resource import TestResource
from similarity.similarity_cmd import create_parser
import similarity_logging as cl
LOG = cl.get_logger()


def check_create_parser(option, value):
    """ create a parser for command line input and return handle"""
    return create_parser([option, value])


class ParserAndLogTest(unittest.TestCase):
    """ Class to test the logging and command line input feature """

    @classmethod
    def tearDown(cls):
        """"Deletes the files created: merged, recommendation and duplicate."""
        TestResource.clean_unnecessary_files()

    def cmd_args(self, actual, arg, arg_text, exp):
        """ Template function to test the commandline arguments"""
        with self.assertRaises(SystemExit):
            check_create_parser(arg, arg_text)
        self.assertEqual(actual, exp, "tested %s" % arg_text)

    def test_commandline_options(self):
        """ Function to test the similarity command line options """
        self.cmd_args(check_create_parser("--c", "colint_test").filter, "-f", 'range_test', 500000)
        self.cmd_args(check_create_parser("--f", "500").filter, "-f", '1,2', 500)
        self.cmd_args(check_create_parser("--c", "colint_test").range, "-r", 'range_test', "60,100")
        self.cmd_args(check_create_parser("--r", '1,2').range, "-r", '1,2', "1,2")
        self.cmd_args(check_create_parser("--c", "colint_test").numrowcount, "-n", '1', 100)
        self.cmd_args(check_create_parser("--n", '1').numrowcount, "-n", '1', 1)
        self.cmd_args(check_create_parser("--c", "colint_test").colint, "-c", "colint_test", "colint_test")
        self.cmd_args(check_create_parser("--u", "uniqid_test").uniqid, "-u", "uniqid_test", "uniqid_test")
        self.cmd_args(check_create_parser("--p", "path_test").path, "-p", "path_test", "path_test")

    def test_from_command_help(self):
        """Test function to test the command line help option"""
        script = os.path.abspath(os.path.join(TestResource.par_dir,
                                              "similarity"))
        cmd = 'python %s --h'%script
        output = open(os.path.join(TestResource.tst_resource_folder, "cmd_help.txt"), "r")
        tmpfile = open(os.path.join(TestResource.tst_resource_folder, "tmp_help.txt"), "w")
        process = subprocess.Popen(cmd, stdout=tmpfile, shell=True).communicate()[0] # pylint: disable=W0612
        tmpfile.close()
        output.close()
        self.assertEqual(True, (filecmp.cmp(os.path.join(TestResource.tst_resource_folder, "cmd_help.txt"),
                                            os.path.join(TestResource.tst_resource_folder, "tmp_help.txt"))),
                         "Help option validated")
        if os.path.exists(os.path.join(TestResource.tst_resource_folder, "tmp_help.txt")):
            os.remove(os.path.join(TestResource.tst_resource_folder, "tmp_help.txt"))

    def test_log(self):
        """ Function to test the logging functionality and format of logging (except milliseconds ) """
        message = "sample message"
        LOG.info(message)
        current_date_time = str(datetime.now())
        # millisec = current_date_time.split(".")[1]
        date_time = current_date_time.split(".")[0]
        line = subprocess.check_output(["tail", "-1", TestResource.log_file_path])
        line = str(line.decode("UTF-8")).split(",")
        act_date = line[0]
        act_message = line[1][4:]
        self.assertEqual(str(message).strip(), str(act_message).strip(), "Loge message verified")
        self.assertEqual(date_time, act_date, "Loge message date& time verified")
