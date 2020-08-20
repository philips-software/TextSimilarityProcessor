# Text Similarity

![Python application](https://github.com/philips-software/TextSimilarityProcessor/workflows/Python%20application/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![codecov](https://codecov.io/gh/philips-software/TextSimilarityProcessor/branch/master/graph/badge.svg)](https://codecov.io/gh/philips-software/TextSimilarityProcessor)

Tool to identify the similarity of the input text

It can be used to identify the similarity of,

- Tests  

- Code  

- Requirements  

- Defects  

Advantage of using such similarity analysis are,

- Resolving technical debt  

- Grouping together similar code / tests / requirements / defects etc.  
  
## Dependencies

- python 3.8 : 64 bit  

- python packages (xlrd, xlsxwriter, pandas, scikit-learn, numpy)  

## Installation
  
[INSTALL.md](INSTALL.md)

```sh
pip install similarity-processor
```

## Usage

### UI

```sh
>>>python -m similarity.similarity_ui
```

- Path to the test/requirement/other other document to be
 analyzed(xlsx / csv format).  

- Unique ID in the csv/xlsx column ID(0/1 etc...)  

- Steps/Description id for content matching (column of interest IDs
 in the csv/xlsx separated by , like 1,2,3)  

- If new requirement / test to me checked with existing, enable the
 check box and paste the content to be checked in the new text box.  

### Commandline

```sh
>>>python -m similarity --p "path\to\TestBank.xlsx" --u 0 --c "1,2,3" --n 8
```

- Help option can be found at,  

```sh
>>>python -m similarity --h
```

### Code

```sh
>>> from similarity.similarity_io import SimilarityIO
>>> similarity_io_obj = SimilarityIO("path\to\TestBank.xlsx", 0, "1,2,3")
>>> similarity_io_obj.orchestrate_similarity()
```

### Arguments

Mandatory

- Path to the input file
- Unique id value column id in xlsx  
- Interested columns in xlsx  

Optional

- Upper and lower range to filter the similarity values in the output
   (defaulted "60,100")
- Number of rows in the html report, defaulted to 100  
- Are you checking a new text against a existing text bank?
- If yes: new text
- Filter value to split the report xlsx file, defaulted to 500000,
   500001 onward row will be moved to new file

```sh
import pandas as pd
from similarity.similarity_io import SimilarityIO

demo_df = pd.read_excel(r"input\xlsx\sheet\name")  # You could read from any input source

similarity_io_obj = SimilarityIO(None, None, None)  # (None, None, None, 200) =>200 = The brief html report rows
 default is 10  
similarity_io_obj.file_path = r"path\to\report\folder" #when used in this format, else input file path to read data
similarity_io_obj.data_frame = demo_df # input data frame
similarity_io_obj.uniq_header = "Uniq ID"  # Unique header of the input data frame (string)
similarity_io_obj.create_merged_df()
processed_similarity = similarity_io_obj.process_cos_match()
similarity_io_obj.report_brief_html(processed_similarity)
processed_similarity.to_csv(r"path\to\report\folder\report.csv", header=True)
```

### Output
  
- Output will be available in same folder as input file or  `file_path`
 specified  

- If any duplicate ids in the unique id file with name string containing
 'duplicate id'  

- A recommendation file with similarity values  

- A merged file with data in the "interested columns in xlsx"  

- An html brief report containing the top 10 similarities
 (100 is default value which can be changed by --n option)  

## Contact

[MAINTAINERS.md](MAINTAINERS.md)  

## License

[License.md](LICENSE.md)
