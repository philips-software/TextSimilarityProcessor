[![Build Status](https://travis-ci.com/philips-software/TextSimilarityProcessor.svg?branch=master)](https://travis-ci.com/philips-software/TextSimilarityProcessor)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![codecov](https://codecov.io/gh/philips-software/TextSimilarityProcessor/branch/master/graph/badge.svg)](https://codecov.io/gh/philips-software/TextSimilarityProcessor)


Text Similarity Index processor
====================
What is the project intented to solve?
--------
Resolving the Technical Debt in "Test/Requirement/Issues/Any-text" repos with unique id using Natural Language Processing Continuous 
duplicate monitoring system in place to check the duplication of any new text added to "Test/Requirement/Issues/Any-text" bank. 
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
1. How to use the tool from the source code:
--------

From any editor which support Python (pref: pycharm, set similarity_processor and text-de-duplication_monitoring as root by
right clicking and selecting option)

Make sure to set the right python interpreter and make sure it lists all the packages mentioned as mandate.

Option 1: UI
--------
Execute the `similarity_ui.py`, which will open the UI window where you need to enter the options like,

1. Path to the test/requirement/other other document to be analyzed.
2. Similarity to be processed (find out 100% match, 99% etc...)
3. Unique ID in the csv/xlsx column ID(0/1 etc...)
4. Steps/Description id for content matching (column of interest IDs in the csv/xlsx seperated by , like 1,2,3)
5. If new requirement / test to me checked with existing, enable the check box and paste the content to be checked in
the new text box.

Option 2: commandline
--------
```
$ python similarity_processor\similarity_cmd.py --h
usage: similarity_cmd.py [-h] [--path --p] [--simindex --s] [--uniqid --u]
                     [--colint --c]

Text Similarity Index Processor

optional arguments:
  -h, --help      show this help message and exit
  --path --p      the Input file path
  --simindex --s  the Similarity index to be processed
  --uniqid --u    uniq id index(column) of the input file
  --colint --c    the col of interest
``` 


2. How to use the tool after "pip install similarity-processor"
-----------------------------------------------------------

Option 1: To use only the similarity 
------------------------------------
```
>>> from similarity_processor import similarity_core

>>> x = similarity_core.text_to_vector("this is a sample test")
>>> y = similarity_core.text_to_vector("this is a sample")
>>> w = similarity_core.get_cosine(x,y)
>>> print(w)
0.8944271909999159
```
Option 2: Generate similarity for a group of text
like "Test cases, requirement etc... which is present in xlsx
-------------------------------------------------------------
```
>>> from similarity_processor.similarity_io import SimilarityIO

>>> similarity_io_obj = SimilarityIO("TestBank.xlsx", "99", 0, "1,2,3", 0, None)
>>> similarity_io_obj.orchestrate_similarity()
```
Arguments:Path to the input file, Similarity index of interest, Unique id value column id in xlsx, Interested columns in xlsx, Are you checking a new text against a existing text bank ?, If yes: new text

Output will be available in same folder as input file

files are,
1. If any duplicate ids in the unique id
2. A recomendation for the similarity value input
3. a metged file with datas in the "interested columns in xlsx"

Option 3: Generate similarity for a group of text
like "Test cases, requirement etc... which is present in xlsx
through commandline
-------------------------------------------------------------
```
>python -m similarity_processor.similarity_cmd --h
>python -m similarity_processor.similarity_cmd --p "TestBank.xlsx" --s "99" --u 0 --c "1,2,3"
```

Option 4: Generate similarity for a group of text
like "Test cases, requirement etc... which is present in xlsx
through UI
-------------------------------------------------------------
```
>python -m similarity_processor.similarity_ui
```
1. Path to the test/requirement/other other document to be analyzed.
2. Similarity to be processed (find out 100% match, 99% etc...)
3. Unique ID in the csv/xlsx column ID(0/1 etc...)
4. Steps/Description id for content matching (column of interest IDs in the csv/xlsx seperated by , like 1,2,3)
5. If new requirement / test to me checked with existing, enable the check box and paste the content to be checked in
the new text box.

How to test the software
====================
1. To test the tool use : navigate to "text_de_duplication_monitoring" which is the root directory
2. issue `pytest -v` to run all the tests

- To report the pytest in html:
issue command `pytest --html=report.html`

- To run test for coverage:
`pytest --cov-report html --cov="similarity_processor"`

- pydoc creation 
`python -m pydoc -w module_name`

- mutation testing using mutmut
`mutmut --paths-to-mutate "path_to \ similarity_processor" run`

- pylint execution on code
`pylint similarity_processor test >"path_to_save_file\pylint.txt"`

- jscpd execution on root folder
`jscpd --min-tokens 20 --reporters "html" --mode "strict" --format "python" --output . .`

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
