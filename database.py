from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


class Rent(Base):
    __tablename__ = 'rents'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    app_number = Column(String(250), nullable=False)
    rent = Column(Integer, nullable=False)
    availability = Column(String(250), nullable=False)
    type = Column(String(250), nullable=False)

engine = create_engine('sqlite:///rents.db')


Base.metadata.create_all(engine)