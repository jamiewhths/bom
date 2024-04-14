import itertools as it
from typing import List, Optional

import models as m

UNIT = 'mm'
TAB = '    '
COUNT_SPLIT = 'X'
MEAS_DIM_SPLIT = 'by'
DEPTH_STR_PREFIX = 'Depth = '
HEIGHT_STR_PREFIX = 'Height = '

def _is_group_label(line: str) -> bool:
    if line.startswith(TAB):
        return False
    if line[0].isnumeric():
        return False
    return True

def _group_lines(partlist: List[str]) -> List[List[str]]:
   '''Splits a partlist into groups, using empty lines as divisions between groups'''
   return [list(g) for k, g in it.groupby(partlist, key=bool) if k]

def _extract_group_label(grouped_lines: List[str]) -> str:
    label = None
    for l in grouped_lines:
        if _is_group_label(l):
            return l
    if label is None:
        print(f'No group label defined in lines: {grouped_lines}')
        return ''

def _is_unit(line: str) -> bool:
    if line is None or line == '':
        return False
    if line.startswith(TAB):
        return False
    return line[0].isnumeric()    

def _is_door(line: str) -> bool:
    return line.startswith(TAB)

def _extract_unit_id(line: str) -> int:
    line_components = line.split('.')
    id_str = line_components[0]
    return int(id_str)

def _extract_unit_description(line: str):
    # expected format: `{id}. {width}{unit} {text description}, Depth = {depth}{unit}, Height = {height}{unit}`
    line_components = line.split('.')
    definition_str = line_components[1].strip()
    definition_compenents = definition_str.split(', ')
    width_decription_components = definition_compenents[0].split(f'{UNIT} ')
    description_str = width_decription_components[1]
    return description_str

def _extract_unit_width(line: str) -> int:
    # expected format: `{id}. {width}{unit} {text description}, Depth = {depth}{unit}, Height = {height}{unit}`
    line_components = line.split('. ')
    definition_str = line_components[1].strip()
    definition_compenents = definition_str.split(', ')
    width_decription_components = definition_compenents[0].split(f'{UNIT} ')
    width_str = width_decription_components[0]  # WITHOUT UNIT
    return int(width_str)

def _extract_unit_depth(line: str) -> int:
    # expected format: `{id}. {width}{unit} {text description}, Depth = {depth}{unit}, Height = {height}{unit}`
    line_components = line.split('. ')
    definition_str = line_components[1].strip()
    definition_compenents = definition_str.split(', ')
    depth_str = definition_compenents[1]  # WITH UNIT
    return int(depth_str.replace(DEPTH_STR_PREFIX, '').replace(UNIT, ''))

def _extract_unit_height(line: str) -> Optional[int]:
    # expected format: `{id}. {width}{unit} {text description}, Depth = {depth}{unit}, Height = {height}{unit}`
    # NOT ALWAYS DEFINED
    line_components = line.split('. ')
    definition_str = line_components[1].strip()
    definition_compenents = definition_str.split(', ')
    if len(definition_compenents) <= 2:
        return None
    height_str = definition_compenents[2]  # WITH UNIT
    return int(height_str.replace(HEIGHT_STR_PREFIX, '').replace(UNIT, ''))

def _parse_unit(line: str) -> m.Unit:
    # expected format: `{id}. {width}{unit} {text description}, Depth = {depth}{unit}, Height = {height}{unit}`
    # example: `1000mm Tall Open Fridge(American)Housing with Top Cupboard, Depth = 600mm, Height = 2300mm`
    print(f'Parsing line for unit: {line}')
    id = _extract_unit_id(line)
    description = _extract_unit_description(line)
    height = _extract_unit_height(line)
    width = _extract_unit_width(line)
    depth = _extract_unit_depth(line)
    return m.Unit(id=id, description=description, height=height, width=width, depth=depth)

def _extract_door_count(line: str) -> int:
    # expected format: `    {count} X {width}{unit} by {height}{unit} {text_description}`
    stripped_line = line.strip()
    count_definition_components = stripped_line.split(f' {COUNT_SPLIT} ')
    count_str = count_definition_components[0]
    return int(count_str)

def _extract_door_description(line: str) -> int:
    # expected format: `    {count} X {width}{unit} by {height}{unit} {text_description}`
    stripped_line = line.strip()
    count_definition_components = stripped_line.split(f' {COUNT_SPLIT} ')
    definition_str = count_definition_components[1]
    measurement_description_components = definition_str.split(f' {MEAS_DIM_SPLIT} ')
    height_description_str = measurement_description_components[1]
    height_description_components = height_description_str.split(f'{UNIT} ')
    description_str = height_description_components[1]
    return description_str

def _extract_door_height(line: str) -> int:
    # expected format: `    {count} X {width}{unit} by {height}{unit} {text_description}`
    stripped_line = line.strip()
    count_definition_components = stripped_line.split(f' {COUNT_SPLIT} ')
    definition_str = count_definition_components[1]
    measurement_description_components = definition_str.split(f' {MEAS_DIM_SPLIT} ')
    height_description_str = measurement_description_components[1]
    height_description_components = height_description_str.split(f'{UNIT} ')
    height_str = height_description_components[0]  # WITHOUT UNIT
    return int(height_str)

def _extract_door_width(line: str) -> int:
    # expected format: `    {count} X {width}{unit} by {height}{unit} {text_description}`
    stripped_line = line.strip()
    count_definition_components = stripped_line.split(f' {COUNT_SPLIT} ')
    definition_str = count_definition_components[1]
    measurement_description_components = definition_str.split(f' {MEAS_DIM_SPLIT} ')
    width_str = measurement_description_components[0]  # WITH UNIT
    return int(width_str.replace(UNIT, ''))

def _parse_door(unit_id: int, line: str) -> m.Door:
    # expected format: `    {count} X {width}{unit} by {height}{unit} {text_description}`
    # example: `1 X 496mm by 495mm Wall Unit Door LHH`
    print(f'Parsing line for door: {line}')
    count = _extract_door_count(line)
    description = _extract_door_description(line)
    height = _extract_door_height(line)
    width = _extract_door_width(line)
    return m.Door(unit_id=unit_id, count=count, description=description, height=height, width=width)

def _parse_units(grouped_lines: List[str]) -> List[m.Unit]:
    units: List[m.Unit] = []
    current_unit = None
    for l in grouped_lines:
        if _is_group_label(l):
            continue
        if _is_unit(l):
            if current_unit is not None:
                units.append(current_unit)
            current_unit = _parse_unit(l)
        elif _is_door(l):
            door = _parse_door(current_unit.id, l)
            current_unit.doors.append(door)
        else:
            print(f'!!! UNKNOWN: {l}')
    return units

def _parse_group(grouped_lines: List[str]) -> m.Group:
    label = _extract_group_label(grouped_lines)
    units = _parse_units(grouped_lines)
    return m.Group(label, units)

def read(partlist: List[str]) -> m.BillOfMaterials:
    bom = m.BillOfMaterials()
    grouped_lines = _group_lines(partlist)
    print(grouped_lines)
    groups: List[m.Group] = [_parse_group(g) for g in grouped_lines]
    bom.groups.extend(groups)
    return bom
