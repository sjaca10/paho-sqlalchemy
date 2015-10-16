from sqlalchemy import Column, Integer, Float
from Base import Base

class Position(Base):
    __tablename__ = 'position'

    id        = Column(Integer, primary_key = True)
    latitude  = Column(Float)
    longitude = Column(Float)

    def __repr__(self):
        return "<Position(id='%d', latitude='%s', longitude='%s')>" % (self.id,
            self.latitude, self.longitude)