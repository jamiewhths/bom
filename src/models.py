import datetime as dt
import dataclasses as dc
from typing import List, Optional

@dc.dataclass
class Door:
    unit_id: int
    # id: int
    count: int
    description: str
    height: int  # mm
    width: int  # mm
    # depth: int  # mm

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

    def carcasses(self) -> List[Unit]:
        carcasses = []
        for group in self.groups:
            for unit in group.units:
                if not unit.is_carcass():
                    continue
                carcasses.append(unit)
        return carcasses
