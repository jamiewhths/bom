# Bill Of Materials Generator

Transforms an ArtiCad partlist file (txt) into a bill of materials ready for an order list.

## Usage

CLI Arguments:
- `input`: The input file path (absolute)
- `format`: The output file format (`csv` (default) or `txt`)

### Linux

`./bom {input} {format}`

### Windows

`bom.exe {input} {format}`

## Generating EXE file

`pyinstaller bom/bom.py -p /bom -F`
