from sqlalchemy import Column, String
from app.database.connection import Base


class Solution(Base):
    __tablename__ = "solutions"

    type = Column(String(20), primary_key=True)  # GD ou Mercado Livre

    def __repr__(self):
        return f"<Solution {self.type}>"
