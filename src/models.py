from dataclasses import dataclass

@dataclass
class Unit:
    id: int
    description: str
    height: float  # mm
    width: float  # mm
    depth: float  # mm

@dataclass
class Door:
    id: int
    unit_id: int
    count: int
    height: float  # mm
    width: float  # mm
    depth: float  # mm
