from typing import List

import models as m

BOM_HEADER = 'Bill of Materials'
DIVIDER = '==='
CARCASS_HEADER = 'Carcasses'
DOORS_HEADER = 'Doors'
PANELS_HEADER = 'Panels'
FILLERS_HEADER = 'Fillers'
OTHER_HEADER = 'Other'

COUNT_SPLIT = 'X'
NEWLINE = '\n'

def _write_header(bom: m.BillOfMaterials, file):
    file.write(BOM_HEADER)
    file.write(NEWLINE)
    file.write(f'Generated: {bom.timestamp.strftime("%Y/%m/%d, %H:%M:%S")}')
    file.write(NEWLINE)
    file.write(DIVIDER)
    file.write(NEWLINE)

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

    if len(carcasses) == 0:
        return

    file.write(CARCASS_HEADER)
    file.write(NEWLINE)

    for c in carcasses:
        file.write(f'{c.id}: {c.description} ({c.measurements()})')
        file.write(NEWLINE)

    file.write(NEWLINE)

def _write_doors(bom: m.BillOfMaterials, file):
    doors = _extract_doors(bom)

    if len(doors) == 0:
        return

    file.write(DOORS_HEADER)
    file.write(NEWLINE)

    for d in doors:
        file.write(f'{d.id}: {d.count} {COUNT_SPLIT} {d.measurements()} ({d.description})')
        file.write(NEWLINE)

    file.write(NEWLINE)

def _write_standalones(bom: m.BillOfMaterials, file):
    standalones = _extract_standalone(bom)
    panels = [u for u in standalones if u.is_panel()]
    fillers = [u for u in standalones if u.is_filler()]
    others = [u for u in standalones if not u.is_panel() and not u.is_filler()]

    print(standalones)
    print(panels)

    _write_standalone_units(PANELS_HEADER, panels, file)
    _write_standalone_units(FILLERS_HEADER, fillers, file)
    _write_standalone_units(OTHER_HEADER, others, file)

def _write_standalone_units(header: str, units: List[m.Unit], file):
    if len(units) == 0:
        return

    file.write(header)
    file.write(NEWLINE)

    for u in units:
        file.write(f'{u.id}: {u.description} ({u.measurements()})')
        file.write(NEWLINE)

    file.write(NEWLINE)

def write(bom: m.BillOfMaterials, filepath: str):
    with open(filepath, 'w', encoding='utf-8') as file:
        _write_header(bom, file)
        _write_carcasses(bom, file)
        _write_doors(bom, file)
        _write_standalones(bom, file)
