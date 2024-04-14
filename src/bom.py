from typing import List

import bom_reader as reader
import bom_writer as writer

input_file = '/home/jamie/dev/bom/examples/partslist.txt'
output_file = '/home/jamie/dev/bom/output.txt'

def read_partlist_file(filepath: str) -> List[str]:
    with open(filepath, 'r') as file:
        content = file.readlines()
        # only remove newlines -- need to preserve tab whitespace for door definitions
        content = [l.replace('\n', '') for l in content]
        return content

def main():
    print(f'Reading file {input_file}')
    partlist = read_partlist_file(input_file)
    bill_of_materials = reader.read(partlist)
    print(bill_of_materials)
    print('\n')
    print(f'Writing file {output_file}')
    writer.write(bill_of_materials, output_file)

if __name__ == '__main__':
    main()
