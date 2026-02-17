from sqlalchemy import Column, Integer, String, Float, Table, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database.connection import Base

# Tabela de relacionamento many-to-many
supplier_states = Table(
    "supplier_states",
    Base.metadata,
    Column("supplier_id", Integer, ForeignKey("suppliers.id"), primary_key=True),
    Column("state_uf", String(2), ForeignKey("states.uf"), primary_key=True),
)


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    logo_url = Column(String(500), nullable=True)
    origin_state = Column(String(2), ForeignKey("states.uf"), nullable=False)
    total_customers = Column(Integer, default=0)
    average_rating = Column(Float, default=0.0)

    states = relationship(
        "State",
        secondary=supplier_states,
        back_populates="suppliers"
    )

    solutions = relationship("SupplierSolution", back_populates="supplier", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Supplier {self.name}>"
