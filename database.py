from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Apartment(Base):
    __tablename__ = 'apartments'

    id = Column(Integer, primary_key=True)
    app_number = Column(String(250), nullable=False)
    path_to_floor_plan = Column(String(250), nullable=False)
    availability = Column(String(250), nullable=False)
    type = Column(String(250), nullable=False)


class Rent(Base):
    __tablename__ = 'rents'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    rent = Column(Integer, nullable=False)
    apartment_id = Column(Integer, ForeignKey('apartments.id'))
    Apartment = relationship(Apartment)

engine = create_engine('sqlite:///rents.db')


Base.metadata.create_all(engine)
