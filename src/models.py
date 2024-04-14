import datetime as dt
import dataclasses as dc
from typing import List, Optional

MEAS_DIM_SPLIT = 'x'
PANEL = 'panel'
FILLER = 'filler'

@dc.dataclass
class Door:
    unit: 'Unit'
    count: int
    description: str
    height: int  # mm
    width: int  # mm

    @property
    def id(self) -> int:
        return self.unit.id

    def measurements(self) -> str:
        return f'{self.height} {MEAS_DIM_SPLIT} {self.width}'

@dc.dataclass
class Unit:
    id: int
    description: str
    height: Optional[int] = dc.field(default=None)  # mm
    width: Optional[int] = dc.field(default=None)  # mm
    depth: Optional[int] = dc.field(default=None)  # mm
    doors: List[Door] = dc.field(default_factory=list)

    def is_carcass(self) -> bool:
        return len(self.doors) > 0

    def is_panel(self) -> bool:
        return PANEL in self.description.lower()

    def is_filler(self) -> bool:
        return FILLER in self.description.lower()

    def measurements(self) -> str:
        dims = ''
        if self.height is not None:
            if len(dims) > 0:
                dims = f'{dims} {MEAS_DIM_SPLIT} {self.height}'
            else:
                dims = f'{self.height}'
        if self.width is not None:
            if len(dims) > 0:
                dims = f'{dims} {MEAS_DIM_SPLIT} {self.width}'
            else:
                dims = f'{self.width}'
        if self.depth is not None:
            if len(dims) > 0:
                dims = f'{dims} {MEAS_DIM_SPLIT} {self.depth}'
            else:
                dims = f'{self.depth}'
        return dims

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
