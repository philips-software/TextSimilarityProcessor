"""Koninklijke Philips N.V., 2019 - 2020. All rights reserved.
File provides command line interface for the text similarity """
import os
import sys
import argparse
sys.path.append(os.path.abspath(os.path.join
                                (os.path.dirname(__file__), os.pardir
                                 )))# pragma: no mutate
from similarity_processor.similarity_io import SimilarityIO


def create_parser(args):
    """ Function which add the command line arguments required for the command line input
    of text similarity index processor"""
    # Create the parser
    cos_parser = argparse.ArgumentParser(description='Text Similarity')

    # Add the arguments
    cos_parser.add_argument("--path",
                            metavar="--p",
                            type=str,
                            help="Input file path")

    cos_parser.add_argument("--uniqid",
                            metavar="--u",
                            type=str,
                            help="Unique id index(column) of the input file")

    cos_parser.add_argument("--colint",
                            metavar="--c",
                            type=str,
                            help="Columns of interest")

    cos_parser.add_argument("--numrowcount",
                            metavar="--n",
                            default=100,
                            type=int,
                            help="Number of rows for html brief report")

    cos_parser.add_argument("--range",
                            metavar="--r",
                            default="60,100",
                            type=str,
                            help="Range of similarity of interest")

    cos_parser.add_argument("--filter",
                            metavar="--f",
                            default=500000,
                            type=int,
                            help="Filter for report file row split")

    # ...Create your parser as you like...
    return cos_parser.parse_args(args)


if __name__ == '__main__':
    # Execute the parse_args() method
    ARGS = create_parser(sys.argv[1:])
    # Process the similarity with inputs provided
    SIM_IO_OBJ = SimilarityIO(ARGS.path, ARGS.uniqid, ARGS.colint, ARGS.range, ARGS.numrowcount, False, None, ARGS.filter)
    SIM_IO_OBJ.orchestrate_similarity()
