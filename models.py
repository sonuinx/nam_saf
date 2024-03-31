from sqlalchemy import Column, Integer, String, Float
from database import Base,engine

class ItemModel(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True, nullable=True)
    price = Column(Float, index=True)
    tax = Column(Float, index=True, nullable=True)
Base.metadata.create_all(bind=engine)