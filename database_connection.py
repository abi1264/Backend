from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

DATABASE_URL="postgresql://postgres:abishek@localhost:5432/Mero_db"

engine =create_engine(DATABASE_URL)
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base=declarative_base()


#DEPENDENCY INJECTION
def get_db():
    db=SessionLocal()
    try:
        yield db

    finally:
        db.close()



