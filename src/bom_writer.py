from typing import List

import models as m

CARCASS_HEADER = 'Carcasses'
DOORS_HEADER = 'Doors'
OTHER_HEADER = 'Other'

COUNT_SPLIT = 'X'
MEAS_DIM_SPLIT = 'x'
NEWLINE = '\n'

def _extract_caracasses(bom: m.BillOfMaterials) -> List[m.Unit]:
    units = []
    for group in bom.groups:
        for unit in group.units:
            if not unit.is_carcass():
                continue
            units.append(unit)
    return units

def _extract_doors(bom: m.BillOfMaterials) -> List[m.Unit]:
    doors = []
    for group in bom.groups:
        for unit in group.units:
            if not unit.is_carcass():
                continue
            for door in unit.doors:
                doors.append(door)
    return doors

def _extract_standalone(bom: m.BillOfMaterials) -> List[m.Unit]:
    units = []
    for group in bom.groups:
        for unit in group.units:
            if unit.is_carcass():
                continue
            units.append(unit)
    return units

def _write_carcasses(bom: m.BillOfMaterials, file):
    carcasses = _extract_caracasses(bom)

    file.write(CARCASS_HEADER)
    file.write(NEWLINE)

    for c in carcasses:
        file.write(f'{c.id}: {c.description} ({c.height} {MEAS_DIM_SPLIT} {c.width} {MEAS_DIM_SPLIT} {c.depth})')
        file.write(NEWLINE)

    file.write(NEWLINE)

def _write_doors(bom: m.BillOfMaterials, file):
    doors = _extract_doors(bom)

    file.write(DOORS_HEADER)
    file.write(NEWLINE)

    for d in doors:
        file.write(f'{d.count} {COUNT_SPLIT} {d.height} {MEAS_DIM_SPLIT} {d.width} ({d.id}) ({d.description})')
        file.write(NEWLINE)

    file.write(NEWLINE)

def _standlone_dims(standalone: m.Unit) -> str:
    if (standalone.height is not None):
        return f'{standalone.height} {MEAS_DIM_SPLIT} {standalone.width} {MEAS_DIM_SPLIT} {standalone.depth}'
    else:
        return f'{standalone.width} {MEAS_DIM_SPLIT} {standalone.depth}'

def _write_standalones(bom: m.BillOfMaterials, file):
    standalones = _extract_standalone(bom)

    file.write(OTHER_HEADER)
    file.write(NEWLINE)

    for s in standalones:
        file.write(f'{s.id}: {s.description} ({_standlone_dims(s)})')
        file.write(NEWLINE)

    file.write(NEWLINE)

def write(bom: m.BillOfMaterials, filepath: str):
    with open(filepath, 'w') as file:
        _write_carcasses(bom, file)
        _write_doors(bom, file)
        _write_standalones(bom, file)
