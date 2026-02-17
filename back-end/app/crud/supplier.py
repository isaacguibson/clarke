from sqlalchemy.orm import Session
from app.models import State, Supplier, Solution, SupplierSolution
from sqlalchemy import and_


def get_state(db: Session, uf: str):
    return db.query(State).filter(State.uf == uf).first()


def get_all_states(db: Session):
    return db.query(State).all()


def get_suppliers_by_state_and_solution(db: Session, state_uf: str, solution_type: str):
    return db.query(Supplier).join(
        Supplier.states
    ).join(
        SupplierSolution
    ).filter(
        and_(
            State.uf == state_uf,
            SupplierSolution.solution_type == solution_type,
            SupplierSolution.supplier_id == Supplier.id
        )
    ).distinct().all()


def get_supplier_solutions(db: Session, supplier_id: int, solution_type: str):
    return db.query(SupplierSolution).filter(
        and_(
            SupplierSolution.supplier_id == supplier_id,
            SupplierSolution.solution_type == solution_type
        )
    ).first()


def get_available_solutions(db: Session, state_uf: str):
    return db.query(Solution.type).join(
        SupplierSolution
    ).join(
        Supplier
    ).join(
        Supplier.states
    ).filter(
        State.uf == state_uf
    ).distinct().all()


def get_suppliers_in_state(db: Session, state_uf: str):
    return db.query(Supplier).join(
        Supplier.states
    ).filter(State.uf == state_uf).all()
