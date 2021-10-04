import pathlib

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.orm import sessionmaker, declarative_base


apc_dir = pathlib.Path.home().joinpath(".apc-power-usage").resolve()
if not apc_dir.exists():
    apc_dir.mkdir()


engine = create_engine(
    "sqlite:///{}/main.db".format(apc_dir), connect_args={"check_same_thread": False}
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
