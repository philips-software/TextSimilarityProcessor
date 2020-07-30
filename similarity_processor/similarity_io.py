"""Koninklijke Philips N.V., 2019 - 2020. All rights reserved.
This file process the IO for the Text similarity index processor """
import math
import os
import datetime
import shutil
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import similarity_processor.similarity_logging as cl

LOG = cl.get_logger()


def is_nan(value):
    """ Function which identifies the "nan" on empty cells """
    try:
        return math.isnan(float(value))
    except ValueError:
        return False


class SimilarityIO:
    """ This class is used for IO Processing the text similarity index processing tool.
    User input file is fetched here, also intermediate file as well as
    the final recommendation creating are tasks for this class """

    def __init__(self, file_path, uniq_id, col_int, num_html_row=10, is_new_text=False, new_text=None):
        """constructor for Similarity input output processor, which initializes the the input variables needed IO
        processing """
        LOG.info("\nSimilarity_UI \nValues passed:\n")  # pragma: no mutate
        self.file_path = file_path
        LOG.info("Path:%s", str(self.file_path))  # pragma: no mutate
        self.uniq_id = uniq_id
        LOG.info("\nUnique ID Column:%s", str(self.uniq_id))  # pragma: no mutate
        self.col_int = col_int
        LOG.info("\nColumns of Interest:%s", str(self.col_int))  # pragma: no mutate
        self.num_html_row = num_html_row
        LOG.info("\nnumber of html row:%s", str(self.num_html_row))  # pragma: no mutate
        self.is_new_text = is_new_text
        self.new_text = new_text
        LOG.info("\nNew_text:%s", str(self.new_text))  # pragma: no mutate
        self.data_frame = None
        self.uniq_header = None

    def __get_file_path(self):
        """ Function used for getting the file path where the results can be stored /
        from where input is provided"""
        if os.path.isfile(self.file_path):
            return str(os.path.dirname(self.file_path))
        return self.file_path

    def __get_file_name(self):
        """ Function used for getting the input file name which can be further used for naming
        the result """
        if os.path.isfile(self.file_path):
            file_path = self.file_path.split("/")
            return os.path.splitext(file_path[-1])[0]
        return "similarity"

    def __get_header(self):
        """ Function to fetch the header from the input file read in the dataframe """
        return list(self.data_frame.columns.values)

    def __set_uniq_header(self):
        """ Function to fetch the unique ID header """
        sheet_headers = self.__get_header()
        self.uniq_header = sheet_headers[int(self.uniq_id)]

    def __get_duplicate_id(self):
        """ Function which identifies if any duplicate ID present in the input file """
        # List the duplicate ID
        __duplicated_list = list(self.data_frame[self.uniq_header].duplicated())
        __du_list = []
        __data = [[]]
        # Remove the 'NaN' in case of empty cell and filter only IDs
        for key, item in enumerate(__duplicated_list):
            if item:
                __du_list.append(self.data_frame[self.uniq_header][key])
        du_list = list(map(lambda x: 0 if is_nan(x) else x, __du_list))
        __data = {"Duplicate ID": [nonzero for nonzero in du_list if nonzero != 0]}
        # Create DataFrame and write
        self.__write_xlsx(pd.DataFrame(__data), "Duplicate_ID")

    def __get_ip_file_type(self):
        file_type = self.file_path.split(".")[-1]
        return file_type.upper()

    def __read_to_panda_df(self):
        """ Function which read the input data/xlsx to a pandas Data frame """
        if not os.path.exists(self.file_path):
            LOG.error("\nFile path is invalid")  # pragma: no mutate
            return False
        function_dict = {
            "XLSX": lambda x: pd.read_excel(self.file_path),
            "CSV": lambda x: pd.read_csv(self.file_path)
        }

        self.data_frame = function_dict[self.__get_ip_file_type()](self.file_path)
        if self.data_frame.empty:
            LOG.error("\nInput data is incorrect/ file is invalid/"
                      "It has more than one sheet")  # pragma: no mutate
            return False
        return True

    def __get_needed_df_header(self, uniq_id_header, sheet_headers):
        """ Function to fetch only the Unique ID + column of interest as per user input """
        self.col_int = list(self.col_int.split(','))
        __column_of_interest_header = [sheet_headers[int(i)] for i in self.col_int]
        __all_col_int = ",".join(str(potion) for potion in __column_of_interest_header)
        return (uniq_id_header + "," + __all_col_int).split(",")

    def __refine_df(self):
        """ Create/Modify data frame with only needed contents as per user input """
        sheet_headers = self.__get_header()
        self.data_frame[sheet_headers[int(self.uniq_id)]] = self.data_frame[
            sheet_headers[int(self.uniq_id)]].ffill()
        self.data_frame = self.data_frame[self.__get_needed_df_header(
            sheet_headers[int(self.uniq_id)], sheet_headers)]

    def create_merged_df(self):
        """ Merge the text so as to form two column one with unique ID , other with merged
        content in steps """
        self.data_frame = (self.data_frame.set_index([self.uniq_header])
                           .apply(lambda x: " ".join(x.dropna()), axis=1)
                           .reset_index(name="Steps"))
        self.data_frame = self.data_frame.groupby(self.uniq_header)["Steps"] \
            .apply(' '.join).reset_index()

    def __create_mergrd_file(self):
        """ Create a copy of the merged content so that user can analyse """
        self.__write_xlsx(self.data_frame, "merged_steps")

    def __write_xlsx(self, data_f, name):
        """ Function which write the dataframe to xlsx """
        file_path = os.path.join(self.__get_file_path(), self.__get_file_name() + "_" + name)
        # Github open ticket for the abstract method
        writer = pd.ExcelWriter("%s.xlsx" % file_path, engine="xlsxwriter")
        data_f.to_excel(writer, sheet_name=name)
        writer.save()

    def __write_csv(self, data_f, name):
        """ Function which write the dataframe to xlsx """
        file_path = os.path.join(self.__get_file_path(), self.__get_file_name() + "_" + name)
        data_f.to_csv(file_path, header=True)

    def __new_text_df(self):
        """ Function which is created to form the new dataframe to include new text if
        entered in UI """
        __new_df = pd.DataFrame({self.uniq_header: ["New/ID_TBD"], "Steps": [self.new_text]})
        self.data_frame = __new_df.append(self.data_frame, ignore_index=True)

    @staticmethod
    def set_column_width(df_column):
        """
        Function to split the long line in the steps column
            df_column: data frame column value

        Returns: data frame column value after splitting

        """
        specifier_column = []
        spe_data = ""
        line_length = 200
        for i in range(len(df_column)):
            for line in str(df_column.iat[i, 0]).splitlines():
                if len(line) > line_length:
                    spe_data = spe_data + "\r\n".join(line[i:i + line_length] for i in range(0, len(line), line_length))
                else:
                    spe_data = spe_data + line + "\r\n"
            specifier_column.append(spe_data)
            spe_data = ""
        return specifier_column

    def __write_html(self, html_data_frame):
        """ Function which is used to report out the top similarity match defaulted to 10 rows """
        html_file_path = os.path.join(self.__get_file_path(), self.__get_file_name() + "_" + "brief_report.html")
        html_data_frame['UNIQ ID'] = html_data_frame['UNIQ ID'].apply(str).str.wrap(80)
        html_data_frame['POTENTIAL MATCH'] = html_data_frame['POTENTIAL MATCH'].apply(str).str.wrap(80)
        html_data_frame.sort_values('SIMILARITY', ascending=False, inplace=True)
        pd.set_option('colheader_justify', 'center')
        html_string = '''
        <html>
          <head><title>HTML Pandas Dataframe with CSS</title></head>
          <link rel="stylesheet" type="text/css" href="df_style.css"/>
          <h1 style="font-size:50px;">Brief Report on Similarity Analysis</h1>
          <h2 style="font-size:20px;font-style:italic;">Note: This is a brief report. For details 
          please refer 'csv/xlsx' in same folder</h2>
          <body>
            {table}
          </body>
        </html>
        '''
        with open(html_file_path, 'w') as html_file:

            html_file.write(html_string.format(table=html_data_frame.to_html(classes='mystyle')).
                            replace(r'\r\n', "<br>").replace(r'\n', "<br>").replace(r'\r', "<br>"))
        shutil.copy(os.path.join(os.path.dirname(__file__), "df_style.css"), os.path.join(self.__get_file_path(),
                                                                                          "df_style.css"))

    def report_brief_html(self, data_similarity):
        """ Function which report the highest similarity match in html output based on input argument (defaulted to
        10 rows #no """
        brief_report = data_similarity.sort_values('SIMILARITY', ascending=False).iloc[:int(self.num_html_row)]
        html_df = self.data_frame.rename(columns={self.uniq_header: 'UNIQ ID', "Steps": "Steps"})
        html_df['Steps'] = self.set_column_width(html_df[['Steps']])
        temp_data_frame1 = (pd.merge(html_df.drop(['Potential Match'], axis=1), brief_report, on=['UNIQ ID'],
                                     how='inner'))
        html_df.rename(columns={'UNIQ ID': 'POTENTIAL MATCH', "Steps": "Steps"}, inplace=True)
        temp_data_frame2 = ((pd.merge(html_df.drop(['Potential Match'], axis=1), temp_data_frame1,
                                      on=['POTENTIAL MATCH'],
                                      how='inner')))
        self.__write_html(temp_data_frame2)

    def process_cos_match(self):
        """ Function which process the data frame for matching/finding similarity index """
        count_vect = CountVectorizer()
        word_count_vector = count_vect.fit_transform(self.data_frame["Steps"].to_numpy())
        c_sim = 100 * (cosine_similarity(word_count_vector))
        self.data_frame["Potential Match"] = self.data_frame[self.uniq_header]
        dataframe = pd.DataFrame(c_sim, columns=self.data_frame["Potential Match"],
                                 index=self.data_frame[self.uniq_header])
        row, col = dataframe.shape
        dataframe[:] = np.where(np.arange(row)[:, None] >= np.arange(col), np.nan, dataframe)
        report_df = dataframe.stack().reset_index()
        report_df.columns = ["UNIQ ID", "POTENTIAL MATCH", "SIMILARITY"]
        return report_df

    def __validate_input(self):
        """ Function to validate the input parameters """
        __ret_val = True
        try:
            rows, columns = self.data_frame.shape
            LOG.info("\n#Row:%s #Col:%s" % (str(rows), str(columns)))  # pragma: no mutate
            input_list = self.col_int.split(',')
            test_list = [int(i) for i in input_list]
            test_list.append(int(self.uniq_id))
            list_check = list(map(lambda item: True if item <= columns - 1 else False, test_list))
            if False in list_check:
                __ret_val = False
                LOG.error("\nEither or both unique id and col of interest out of range")  # pragma: no mutate
            return __ret_val
        except ValueError:
            LOG.error("\nInput data is not an integer")  # pragma: no mutate
            return False

    def orchestrate_similarity(self):
        """Function which orchestrate the entire sequence of cosine similarity matching
        from IO layer"""
        start = datetime.datetime.now().timestamp()
        if self.__read_to_panda_df() and self.__validate_input():
            self.__set_uniq_header()
            self.__get_duplicate_id()
            self.__refine_df()
            self.create_merged_df()
            if self.is_new_text == 1:
                self.__new_text_df()
            self.__create_mergrd_file()
            report_df = self.process_cos_match()
            self.__write_csv(report_df, "recommendation.csv")
            self.report_brief_html(report_df)
        end = datetime.datetime.now().timestamp()
        print("Execution time %s" % (end - start))  # pragma: no mutate
