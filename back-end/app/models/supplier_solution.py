from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database.connection import Base


class SupplierSolution(Base):
    __tablename__ = "supplier_solutions"

    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    solution_type = Column(String(20), ForeignKey("solutions.type"), nullable=False)
    cost_kwh = Column(Float, nullable=False)

    supplier = relationship("Supplier", back_populates="solutions")

    def __repr__(self):
        return f"<SupplierSolution {self.supplier_id} - {self.solution_type}>"
