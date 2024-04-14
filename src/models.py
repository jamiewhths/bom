import datetime as dt
import dataclasses as dc
from typing import List, Optional

@dc.dataclass
class Door:
    unit: 'Unit'
    # id: int
    count: int
    description: str
    height: int  # mm
    width: int  # mm
    # depth: int  # mm

    @property
    def id(self) -> int:
        return self.unit.id

@dc.dataclass
class Unit:
    id: int
    description: str
    width: int  # mm
    depth: int  # mm
    height: Optional[int] = dc.field(default=None)  # mm
    doors: List[Door] = dc.field(default_factory=list)

    def is_carcass(self) -> bool:
        return len(self.doors) > 0

@dc.dataclass
class Group:
    label: str
    units: List[Unit] = dc.field(default_factory=list)

@dc.dataclass
class BillOfMaterials:
    timestamp: dt.datetime = dc.field(init=False, default_factory=dt.datetime.now)
    groups: List[Group] = dc.field(init=False, default_factory=list)

    def carcass_units(self) -> List[Unit]:
        units = []
        for group in self.groups:
            for unit in group.units:
                if not unit.is_carcass():
                    continue
                units.append(unit)
        return units
    
    def standalone_units(self) -> List[Unit]:
        units = []
        for group in self.groups:
            for unit in group.units:
                if unit.is_carcass():
                    continue
                units.append(unit)
        return units
