import csv
import dataclasses as dc
from typing import List, Optional

import bom.models as m

HEADER_ROW = ['Group', 'Type', 'ID', 'Quantity', 'Description', 'Height [mm]', 'Width [mm]', 'Depth [mm]']

@dc.dataclass
class Row:
    group: str
    type: str
    id: int
    quantity: Optional[int] = dc.field(default=None)
    description: str = dc.field(default='')
    height: Optional[int] = dc.field(default=None)
    width: Optional[int] = dc.field(default=None)
    depth: Optional[int] = dc.field(default=None)

    def values(self) -> List[object]:
        return [self.group, self.type, self.id, self.quantity, self.description, self.height, self.width, self.depth]

def _build_unit_row(group_label: str, unit: m.Unit) -> Row:
    return Row(group_label, unit.type, unit.id, 1, unit.description, unit.height, unit.width, unit.depth)

def _build_door_row(group_label: str, door: m.Door) -> Row:
    return Row(group_label, door.type, door.id, door.count, door.description, door.height, door.width)

def _build_rows(bom: m.BillOfMaterials) -> List[Row]:
    rows = []
    for group in bom.groups:
        for unit in group.units:
            rows.append(_build_unit_row(group.label, unit))
            for door in unit.doors:
                rows.append(_build_door_row(group.label, door))
    return rows

def _order_rows(rows: List[Row]) -> List[Row]:
    # sort by type 
    # then sort by id
    return sorted(rows, key=lambda r: (r.type, r.id))

def write(bom: m.BillOfMaterials, filepath: str):
    rows = _build_rows(bom)
    ordered_rows = _order_rows(rows)
    with open(filepath, 'w', newline='', encoding='utf-16') as csvfile:
        writer = csv.writer(csvfile, dialect='excel-tab')
        writer.writerow(HEADER_ROW)
        for row in ordered_rows:
            writer.writerow(row.values())
