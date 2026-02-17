from sqlalchemy import Column, String, Float
from sqlalchemy.orm import relationship
from app.database.connection import Base


class State(Base):
    __tablename__ = "states"

    uf = Column(String(2), primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    base_tariff_kwh = Column(Float, nullable=False)  # Tarifa base por kWh

    suppliers = relationship(
        "Supplier",
        secondary="supplier_states",
        back_populates="states"
    )

    def __repr__(self):
        return f"<State {self.uf}>"
