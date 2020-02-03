""" This file does the  test of the "Text similarity processor
logging and commandline """

import os
import unittest
import filecmp
import subprocess
from datetime import datetime
from test.test_resource import TestResource
from similarity_processor.similarity_cmd import create_parser
import similarity_logging as cl
LOG = cl.get_logger()


def check_create_parser(option, value):
    """ create a parser for commandline input and return handle"""
    return create_parser([option, value])


class ParserAndLogTest(unittest.TestCase):
    """ Class to test the logging and command line input feature """
    def test_path(self):
        """ Function to test the path variable in the command line
        correct and incorrect """
        with self.assertRaises(SystemExit):
            check_create_parser("-p", "path_test")
        parsed = check_create_parser("--p", "path_test")
        self.assertEqual(parsed.path, "path_test")

    def test_simindex(self):
        """ Function to test the similarity index variable in the command line
                correct and incorrect """
        with self.assertRaises(SystemExit):
            check_create_parser("-s", "simindex_test")
        parsed = check_create_parser("--s", "simindex_test")
        self.assertEqual(parsed.simindex, "simindex_test")

    def test_uniqid(self):
        """ Function to test the unique id  variable in the command line
                correct and incorrect """
        with self.assertRaises(SystemExit):
            check_create_parser("-u", "uniqid_test")
        parsed = check_create_parser("--u", "uniqid_test")
        self.assertEqual(parsed.uniqid, "uniqid_test")

    def test_colint(self):
        """ Function to test the column of interest variable in the command line
                correct and incorrect """
        with self.assertRaises(SystemExit):
            check_create_parser("-c", "colint_test")
        parsed = check_create_parser("--c", "colint_test")
        self.assertEqual(parsed.colint, "colint_test")

    def test_from_command_help(self):
        """Test function to test the commandline help option"""
        script = os.path.abspath(os.path.join(TestResource.par_dir,
                                              "similarity_processor", "similarity_cmd.py"))
        cmd = 'python3.7 %s --h'%script
        output = open(os.path.join(TestResource.tst_resource_folder, "cmd_help.txt"), "r")
        tmpfile = open(os.path.join(TestResource.tst_resource_folder, "tmp_help.txt"), "w")
        process = subprocess.Popen(cmd, stdout=tmpfile, shell=True).communicate()[0]
        print(process)
        tmpfile.close()
        output.close()
        self.assertEqual(True, (filecmp.cmp(os.path.join(TestResource.tst_resource_folder, "cmd_help.txt"),
                                            os.path.join(TestResource.tst_resource_folder, "tmp_help.txt"))),
                         "Help option validated")
        if os.path.exists(os.path.join(TestResource.tst_resource_folder, "tmp_help.txt")):
            os.remove(os.path.join(TestResource.tst_resource_folder, "tmp_help.txt"))

    def test_log(self):
        """ Function to test the logging functionality and format of logging (except millisec) """
        message = "sample message"
        LOG.info(message)
        current_date_time = str(datetime.now())
        # millisec = current_date_time.split(".")[1]
        date_time = current_date_time.split(".")[0]
        line = subprocess.check_output(['tail', '-1', TestResource.log_file_path])
        line = str(line.decode('UTF-8')).split(",")
        act_date = line[0]
        act_message = line[1][4:]
        self.assertEqual(str(message).strip(), str(act_message).strip(), "Loge message verified")
        self.assertEqual(date_time, act_date, "Loge message date& time verified")
