from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.orm import sessionmaker, declarative_base


engine = create_engine(
    "sqlite:///foo.db", connect_args={"check_same_thread": False}
)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class APCReading(Base):
    __tablename__ = "apc_reading"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime(timezone=True))
    no_logs = Column(Integer)
    load = Column(Float)


Base.metadata.create_all(engine)
