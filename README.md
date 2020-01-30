[![Build Status](https://travis-ci.com/bkk003/text_de_duplication_monitoring.svg?branch=master)](https://travis-ci.com/bkk003/text_de_duplication_monitoring)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![codecov](https://codecov.io/gh/bkk003/text_de_duplication_monitoring/branch/master/graph/badge.svg)](https://codecov.io/gh/bkk003/text_de_duplication_monitoring)


Text Similarity Index processor
====================
What is the project intented to solve?
--------
Resolving the Technical Debt in "Test/Requirement/Issues/Any-text" repos with unique id using Natural Language Processing Continuous 
de-duplicate monitoring system in place to check the duplication of any new text added to "Test/Requirement/Issues/Any-text" bank. 
Grouping of similar "Test/Requirement/Issues/Any-text" helps in reduction of "Test/Requirement/Issues/Any-text" yet quality quotient remain same.  
Cycle time of test execution comes down as similar tests are identified for merging. 
Repeated requirement can be reduced Issues list can be merged/reduced


Technology stack 
--------
Python with few python packages mentioned in the [INSTALL.md](INSTALL.md) 

Status 
-------- 
This is a development release. There are known Issues/improvements & Limitations which will be taken up in the subsequent releases. Tool is open for the community to make changes for enhancement, bug fix etc.

Dependencies
--------
Python 3.7.3 (64bit)
 
[packages]

pip,
mutmut,
pytest,
xlrd,
xlsxwriter,
pandas,
codecov,
pytest-cov,
pylint

Installation
====================
[INSTALL.md](INSTALL.md) 

Usage & Configuration
====================
How to use the tool:
--------

From any editor which support Python (pref: pycharm, set cosine_source and text-de-duplication_monitoring as root by
right clicking and selecting option)

Make sure to set the right python interpreter and make sure it lists all the packages mentioned as mandate.

Option 1: UI
--------
Execute the cosine_ui.py, which will open the UI window where you need to enter the options like,

1. Path to the test/requirement/other other document to be analyzed.
2. Similarity to be processed (find out 100% match, 99% etc...)
3. Unique ID in the csv/xlsx column ID(0/1 etc...)
4. Steps/Description id for content matching (column of interest IDs in the csv/xlsx seperated by , like 1,2,3)
5. If new requirement / test to me checked with existing, enable the check box and paste the content to be checked in
the new text box.

Option 2: commandline
--------
C:\Projects\PythonRepo\text-de-duplication>python cosine_source\cosine_cmd.py --h
usage: cosine_cmd.py [-h] [--path --p] [--simindex --s] [--uniqid --u]
                     [--colint --c]

Text Similarity Index Processor

optional arguments:
  -h, --help      show this help message and exit
  --path --p      the Input file path
  --simindex --s  the Similarity index to be processed
  --uniqid --u    uniq id index(column) of the input file
  --colint --c    the col of interest
 


How to test the software
====================
1. To test the tool use : navigate to "text_de_duplication_monitoring" which is the root directory
2. issue pytest -v to run all the tests

- To report the pytest in html:
issue command pytest --html=report.html

- To run test for coverage:
pytest --cov-report html --cov="cosine_source"

- pydoc creation 
python -m pydoc -w module_name

- mutation testing using mutmut
mutmut --paths-to-mutate "path_to \ cosine_source" run

- pylint execution on code
pylint cosine_source test >"path_to_save_file\pylint.txt"

- jscpd execution on root folder
jscpd --min-tokens 20 --reporters "html" --mode "strict" --format "python" --output . .

Limitations
--------
1. Input is accepted only via xlsx
2. Stand alone application not web enabled
3. Users have to fetch the input to csv/xlsx
4. Tool is not yet plugged to TFS, ALM etc


Improvements/ Road-map
--------
1. Increase the test efficiency based on mutation testing output.
2. Make the tool web enabled (using python flask...).
3. Create hook to TFS, ALM etc so that this tool we can download the test/ requirement/ defects
and do further processing.
4. Enable the tool to do similarity check on code base.


Contact / Getting help
====================
[MAINTAINERS.md](MAINTAINERS.md) 

License
====================
[License.md](LICENSE.md) 