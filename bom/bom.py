import argparse
import datetime
from typing import List

from bom import bom_txt_reader as reader, bom_txt_writer as txt_writer, bom_csv_writer as csv_writer

DESCRIPTION = "Transforms an ArtiCad partlist file (txt) into a bill of materials ready for an order list."
INPUT_ARG_DESCRIPTION = 'ArtiCad partlist file (txt)'
FORMAT_ARG_DESCRIPTION = 'Output file format ("csv", "txt")'
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
    parser.add_argument('format', type=str, default='csv', help=FORMAT_ARG_DESCRIPTION)
    return parser.parse_args()

def main(input_file: str, output_format: str):
    print(f'Reading file {input_file}')
    partlist = read_partlist_file(input_file)
    bill_of_materials = reader.read(partlist)
    output_filename = f'bom_output__{datetime.datetime.now().strftime("%Y_%m_%dT%H_%M_%S")}.{output_format}'
    print(f'Writing file {output_filename}')
    if output_format == 'txt':
        txt_writer.write(bill_of_materials, output_filename)
    elif output_format == 'csv':
        csv_writer.write(bill_of_materials, output_filename)
    else:
        print('!!! Unknown output format specified')

if __name__ == '__main__':
    args = _parse_args()
    main(args.input, args.format)
