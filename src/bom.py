import argparse
import datetime
from typing import List

import bom_reader as reader
import bom_writer as writer

DESCRIPTION = "Transforms an ArtiCad partlist file (txt) into a bill of materials ready for an order list."
INPUT_ARG_DESCRIPTION = 'ArtiCad partlist file (txt)'
VERSION = 'v1.0.0'

def read_partlist_file(filepath: str) -> List[str]:
    with open(filepath, 'r') as file:
        content = file.readlines()
        # only remove newlines -- need to preserve tab whitespace for door definitions
        content = [l.replace('\n', '') for l in content]
        return content

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('input', type=str, help=INPUT_ARG_DESCRIPTION)
    return parser.parse_args()

def main(input_file: str):
    print(f'Reading file {input_file}')
    partlist = read_partlist_file(input_file)
    bill_of_materials = reader.read(partlist)
    output_filename = f'bom_output_{datetime.datetime.now()}'
    print(f'Writing file {output_filename}')
    writer.write(bill_of_materials, output_filename)

if __name__ == '__main__':
    args = _parse_args()
    main(args.input)
