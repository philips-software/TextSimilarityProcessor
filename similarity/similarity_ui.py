"""Koninklijke Philips N.V., 2019 - 2020. All rights reserved.
This file holds the UI implementation for the Text similarity processing """
# noinspection PyCompatibility
from tkinter import Tk
from tkinter import IntVar, END
from tkinter import Label, Entry, Button, Checkbutton
from tkinter import filedialog
from similarity.similarity_io import SimilarityIO
import similarity.similarity_logging as cl

ROW_SPACER = 25
LOG = cl.get_logger()


class TextSimilarityWindow:
    """ This class is used for creating the minimalistic UI for the Text similarity index processor
    which is used to find the similarity index (100%, 99% matching text etc...)
    between text say, requirements, Tests... """
    i = ROW_SPACER

    def __init__(self, win):
        """constructor for text Similarity Window, which initializes
        the input variables needed to fetch from user """
        self.filename = None
        self.new_text = None
        self.is_new_text = IntVar()
        self.browsebutton = Button(win, text="Browse", command=self.__browse_func)
        self.browsebutton.place(x=450, y=ROW_SPACER)

        def __place_ui_item(text, val, width=10):
            """ Function used to place the UI elements to respective place in the UI """
            _id = Label(win, text=text)
            _id.place(x=10, y=ROW_SPACER * val)
            _text_in = Entry(win, width=width)
            _text_in.place(x=200, y=ROW_SPACER * val)
            _text_in.delete(0, END)
            return _id, _text_in

        self.path, self.path_t = __place_ui_item("Input File Path", 1, 30)
        self.uniq_id, self.uniq_id_t = __place_ui_item("Unique ID Column", 2)
        self.steps_id, self.steps_t = __place_ui_item("Columns Of Interest", 3)
        self.range_id, self.range_t = __place_ui_item("similarity range", 4)

        def __new_text_compare():
            """ Function used to create the place holder for the User input used
            for the new text to be compared """
            if self.is_new_text.get() == 1:
                self.new_text = Entry(win, width=10)
                self.new_text.place(x=250, y=ROW_SPACER * 6, width=340, height=50)
            else:
                self.new_text.destroy()

        self.check_is_new_text = Checkbutton(win, text="New Text Comparison",
                                             variable=self.is_new_text,
                                             command=__new_text_compare)
        self.check_is_new_text.place(x=50, y=ROW_SPACER * 6)
        self.submit = Button(win, text="Process", command=self.process)
        self.submit.place(x=250, y=ROW_SPACER * 9)

    def __browse_func(self):
        """ Function used for providing the Browse to file path in the GUI """
        try:
            self.filename = filedialog.askopenfilename()
            self.path_t.delete(0, END)
            self.path_t.insert(0, str(self.filename))
        except TypeError as error:
            print("Exception at browse_func method:", str(error)) # pragma: no mutate
            LOG.error("Error:%s", str(error)) # pragma: no mutate

    def __get_new_text(self):
        """ Function used to get the user input text in case of new text
        for similarity checking, else to return None """
        return str(self.new_text.get()) if self.is_new_text.get() == 1 else None

    def process(self):
        """ Function which is the entry for all the processing activity."""
        try:
            similarity_io_obj = SimilarityIO(self.path_t.get(),
                                             self.uniq_id_t.get(), self.steps_t.get(), self.range_t.get(),
                                             100, self.is_new_text.get(), self.__get_new_text(), 500000)
            similarity_io_obj.orchestrate_similarity()
        except TypeError as error:
            print("Error:", str(error)) # pragma: no mutate
            LOG.error("Error:%s", str(error)) # pragma: no mutate


if __name__ == '__main__':
    WINDOW = Tk()
    MY_WIN = TextSimilarityWindow(WINDOW)
    WINDOW.title("Text Similarity")
    WINDOW.geometry("550x250+10+10")
    WINDOW.mainloop()
