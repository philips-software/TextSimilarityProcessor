"""Koninklijke Philips N.V., 2019 - 2020. All rights reserved."""
import sys
import os
sys.path.append(os.path.abspath(os.path.join
                                (os.path.dirname(__file__), os.pardir
                                 )))# pragma: no mutate
from similarity.similarity_io import SimilarityIO
from similarity.similarity_cmd import create_parser

if __name__ == '__main__':
    # Execute the parse_args() method
    ARGS = create_parser(sys.argv[1:])
    # Process the similarity with inputs provided
    SIM_IO_OBJ = SimilarityIO(ARGS.path, ARGS.uniqid, ARGS.colint, ARGS.range,
                              ARGS.numrowcount, False, None, ARGS.filter)
    SIM_IO_OBJ.orchestrate_similarity()
