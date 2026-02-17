import strawberry
from typing import List, Optional
from sqlalchemy.orm import Session
from app.schemas.types import (
    StateType,
    SupplierType,
    SupplierSolutionType,
    SimulationResultType,
    SolutionAvailabilityType,
    EconomyType,
)
from app.crud.supplier import (
    get_all_states,
    get_state,
    get_available_solutions,
    get_supplier_solutions,
)
from app.database.connection import SessionLocal
from app.models import Supplier, SupplierSolution


@strawberry.type
class Query:
    @strawberry.field
    def states(self) -> List[StateType]:
        db = SessionLocal()
        try:
            states = get_all_states(db)
            return [
                StateType(
                    uf=state.uf,
                    name=state.name,
                    base_tariff_kwh=state.base_tariff_kwh,
                )
                for state in states
            ]
        finally:
            db.close()

    @strawberry.field
    def simulate(self, state_uf: str, consumption_kwh: float) -> Optional[SimulationResultType]:
        db = SessionLocal()
        try:
            state = get_state(db, state_uf)
            if not state:
                return None

            base_cost = consumption_kwh * state.base_tariff_kwh

            solutions_query = db.query(SupplierSolution.solution_type).join(
                Supplier
            ).join(
                Supplier.states
            ).filter(
                Supplier.states.any(uf=state_uf)
            ).distinct().all()

            solutions = []
            for solution_row in solutions_query:
                solution_type = solution_row[0]
                
                suppliers_with_solution = db.query(Supplier).join(
                    SupplierSolution
                ).filter(
                    SupplierSolution.solution_type == solution_type,
                    Supplier.states.any(uf=state_uf)
                ).all()

                economy_list: List[EconomyType] = []
                best_economy = 0.0
                best_supplier_name = ""

                for supplier in suppliers_with_solution:
                    supplier_solution = get_supplier_solution(db, supplier.id, solution_type)
                    if supplier_solution:
                        supplier_cost = consumption_kwh * supplier_solution.cost_kwh
                        economy = base_cost - supplier_cost
                        economy_percentage = (economy / base_cost * 100) if base_cost > 0 else 0

                        economy_data = EconomyType(
                            supplier_id=supplier.id,
                            supplier_name=supplier.name,
                            logo_url=supplier.logo_url,
                            solution_type=solution_type,
                            cost_kwh=supplier_solution.cost_kwh,
                            base_cost=base_cost,
                            supplier_cost=supplier_cost,
                            economy=economy,
                            economy_percentage=economy_percentage,
                            total_customers=supplier.total_customers,
                            average_rating=supplier.average_rating,
                        )
                        economy_list.append(economy_data)

                        if economy > best_economy:
                            best_economy = economy
                            best_supplier_name = supplier.name

                if economy_list:
                    solutions.append(
                        SolutionAvailabilityType(
                            solution_type=solution_type,
                            suppliers=economy_list,
                            best_economy=best_economy,
                            best_supplier=best_supplier_name,
                        )
                    )

            return SimulationResultType(
                state_uf=state_uf,
                consumption_kwh=consumption_kwh,
                base_cost=base_cost,
                solutions=solutions,
            )
        finally:
            db.close()


def get_supplier_solution(db: Session, supplier_id: int, solution_type: str):
    return db.query(SupplierSolution).filter(
        SupplierSolution.supplier_id == supplier_id,
        SupplierSolution.solution_type == solution_type,
    ).first()


schema = strawberry.Schema(query=Query)
