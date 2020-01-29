""" This file process the IO for the Text similarity index processor """
import math
import os
import pandas as pd
from cosine_source.cosine_core import get_cosine
from cosine_source.cosine_core import text_to_vector
from cosine_source.cosine_core import check_tolerance
import cosine_source.cosine_logging as cl
LOG = cl.get_logger()


def is_nan(value):
    """ Function which identifies the "nan" on empty cells """
    try:
        return math.isnan(float(value))
    except ValueError:
        return False


class CosineIO:
    """ This class is used for IO Processing the text similarity index processing tool.
    User input file is fetched here, also intermediate file as well as
    the final recommendation creating are tasks for this class """

    def __init__(self, file_path, sim_match, uniq_id, col_int, is_new_text, new_text=None):
        """constructor for cosineIO, which initializes the the input variables needed IO
        processing """
        LOG.info("\nCosine_UI \nValues passed:\n")
        self.file_path = file_path
        LOG.info("Path:%s", str(self.file_path))
        self.sim_match = sim_match
        LOG.info("\nSimilarity Index:%s", str(self.sim_match))
        self.uniq_id = uniq_id
        LOG.info("\nUnique ID Column:%s", str(self.uniq_id))
        self.col_int = col_int
        LOG.info("\nColumns of Interest:%s", str(self.col_int))
        self.is_new_text = is_new_text
        self.new_text = new_text
        LOG.info("\nNew_text:%s", str(self.new_text))
        self.data_frame = None
        self.uniq_header = None

    def __get_file_path(self):
        """ Function used for getting the file path where the results can be stored /
        from where input is provided"""
        return str(os.path.dirname(self.file_path))

    def __get_file_name(self):
        """ Function used for getting the input file name which can be further used for naming
        the result """
        file_path = self.file_path.split("/")
        return os.path.splitext(file_path[-1])[0]

    def __get_header(self):
        """ Function to fetch the header from the inputfile read in the dataframe """
        return list(self.data_frame.columns.values)

    def __set_uniq_header(self):
        """ Function to fetch the unique ID header """
        sheet_headers = self.__get_header()
        self.uniq_header = sheet_headers[int(self.uniq_id)]

    def __get_duplicate_id(self):
        """ Function which identifies if any duplicate ID present in the input file """
        # List the duplicate ID
        __duplicated_list = list(self.data_frame.duplicated())
        __du_list = []
        __data = [[]]
        # Remove the 'NaN' in case of empty cell and filter only IDs
        for key, item in enumerate(__duplicated_list):
            if item:
                __du_list.append(self.data_frame[self.uniq_header][key])
        du_list = list(map(lambda x: 0 if is_nan(x) else x, __du_list))
        __data = {'Duplicate ID': [nonzero for nonzero in du_list if nonzero != 0]}
        # Create DataFrame and write
        self.__write_xlsx(pd.DataFrame(__data), "Duplicate_ID")

    def __read_to_panda_df(self):
        """ Function which read the input data/xlsx to a pandas Data frame """
        if not os.path.exists(self.file_path):
            LOG.error("\nFile path is invalid")
            return False
        self.data_frame = pd.read_excel(self.file_path)
        if self.data_frame.empty:
            LOG.error("\nInput data is incorrect/ file is invalid/"
                      "It has more than one sheet")
            return False
        return True

    def __get_needed_df_header(self, uniq_id_header, sheet_headers):
        """ Function to fetch only the Uniq ID + column of interest as per user input """
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

    def __create_merged_df(self):
        """ Merge the text so as to form two column one with unique ID , other with merged
        content in steps """
        self.data_frame = (self.data_frame.set_index([self.uniq_header])
                           .apply(lambda x: ' '.join(x.dropna()), axis=1)
                           .reset_index(name='Steps'))
        self.data_frame = self.data_frame.groupby(self.uniq_header)['Steps']\
            .apply(' '.join).reset_index()

    def __create_mergrd_file(self):
        """ Create a copy of the merged content so that user can analyse """
        self.__write_xlsx(self.data_frame, "merged_steps")

    def __write_xlsx(self, data_f, name):
        """ Function which write the dataframe to xlsx """
        file_path = os.path.join(self.__get_file_path(), self.__get_file_name() + "_" + name)
        # Github open ticket for the abstract method
        writer = pd.ExcelWriter('%s.xlsx' % file_path, engine='xlsxwriter')
        data_f.to_excel(writer, sheet_name=name)
        writer.save()

    def __new_text_df(self):
        """ Function which is created to form the new dataframe to include new text if
        entered in UI """
        __new_df = pd.DataFrame({self.uniq_header: ["New/ID_TBD"], 'Steps': [self.new_text]})
        self.data_frame = __new_df.append(self.data_frame, ignore_index=True)

    def __process_cos_match(self):
        """ Function which process the dataframe for matching/finding similarity index """
        # list to store the analysis
        __reco = []
        # Loop through the set of rows in the dataframe
        for master_text_index in self.data_frame.index:
            __uniq_id = self.data_frame[self.uniq_header][master_text_index]
            master_text = self.data_frame['Steps'][master_text_index]
            vector1 = text_to_vector(str(master_text))
            # Loop through the rows immediate next from the initially selected in previous loop
            for match_text_index in range(master_text_index + 1, len(self.data_frame.index)):
                match_id = self.data_frame[self.uniq_header][match_text_index]
                match_text = self.data_frame['Steps'][match_text_index]
                vector2 = text_to_vector(str(match_text))
                # Generate the cosine similarity match value
                cosine = get_cosine(vector1, vector2)
                if check_tolerance(cosine * 100, int(self.sim_match)):
                    print(cosine * 100)
                    __reco.append({self.uniq_header: str(__uniq_id), 'Potential Match':
                                   str(match_id), 'Similarity Index': str(cosine * 100)})
            if self.is_new_text == 1:
                break
        # Create dataframe and write
        self.__write_xlsx(pd.DataFrame(__reco), "%s_recomendation" % self.sim_match)

    def __validate_input(self):
        """ Function to validate the input parameters """
        __ret_val = True
        try:
            if int(self.sim_match) > 100 or int(self.sim_match) < 1:
                __ret_val = False
                LOG.error("\nSimilarity index is not less than 100")
            rows, columns = self.data_frame.shape
            LOG.info("\n#Row:%s #Col:%s" % (str(rows), str(columns)))
            input_list = self.col_int.split(',')
            test_list = [int(i) for i in input_list]
            test_list.append(int(self.uniq_id))
            list_check = list(map(lambda item: True if item <= columns-1 else False, test_list))
            if False in list_check:
                __ret_val = False
                LOG.error("\nEither or both unique id and col of interest out of range")
            return __ret_val
        except ValueError:
            LOG.error("\nInput data is not an integer")
            return False

    def orchestrate_cosine(self):
        """Function which orchestrate the entire sequence of cosine similarity matching
        from IO layer"""

        if self.__read_to_panda_df() and self.__validate_input():
            self.__set_uniq_header()
            self.__get_duplicate_id()
            self.__refine_df()
            self.__create_merged_df()
            if self.is_new_text == 1:
                self.__new_text_df()
            self.__create_mergrd_file()
            self.__process_cos_match()
