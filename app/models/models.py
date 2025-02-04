from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    password = Column(String, unique=False, nullable=False)
    reservations = relationship("Reservation", back_populates="reservation_owner")


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    capacity = Column(Integer, unique=False, nullable=False)
    location = Column(String, nullable=False)


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    owner = Column(Integer, ForeignKey("users.id"), nullable=False)
    room = Column(Integer, ForeignKey("rooms.id"), unique=False, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    reservation_owner = relationship("User", back_populates="reservations")
    reserved_room = relationship("Room")


DATABASE_URL = "postgresql://admin:admin@localhost:5432/mysideapi"
engine = create_engine(DATABASE_URL)

Base.metadata.create_all(bind=engine)