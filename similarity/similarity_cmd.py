"""Koninklijke Philips N.V., 2019 - 2020. All rights reserved.
File provides command line interface for the text similarity """

import argparse


def create_parser(args):
    """ Function which add the command line arguments required for the command line input
    of text similarity index processor"""
    # Create the parser
    cos_parser = argparse.ArgumentParser(description='Text Similarity')

    # Add the arguments
    cos_parser.add_argument("--path",
                            metavar="--p",
                            type=str,
                            help="Input file xlsx/csv  path")

    cos_parser.add_argument("--uniqid",
                            metavar="--u",
                            type=str,
                            help="Unique id index(column) of the input file [Example: --u 0]")

    cos_parser.add_argument("--colint",
                            metavar="--c",
                            type=str,
                            help='Columns of interest [Example: --c "1,2,3"]')

    cos_parser.add_argument("--numrowcount",
                            metavar="--n",
                            default=100,
                            type=int,
                            help='Number of rows for html brief report [Example: --n 500]')

    cos_parser.add_argument("--range",
                            metavar="--r",
                            default="60,100",
                            type=str,
                            help='Range of similarity of interest [Example: --r "70,100"]')

    cos_parser.add_argument("--filter",
                            metavar="--f",
                            default=500000,
                            type=int,
                            help='Filter for report file row split [Example: --f 500000]')

    # ...Create your parser as you like...
    return cos_parser.parse_args(args)
