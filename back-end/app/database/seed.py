from sqlalchemy.orm import Session
from app.models import State, Supplier, Solution, SupplierSolution
from app.models.supplier import supplier_states
from sqlalchemy import text


def seed_database(db: Session):
    db.query(SupplierSolution).delete()
    db.query(Supplier).delete()
    db.query(Solution).delete()
    db.query(State).delete()

    states_data = [
        State(uf="SP", name="São Paulo", base_tariff_kwh=0.85),
        State(uf="RJ", name="Rio de Janeiro", base_tariff_kwh=0.78),
        State(uf="MG", name="Minas Gerais", base_tariff_kwh=0.72),
        State(uf="BA", name="Bahia", base_tariff_kwh=0.75),
        State(uf="SC", name="Santa Catarina", base_tariff_kwh=0.68),
        State(uf="PR", name="Paraná", base_tariff_kwh=0.76),
        State(uf="RS", name="Rio Grande do Sul", base_tariff_kwh=0.74),
        State(uf="DF", name="Distrito Federal", base_tariff_kwh=0.80),
        State(uf="GO", name="Goiás", base_tariff_kwh=0.71),
        State(uf="MT", name="Mato Grosso", base_tariff_kwh=0.73),
    ]
    db.add_all(states_data)
    db.commit()

    solutions_data = [
        Solution(type="GD"),
        Solution(type="Mercado Livre"),
    ]
    db.add_all(solutions_data)
    db.commit()

    suppliers_data = [
        Supplier(
            name="SunPower Brasil",
            logo_url="https://via.placeholder.com/150?text=SunPower",
            origin_state="SP",
            total_customers=15000,
            average_rating=4.8,
        ),
        Supplier(
            name="WindEnergy Plus",
            logo_url="https://via.placeholder.com/150?text=WindEnergy",
            origin_state="BA",
            total_customers=12000,
            average_rating=4.6,
        ),
        Supplier(
            name="Green Power Solutions",
            logo_url="https://via.placeholder.com/150?text=GreenPower",
            origin_state="RJ",
            total_customers=18000,
            average_rating=4.9,
        ),
        Supplier(
            name="EnergiaTech",
            logo_url="https://via.placeholder.com/150?text=EnergiaTech",
            origin_state="MG",
            total_customers=20000,
            average_rating=4.7,
        ),
        Supplier(
            name="Clean Energy Co",
            logo_url="https://via.placeholder.com/150?text=CleanEnergy",
            origin_state="SC",
            total_customers=8000,
            average_rating=4.5,
        ),
        Supplier(
            name="Energia Sustentável",
            logo_url="https://via.placeholder.com/150?text=Sustentavel",
            origin_state="PR",
            total_customers=10000,
            average_rating=4.4,
        ),
    ]
    db.add_all(suppliers_data)
    db.commit()

    associations = [
        ("SunPower Brasil", ["SP", "RJ", "MG"], [("GD", 0.45), ("Mercado Livre", 0.52)]),
        ("WindEnergy Plus", ["BA", "GO", "MT"], [("GD", 0.40), ("Mercado Livre", 0.48)]),
        ("Green Power Solutions", ["RJ", "SP", "PR"], [("GD", 0.42), ("Mercado Livre", 0.50)]),
        ("EnergiaTech", ["MG", "DF", "GO"], [("GD", 0.43), ("Mercado Livre", 0.51)]),
        ("Clean Energy Co", ["SC", "RS", "PR"], [("GD", 0.38), ("Mercado Livre", 0.46)]),
        ("Energia Sustentável", ["RS", "SC", "PR"], [("GD", 0.41), ("Mercado Livre", 0.49)]),
    ]

    for supplier_name, state_ufs, solutions in associations:
        supplier = db.query(Supplier).filter(Supplier.name == supplier_name).first()
        
        for uf in state_ufs:
            state = db.query(State).filter(State.uf == uf).first()
            if state and supplier not in state.suppliers:
                state.suppliers.append(supplier)
        
        for solution_type, cost_kwh in solutions:
            supplier_solution = SupplierSolution(
                supplier_id=supplier.id,
                solution_type=solution_type,
                cost_kwh=cost_kwh,
            )
            db.add(supplier_solution)

    db.commit()
