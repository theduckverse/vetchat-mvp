from sqlalchemy import create_engine, Column, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///./supporters.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class Supporter(Base):
    __tablename__ = "supporters"
    email = Column(String, primary_key=True, index=True)
    active = Column(Boolean, default=True)

def init_db():
    Base.metadata.create_all(bind=engine)
