import strawberry
from typing import Optional, List


@strawberry.type
class StateType:
    uf: str
    name: str
    base_tariff_kwh: float


@strawberry.type
class SolutionType:
    solution_type: str = strawberry.field(name="type")


@strawberry.type
class SupplierSolutionType:
    id: int
    supplier_id: int
    solution_type: str = strawberry.field(name="type")
    cost_kwh: float


@strawberry.type
class SupplierType:
    id: int
    name: str
    logo_url: Optional[str]
    origin_state: str
    total_customers: int
    average_rating: float
    solutions: List[SupplierSolutionType]


@strawberry.type
class EconomyType:
    supplier_id: int
    supplier_name: str
    logo_url: Optional[str]
    solution_type: str
    cost_kwh: float
    base_cost: float
    supplier_cost: float
    economy: float
    economy_percentage: float
    total_customers: int
    average_rating: float


@strawberry.type
class SolutionAvailabilityType:
    solution_type: str
    suppliers: List[EconomyType]
    best_economy: float
    best_supplier: str


@strawberry.type
class SimulationResultType:
    state_uf: str
    consumption_kwh: float
    base_cost: float
    solutions: List[SolutionAvailabilityType]
